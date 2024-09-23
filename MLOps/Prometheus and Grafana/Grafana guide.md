# Grafana guide

In this guide, we will walk through how to start with Grafana, connect it to Prometheus, and create dashboards to visualize metrics.

## Prerequisites
- Grafana installed on our machine.
- Prometheus installed and running locally.

## Starting Grafana server locally
1. After installation, start Grafana by navigating to the Grafana directory
   ```sh
   cd "C:\Program Files\GrafanaLabs\grafana\bin"
   ```

2. Then, run the following command:
   ```sh
   grafana-server
   ```

3. Now, open a browser and go to:
   ```
   http://localhost:3000
   ```

4. Login with the default credentials:
   ```
   Username: admin
   Password: admin
   ```

   We will be prompted to change the password after the first login.

---

## Connecting Grafana to Prometheus
Once Grafana is up and running, we can configure it to use Prometheus as a data source.
1. **Open Grafana UI**: Go to `http://localhost:3000`, and log in.
2. **Navigate to data sources**: From the left-hand menu, click on **Data Sources**.
3. **Add a new data source**: Click the **Add data source** button and select **Prometheus** from the list of available data sources.
4. **Configure Prometheus**: In the **URL** field, enter the address where Prometheus is running (e.g., `http://localhost:9090`). Leave other settings as default, and click **Save & Test** to verify that Grafana can connect to Prometheus.

---

## Creating dashboards in Grafana
Once Prometheus is connected, we can create dashboards to visualize our metrics.

1. **Create a dashboard**: From the left-hand menu, click on **Dashboards**, then select **Create ashboard**. Click **Add visualization**, and choose **Prometheus** as the data source.
2. **Edit a panel**: We will be taken to the panel editor to start configuring our first panel.
3. **Select a metric**: In the **Metric** field, ensure the tab is set to **code**. Then, start typing the name of the metric we want to visualize (e.g., `up`, `node_cpu_seconds_total`, `http_requests_total`).
4. **Visualize the metric**: Click **Run queries**, and the graph will be updated automatically based on the metric. Use the **Visualization** section to change the type of chart (e.g., graph, table, heatmap).
5. **Save the dashboard**: After configuring the panel, click **Apply**. To save the dashboard, click the **Save** button (disk icon) at the top-right and give our dashboard a name.

---

## Useful Grafana features

1. **Customizing panels**: Each panel in Grafana can be customized to fit our needs:
    - **Visualization type**: We can choose from different visualizations like graphs, bar charts, tables, or single-stat panels.
    - **Panel options**: Customize panel titles, display units, time ranges, and thresholds.

2. **Adding variables**: Variables allow us to create dynamic dashboards where we can filter data. To add a variable:
    1. Go to **Dashboard Settings** (gear icon) > **Variables**.
    2. Click **Add variable** and define a query-based variable, which pulls options dynamically from Prometheus.

    For example, to add a variable for instances:
    ```yaml
    Label: instance
    Query: label_values(up, instance)
    ```

    This will create a drop-down that lets us filter data by specific instances.

---

## Grafana alerts

Grafana allows us to set up alerts based on metrics, which can notify us when certain conditions are met.

1. **Go to the panel**: Open any panel where we would like to create an alert.
2. **Create an alert**: Click on the **Alert** tab within the panel editor. Click **Create Alert** and define the alert condition. For example, alert if the metric `up` (for instance availability) is `0` for 5 minutes.
3. **Notification channels**: Configure how alerts are sent (e.g., email, Slack, PagerDuty). Go to **Alerting** > **Notification Channels** from the left-hand menu to set up channels.

---

## Useful Grafana commands and features

- **Backup and restore dashboards**:
  Dashboards can be exported and imported via JSON files. To export a dashboard:
  1. Open the dashboard.
  2. Click on the **Dashboard Settings** (gear icon) and select **Export JSON**.
  
  To import a dashboard, click **+ (Create)** > **Import**, and upload the JSON file.

- **Viewing logs**:
  Grafana logs can be viewed to troubleshoot issues. The logs are located in:
  - **Windows**: `C:\Program Files\GrafanaLabs\grafana\data\log\grafana.log`