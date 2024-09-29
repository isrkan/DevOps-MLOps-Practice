# Monitoring Dockerized web applications with Prometheus
In this guide, we will configure Prometheus to monitor the performance of containers in a web application deployed with Docker Compose. The focus is on container metrics, such as CPU and memory usage, rather than the web application itself.

**Prerequisites**:
- A deployed web application using Docker Compose.
- Prometheus installed (or configured in Docker Compose).

## Step 1: Expose web application metrics
To monitor a web application like Django or Spring Boot, we need to expose application-specific metrics in a format that Prometheus can scrape. The method for doing this varies slightly between frameworks. Instructions for some frameworks are provided in the `Web applications` directory within this repository. We can follow those guides (for Spring Boot and Django, follow the first two steps of the corresponding guides).

## Step 2: Configure Prometheus to scrape both Docker and application metrics
To scrape both **container metrics** (via cAdvisor) and **application metrics** (e.g., Django or Spring Boot), follow these steps:

### 1. Add the Prometheus and cAdvisor to `docker-compose.yml`
To monitor Docker containers, we will use **Prometheus**, **cAdvisor** (a tool by Google that exposes resource usage and performance metrics for running containers) and our web applications. Here’s an example configuration how to add Prometheus and cAdvisor to our existing `docker-compose.yml`:

```yaml
version: '1'
services:
  # Our existing web app services (e.g., Django, Spring Boot)
  webapp:
    image: mywebapp:latest
    ports:
      - "8082:8081"
    # other configurations...

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8083:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
```

In this setup:
- **Prometheus** is configured to scrape metrics, and it exposes its UI on `localhost:9090`.
- **cAdvisor** collects container resource usage data and exposes metrics on `localhost:8083`.

### 2. Create the `prometheus.yml` configuration
Create the `prometheus.yml` file that configures Prometheus to scrape **container metrics** (via cAdvisor), **application metrics** (such as Django or Spring Boot) and Prometheus itself.

```yaml
global:
  scrape_interval: 10s  # Scrape metrics every 10 seconds

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']  # Monitor Prometheus itself

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']   # Monitor container metrics via cAdvisor

  - job_name: 'django_app'
    static_configs:
      - targets: ['webapp:8000/metrics']  # Scrape Django app metrics

  - job_name: 'spring_boot_app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['webapp:8081']  # Scrape Spring Boot app metrics
```

- **Prometheus**: Scrapes its own metrics at `localhost:9090`.
- - **cAdvisor**: Scrapes Docker container metrics from the cAdvisor endpoint at `cadvisor:8080`. cAdvisor runs on port `8080` inside the container, and Prometheus scrapes its metrics using the `cadvisor` job.
- **Django App**: Prometheus scrapes metrics from the Django app running at `webapp:8000/metrics`. The Django app is running on port `8000`, and its metrics are exposed at `/metrics` using the `django-prometheus` integration.
- **Spring Boot App**: Prometheus scrapes metrics from the Spring Boot app running at `webapp:8081/actuator/prometheus`. The Spring Boot app is running on port `8081`, and its metrics are available at `/actuator/prometheus` using **Micrometer** and the Prometheus registry.

Place the `prometheus.yml` file in the same directory as our `docker-compose.yml`.

### 3. For Spring Boot applications: Rebuild the Spring Boot application
Before starting the Docker Compose stack, ensure that our Spring Boot application is properly configured with the Actuator and Prometheus metrics. Rebuild the Spring Boot application using:
```bash
./mvnw clean package
```

This will ensure the Spring Boot app is ready to expose metrics.

### 4. For Django applications: Update the `ALLOWED_HOSTS` setting
1. Open the `settings.py` file.

2. **Update `ALLOWED_HOSTS`**: Add the service name (in this case, `expenses`) to the `ALLOWED_HOSTS` list. Our `ALLOWED_HOSTS` setting should look something like this:
   ```python
   ALLOWED_HOSTS = [
       'localhost',        # Local development
       '127.0.0.1',       # Local development
       'expenses',        # Docker service name
       'expenses:8003',   # If needed for specific host access
       # Add other hosts if necessary
   ]
   ```

   With these changes, Prometheus should be able to scrape the metrics without encountering the `DisallowedHost` error. This is a common issue in Django applications when they are hosted behind Docker or in other environments where service names are used as hostnames.

## Step 3: Start the Docker Compose stack
Now that Prometheus and cAdvisor are configured, start the Docker Compose stack:
```bash
docker-compose up -d
```

This command will start our web application along with Prometheus and cAdvisor. We should see the services running:
```bash
docker ps
```

## Step 4: Access Prometheus and view metrics

1. **Access Prometheus**: Open the browser and go to:
   ```
   http://localhost:9090
   ```

   This is the Prometheus UI, where we can query metrics, check target status, and view collected data.
