# Prometheus guide

This directory will help you start Prometheus, configure it using the `prometheus.yml` file, and explain how to manage Prometheus instances on a local machine. 

## Starting Prometheus server locally
To start Prometheus on Windows, follow these steps:

1. Navigate to the directory where Prometheus is extracted. For example:
    ```sh
    cd C:\Prometheus
    ```
2. Run the following command to start the Prometheus server:
    ```sh
    prometheus --config.file=prometheus.yml --web.enable-lifecycle
    ```

    This command launches Prometheus with the default configuration found in `prometheus.yml`. We use the `--web.enable-lifecycle` flag to dynamically reload the configuration file and perform other lifecycle management tasks (like shutting down Prometheus) without having to restart the Prometheus server manually. This is particularly useful when managing Prometheus in production environments, where minimizing downtime is critical.
3. Once the command is executed, we should see logs related to Prometheus scraping and server startup. These logs help us ensure that Prometheus is running correctly.
4. Once the server is running, we can access the Prometheus UI. Open a browser and visit:
    ```
    http://localhost:9090
    ```

    The Prometheus dashboard lets us interact with various Prometheus features, query metrics, and monitor the status of the server and targets.

If we started Prometheus using the command line, the easiest way to shut it down is to press `CTRL + C`. This will terminate the server process gracefully.

---

## The `prometheus.yml` configuration file

The `prometheus.yml` file is the core configuration file that defines how Prometheus behaves. It defines how Prometheus collects, scrapes, and handles the metrics.

Here’s a breakdown of each major section of the configuration file:

### 1. Global configuration
The **global configuration** sets parameters that apply to all scrape jobs unless overridden in a specific job.
```yaml
global:
  scrape_interval: 15s       # Default scrape interval. How often to scrape targets.
  evaluation_interval: 15s   # How often rules will be evaluated.
  scrape_timeout: 10s        # Timeout for scraping targets (optional).
```

- **scrape_interval**: The frequency (default is `15s`) at which Prometheus scrapes data from the targets. A lower interval means more frequent data collection, but can increase resource consumption.
- **evaluation_interval**: This defines how often Prometheus evaluates the alerting rules.
- **scrape_timeout**: The time limit for a single scrape to succeed or fail (default is `10s`).

### 2. Scrape configuration
Scrape configurations define what targets Prometheus monitors and how to scrape them. Each block defines a job, and each job has one or more targets. Here’s an example `prometheus.yml` with a scrape configuration:
```yaml
scrape_configs:
  - job_name: 'prometheus'   # This job monitors Prometheus itself.
    static_configs:
      - targets: ['localhost:9090']
```

- **job_name**: Identifies the job (e.g., `prometheus`). Jobs categorize the scraping process, and each job can scrape multiple targets.
- **static_configs**: This defines static targets that Prometheus should scrape.
- **targets**: List of addresses (host and port) Prometheus should scrape. For Prometheus itself, it's `localhost:9090`.

#### Adding a custom target
We can add more jobs to scrape additional services. Here’s an example of scraping a web application running on `localhost:8080`:
```yaml
scrape_configs:
  - job_name: 'my_webapp'
    static_configs:
      - targets: ['localhost:8080']
```

### 3. Alerting and rules
Prometheus can trigger alerts when certain conditions are met. These alerts can be configured within the `prometheus.yml` file or referenced externally. Here’s how alerting can be configured:
```yaml
rule_files:
  - "alert.rules.yml"  # Reference to an external rules file.

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'localhost:9093'  # Address of the Alertmanager.
```

- **rule_files**: A list of external files containing alerting rules.
- **alerting**: Defines the alerting manager targets. Alertmanager is a service that handles alert notifications.

#### Example Alerting Rule
A simple rule that triggers an alert when Prometheus has missed scrapes for more than 5 minutes:

```yaml
groups:
  - name: example-alerts
    rules:
    - alert: InstanceDown
      expr: up == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Instance {{ $labels.instance }} down"
        description: "The instance {{ $labels.instance }} has been down for more than 5 minutes."
```

- **expr**: The expression (`up == 0`) defines the condition when the alert should be triggered.
- **for**: The alert only fires if the condition holds true for the specified time (`5m`).
- **labels**: Labels attached to the alert, like severity.
- **annotations**: Human-readable descriptions of the alert.

---

## Useful Prometheus commands

- **Reload Prometheus configurations without restarting**: Once Prometheus is running, if we make changes to the `prometheus.yml` file, we can reload the configuration without restarting the server. We can do this by openning PowerShell and running the command:
  ```sh
  Invoke-RestMethod -Uri http://localhost:9090/-/reload -Method Post
  ```

- **View available metrics**: We can see all the available metrics in Prometheus by visiting:
  ```sh
  http://localhost:9090/metrics
  ```

- **Querying metrics**: Use the **Prometheus Query Language (PromQL)** in the UI at `http://localhost:9090` to query metrics. Example query to check for memory usage:
  ```promql
  node_memory_MemAvailable_bytes
  ```

- **Check Prometheus logs**: Prometheus logs are very useful for debugging. If we need to see more detailed information, check the logs in the command line where the Prometheus server was started.