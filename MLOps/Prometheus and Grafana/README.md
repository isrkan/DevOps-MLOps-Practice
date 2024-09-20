# Getting started with Prometheus and Grafana

Prometheus and Grafana are popular open-source tools that provide monitoring and visualization solutions. While Prometheus collects and stores the time-series data, Grafana helps to visualize this data in interactive dashboards, making it easier to gain insights from metrics and set up alerts. This repository will introduce the core concepts of both systems, how to set them up, and how to leverage them for monitoring ML models, backend services, and general infrastructure.

## Prometheus
Prometheus is an open-source system monitoring and alerting toolkit designed to collect metrics, store them as time series, and provide a query language (PromQL) to analyze them. It is primarily used to monitor services, applications, and infrastructure.

### Core concepts of Prometheus
1. **Time-Series data**: Prometheus stores all data as time-series data, meaning each metric is stored with timestamps.
2. **Metrics**: Metrics are named data that describe some measurable aspect of the system (e.g., CPU usage, memory consumption, network traffic, etc).
3. **Labels**: Metrics can have labels, which are key-value pairs, used to identify different streams of time-series data. For instance, a metric for CPU usage can have labels for different nodes or containers.
4. **PromQL (Prometheus query language)**: Prometheus has its own query language to retrieve and filter data from the time-series database.
5. **Scraping**: Prometheus pulls (or "scrapes") metrics data from targets (services or applications) at defined intervals.
6. **Exporters**: Exporters are programs that expose metrics in a format that Prometheus can scrape. For example, we can have an exporter that exposes CPU, memory, or custom metrics from our applications.

### How Prometheus works
Prometheus works on a pull model, scraping predefined targets or endpoints that expose their metrics in a Prometheus-compatible format. The collected metrics are stored in a time-series database that allows us to query and analyze them. Here’s a high-level overview:
1. **Prometheus Server**: This is the central server that scrapes metrics from targets, stores, and queries the metrics.
2. **Targets**: The services or applications that expose metrics (e.g., a web server or a machine learning model).
3. **Storage**: Time-series database for storing scraped metrics.
4. **Alerts**: Configurable rules based on the scraped metrics.

## Grafana
Grafana is an open-source analytics and interactive visualization platform. It provides a rich dashboarding interface for Prometheus and other data sources. Grafana enables us to visualize, explore, and create alerts on time-series data.

### Key concepts of Grafana
1. **Dashboards**: A collection of panels that visualize metrics. Dashboards are highly customizable and allow for interactive exploration of the data.
2. **Panels**: The building blocks of a Grafana dashboard. A panel can represent a graph, heatmap, table, or any other visual representation of our data.
3. **Data sources**: Grafana can integrate with various data sources like Prometheus, InfluxDB, Elasticsearch, etc.
4. **Queries**: Each panel uses queries to retrieve and display data. With Prometheus as a data source, we will write PromQL queries to visualize the metrics.
5. **Alerting**: Grafana allows for visual and rule-based alerts that can be sent via email, Slack, or other notification channels.