2. **Check targets**: Navigate to the **Status > Targets** page (`http://localhost:9090/targets`) to verify that Prometheus is successfully scraping metrics from cAdvisor and the webapps. Each target should display its status (e.g., **UP**) if Prometheus is successfully scraping metrics.
3. **Query metrics**: Use the Prometheus query language (PromQL) to explore webapps and container performance metrics. Some useful metrics to monitor Docker container performance include:
   - **`container_cpu_usage_seconds_total`**: Total CPU usage per container.
   - **`container_memory_usage_bytes`**: Memory usage per container.
   - **`container_network_receive_bytes_total`**: Network received data per container.
   - **`container_network_transmit_bytes_total`**: Network transmitted data per container.

## Step 5: Visualizing metrics in Grafana (Optional)
For better visualization, we can connect Grafana to Prometheus and create dashboards. Instead of manually configuring Grafana, we will use Provisioning to automate the setup of data sources and dashboards. This ensures that every time Grafana is deployed or restarted, it automatically loads the configurations we define. Here’s a brief setup guide:

### 1. Add Grafana to `docker-compose.yml`
Add the following configuration to the `docker-compose.yml` file to start Grafana and enable automatic provisioning of data sources and dashboards:
```yaml
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning  # Mount provisioning directory
    depends_on:
      - prometheus
```

This mounts the local `./grafana/provisioning` directory inside the Grafana container at `/etc/grafana/provisioning`, where Grafana expects the provisioning files.

### 2. Create the provisioning directory structure
In the root of our project (where `docker-compose.yml` is located), create the following directory structure:
```
grafana/
└── provisioning/
    ├── dashboards/
    │   ├── dashboards.yaml  # File for loading dashboards
    │   ├── my-dashboard.json  # JSON dashboard configuration
    └── datasources/
        └── datasources.yaml  # File for configuring data sources
```

#### 3. Configure the data source
In `grafana/provisioning/datasources/datasources.yaml`, define the Prometheus data source:
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
```

- **name**: The name of the data source (in this case, Prometheus).
- **url**: The Prometheus service URL within the Docker network (`http://prometheus:9090`).
- **isDefault**: Set to `true` so Prometheus is the default data source.

#### 4. Configure dashboards
In `grafana/provisioning/dashboards/dashboards.yaml`, define where Grafana will look for dashboard files:
```yaml
apiVersion: 1

providers:
  - name: "Dashboard Provider"
    orgId: 1
    type: file
    options:
      path: /etc/grafana/provisioning/dashboards
```

- **path**: Points to `/etc/grafana/provisioning/dashboards` where our JSON dashboard files are located.

#### 5. Add a dashboard
Create a JSON dashboard file (e.g., `grafana/provisioning/dashboards/my-dashboard.json`). We can create this manually or download a pre-built dashboard from the Grafana dashboard repository. Here is an example of a basic dashboard JSON:
```json
{
  "dashboard": {
    "id": null,
    "title": "My Prometheus Dashboard",
    "panels": [
      {
        "type": "graph",
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total[5m])"
          }
        ]
      }
    ],
    "schemaVersion": 16,
    "version": 1
  }
}
```

This dashboard includes a single graph that monitors CPU usage for the Docker containers.

#### 6. Start the Docker Compose stack
After setting up provisioning, start our Docker Compose stack:
```bash
docker-compose up -d
```

This will bring up the Grafana container, and it will automatically load the data sources and dashboards we configured.

### 7. Access Grafana
- Open the browser and visit:
  ```
  http://localhost:3001
  ```

- **Login**: Use the default credentials `admin` / `admin`, and change the password when prompted (or skip it).
- Check the data sources at `http://localhost:3001/connections/datasources` to confirm Prometheus is pre-configured.
- View the pre-loaded dashboards at `http://localhost:3001/dashboards`, including any dashboards we defined in JSON.

### 8. Create dashboards manually
We can create dashboards to visualize container performance, using metrics like CPU, memory, and network traffic. Grafana also provides pre-built dashboards for Docker and cAdvisor metrics, which can be imported directly from the Grafana dashboard repository.

---

## Useful Prometheus metrics for container monitoring
Here are some key metrics we can use to monitor our containerized application:

1. **CPU usage**: 
   ```promql
   rate(container_cpu_usage_seconds_total[5m])
   ```

2. **Memory usage**: 
   ```promql
   container_memory_usage_bytes
   ```

3. **Network usage (Received)**: 
   ```promql
   rate(container_network_receive_bytes_total[5m])
   ```

4. **Network usage (Transmitted)**:
   ```promql
   rate(container_network_transmit_bytes_total[5m])
   ```

5. **Disk I/O**:
   ```promql
   rate(container_fs_reads_bytes_total[5m])  # Disk read
   rate(container_fs_writes_bytes_total[5m])  # Disk write
   ```

---

## Scaling and customizing the setup

- **Custom Metrics**: If we need to monitor custom metrics from our application (e.g., business logic metrics in Django or Spring Boot), integrate Prometheus directly within the web app using libraries like `django-prometheus` or `micrometer`.