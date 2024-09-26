# Monitoring a Spring Boot application with Prometheus

In this guide, we will walk through how to monitor a Spring Boot application using Prometheus.

**Prerequisites**: Before starting, ensure:
- A Spring Boot application running locally.
- Prometheus installed and running on our system.

### Step 1: Update the Spring Boot app for Prometheus
To monitor the Spring Boot application, we need to prepare it to expose metrics in a format that Prometheus can scrape. We achieve this by integrating **Micrometer** and **Spring Boot Actuator**. Micrometer is a library that provides production-ready metrics for monitoring.
- **Spring Boot Actuator**: This module exposes several useful endpoints (e.g., `/health`, `/info`, etc.) to help monitor and manage our Spring Boot application. It allows us to expose metrics, health checks, environment information, and more.
- **Micrometer**: Micrometer is a library that provides production-ready metrics for monitoring. Micrometer integrates with Prometheus to provide these metrics in a format that Prometheus can scrape.

Follow these steps to prepare the Spring Boot app to expose metrics:
1. **Add dependencies**: Ensure our `pom.xml` has the required dependencies for Micrometer and Prometheus.
   ```xml
   <!-- Spring Boot Actuator (exposes the /actuator/prometheus endpoint) -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
   <!-- Micrometer Prometheus registry -->
   <dependency>
       <groupId>io.micrometer</groupId>
       <artifactId>micrometer-registry-prometheus</artifactId>
   </dependency>
   ```

   - **spring-boot-starter-actuator**: This adds Spring Boot's Actuator functionality, exposing a variety of built-in metrics and endpoints for monitoring and managing the application.
   - **micrometer-registry-prometheus**: This library enables Micrometer to export metrics to Prometheus. It provides the integration necessary to expose metrics in Prometheus' format, available at `/actuator/prometheus`.

2. **Enable Prometheus metrics in the `application.properties`**: We need to expose the metrics endpoint for Prometheus to scrape. This is done by enabling the `/actuator/prometheus` endpoint in our Spring Boot app.
    ```properties
    # Enable actuator endpoints
    management.endpoints.web.exposure.include=health,info,prometheus

    # Enable metrics for the Prometheus format
    management.metrics.export.prometheus.enabled=true

    # Expose the metrics at /actuator/prometheus
    management.endpoint.prometheus.enabled=true
    ```

   - **`management.endpoints.web.exposure.include=health,info,prometheus`**: This setting defines which Actuator endpoints are exposed over HTTP. In this case, we expose the `health`, `info`, and `prometheus` endpoints.
   - **`management.metrics.export.prometheus.enabled=true`**: This enables the export of metrics in Prometheus format, allowing Prometheus to scrape them.
   - **`management.endpoint.prometheus.enabled=true`**: This explicitly enables the `/actuator/prometheus` endpoint, which is where Prometheus will scrape the metrics.

    Now our Spring Boot application is ready to expose default and custom metrics to Prometheus.
3. **Start the Spring Boot application**: Run the Spring Boot app as usual. Now, the `/actuator/prometheus` endpoint will be available on our application. For example, if our Spring Boot app is running on port `8081`, we can access the metrics at:
   ```
   http://localhost:8081/actuator/prometheus
   ```

### Step 2: Run the Spring Boot application
Start the Spring Boot application. Once it's running, visit the `/actuator/prometheus` endpoint:
```bash
http://localhost:8081/actuator/prometheus
```

This will display a list of metrics in Prometheus format, which can be scraped by Prometheus for monitoring and analysis.

### Step 3: Configure Prometheus to scrape the Spring Boot application
Prometheus needs to be configured to scrape the metrics exposed by the Spring Boot app.

1. **Configure Prometheus to scrape metrics**: Open the `prometheus.yml` file in the Prometheus installation directory and add a job to scrape our Spring Boot app. Add the following under the `scrape_configs` section:
    ```yaml
    global:
        scrape_interval: 15s

    scrape_configs:
        - job_name: 'spring-boot-app'
          scrape_interval: 10s
          metrics_path: '/actuator/prometheus'
          static_configs:
            - targets: ['localhost:8081']
    ```

   - **scrape_interval**: How often Prometheus will scrape the app.
   - **job_name**: A name for this scrape job (e.g., `spring-boot-app`).
   - **metrics_path**: The endpoint where metrics are exposed (i.e., `/actuator/prometheus`).
   - **targets**: The URL of the Spring Boot app (e.g., `localhost:8081`).

2. **Start Prometheus**: Run Prometheus locally using the command:
    ```bash
    prometheus --config.file=path/to/prometheus.yml --web.enable-lifecycle
    ```

    Once Prometheus is running, if we make changes to the `prometheus.yml` file, we can reload the configuration without restarting the server. We can do this by running:
    ```bash
    Invoke-RestMethod -Uri http://localhost:9090/-/reload -Method Post
    ```

    Prometheus will now start scraping the metrics exposed by the Spring Boot app. We can verify this by visiting the Prometheus UI at:
    ```
    http://localhost:9090
    ```

    Navigate to the **Targets** page (`http://localhost:9090/targets`) to see if Prometheus is successfully scraping the Spring Boot app.

---

## Default metrics exposed by Spring Boot
When Prometheus scrapes the `/actuator/prometheus` endpoint, it will automatically capture a set of default metrics provided by Micrometer.

#### **HTTP request metrics** (`http.server.requests`): 
These metrics help us monitor the performance of HTTP requests handled by our application.
- `http_server_requests_seconds_count`: Total number of HTTP requests.
- `http_server_requests_seconds_sum`: Total time taken by all HTTP requests.
- `http_server_requests_seconds_max`: Maximum time taken by a request.
- `http_server_requests_active`: Number of active requests being processed.

#### **JVM metrics**:
These metrics provide insights into the state and health of the JVM running our Spring Boot app.
- **Memory**:
  - `jvm_memory_used_bytes`: Amount of memory (in bytes) used by the JVM.
  - `jvm_memory_max_bytes`: Maximum amount of memory the JVM can use.
  - `jvm_memory_committed_bytes`: Total memory committed to the JVM (allocated but not necessarily used).
- **Garbage collection**:
  - `jvm_gc_pause_seconds_count`: Number of times the garbage collector has paused.
- **Threads**:
  - `jvm_threads_live_threads`: Current number of live JVM threads.
  - `jvm_threads_daemon_threads`: Number of daemon threads in the JVM.
- **Uptime**:
  - **`process_uptime_seconds`**: Tracks how long the JVM has been running since the application started.

#### **System metrics**:
System-level metrics track resource consumption by our application.
- **CPU**:
  - `system_cpu_usage`: System-wide CPU usage.
  - `process_cpu_usage`: CPU usage by the application.

#### **Database metrics** (Hikari connection pool metrics):
If our application uses a JDBC connection pool (like Hikari), it exposes the following metrics:
- `hikaricp_connections_active`: Active database connections.
- `hikaricp_connections_pending`: Pending connection requests.
- `hikaricp_connections_max`: Maximum allowed connections.

#### **Web server metrics** (Tomcat-specific if using embedded Tomcat):
Metrics related to the embedded web server that ships with Spring Boot (Tomcat by default).
- **Active sessions**:
  - **`tomcat_sessions_active_current_sessions`**: Tracks the current number of active sessions managed by the Tomcat web server.
- **Session expiry**:
  - **`tomcat_sessions_expired_sessions_total`**: Tracks the total number of sessions that have expired.


These default metrics are useful for monitoring the overall performance and health of our Spring Boot application. We can query these metrics directly from Prometheus or visualize them in Grafana.

---

## Add custom metrics (Optional)
Sometimes, default metrics are not enough. We may want to track custom metrics specific to our application's business logic. This can include tracking the number of user logins, the processing time of a specific tasks, number of orders processed or failed transactions. In a typical Spring Boot project structure, it’s a good practice to create a dedicated package for services that handle specific business logic and to house the custom metrics logic. For example:
```
src/main/java/com/example/ourapp
    └───config
    └───controllers
    └───models
    └───repositories
    └───services   <-- Create a new package for services, including metrics logic
```

Here, we would place our class responsible for processing tasks (e.g., a service class) under `services` and inject `MeterRegistry` to define custom metrics.

1. **Inject `MeterRegistry` to define custom metrics**: Use Micrometer’s `MeterRegistry` to define custom metrics in the Spring Boot application. Here's an example of a general custom metric that tracks the number of failed requests (a metric that could be relevant for any application).

   ```java
   import io.micrometer.core.instrument.MeterRegistry;
   import org.springframework.stereotype.Service;

   @Service
   public class AppService {

       private final MeterRegistry meterRegistry;

       public AppService(MeterRegistry meterRegistry) {
           this.meterRegistry = meterRegistry;
       }

       public void handleRequest(boolean isSuccess) {
           // Increment custom counter for failed requests
           if (!isSuccess) {
               meterRegistry.counter("requests.failed").increment();
           }
       }
   }
   ```

   In this example, the custom metric `requests.failed` will track the number of failed requests.

2. **Add timers, counters, and gauges**: We can add different types of custom metrics:
   - **Counters**: For tracking events like number of requests or orders.
   - **Timers**: For tracking the duration of events, like processing time.
   - **Gauges**: For tracking variables that change over time (e.g., queue size).

   Example for tracking the time it takes to process a request:
   
   ```java
   meterRegistry.timer("request.processing.time").record(() -> {
       // Simulate task processing logic
       try {
           Thread.sleep(300); // Simulate a delay
       } catch (InterruptedException e) {
           e.printStackTrace();
       }
   });
   ```

    In this example, the custom metric `request.processing.time` tracks the time it takes to process a request or a task.

3. **Add labels to custom metrics**: Labels (or tags) allow us to categorize our metrics and filter them based on certain criteria. For instance, we may want to track failed requests by type (e.g., internal error or user error).
   ```java
   meterRegistry.counter("requests.failed", "type", "user_error").increment();
   ```

    Prometheus will now track `requests.failed` with the label `type=user_error`. We can filter or group by this label when querying in Prometheus.

4. In our current `AppService` class, we have defined the custom metric `requests.failed` as an example, but to make it visible in the Prometheus endpoint, this metric needs to be registered during the execution of the application. The `handleRequest` method has not been called yet. Prometheus will not show the custom metric unless it has been incremented or registered in a request flow. We need to make sure that our `handleRequest` method is actually invoked during the lifecycle of our application. 

    An example of how to call `handleRequest`: We can call the `handleRequest` method from a controller. Add a simple controller that invokes this method and simulates a request flow. 
    1. **Create a controller to call the service**: In our `controllers` package, create a new file called `AppController.java`:
    ```java
    package com.example.expenses.controllers;

    import com.example.expenses.services.AppService;
    import org.springframework.web.bind.annotation.GetMapping;
    import org.springframework.web.bind.annotation.RequestParam;
    import org.springframework.web.bind.annotation.RestController;

    @RestController
    public class AppController {

        private final AppService appService;

        public AppController(AppService appService) {
            this.appService = appService;
        }

        @GetMapping("/process")
        public String processRequest(@RequestParam boolean isSuccess) {
            appService.handleRequest(isSuccess);
            return isSuccess ? "Request processed successfully!" : "Request failed!";
        }
    }
    ```

    This simple controller allows us to invoke the `handleRequest` method by sending a request to the `/process` endpoint.
    2. **Test the endpoint**: After starting the Spring Boot application, test the `/process` endpoint by visiting in the browser:
    ```bash
    http://localhost:8081/process?isSuccess=false
    ```

    This simulates a failed request, causing the `requests.failed` metric to increment. We must make sure that the `handleRequest` method is called at runtime so that the metric is actually recorded. Prometheus only registers metrics that have been incremented or used. We can use this test endpoint temporarily to ensure that our metric is working. In a production system, this method would be called in our actual business logic.

5. **View custom metrics in Prometheus**: Once we have added our custom metrics, We can query them in Prometheus. For example, if we added a counter for failed requests, we can query it in Prometheus with:
    ```promql
    requests_failed_total
    ```

    This will return the total count of failed requests tracked by our custom metric. We can also check for the metric in the Prometheus endpoint by visiting:
    ```bash
    http://localhost:8081/actuator/prometheus
    ```

    Search for the `requests_failed_total` metric. If everything has been set up correctly, we should now see this metric exposed.

6. **Automate custom netric invocation in real logic (Optional)**: Once we have tested that the custom metric works, we can remove the temporary controller or refactor it so that the `handleRequest` method is invoked within our actual business logic. This ensures that the metric tracks real failures in our application flow.

---

## Visualize metrics in Grafana
Grafana offers a more advanced and user-friendly way to visualize metrics. To visualize metrics in Grafana:
  1. Install Grafana and connect it to Prometheus.
  2. Create dashboards with panels displaying key metrics such as `http_server_requests`, `requests_failed_total`, or JVM memory usage.
  3. We can also set up alerts based on metrics, e.g., alert when request latency is too high.