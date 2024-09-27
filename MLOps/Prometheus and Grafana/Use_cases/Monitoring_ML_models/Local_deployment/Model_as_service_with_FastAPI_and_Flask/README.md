# Monitoring ML models served via FastAPI and Flask applications with Prometheus

Monitoring web applications, especially when serving ML models, is critical for maintaining system reliability and performance. This guide will cover how to monitor both **operational** (system health) and **functional** (ML model behavior) metrics for two different applications: **Flask** (which sends requests to the ML model) and **FastAPI** (which serves the ML model itself). We will use **Prometheus** for metric collection and **Grafana** for visualizations.

## Prerequisites
Before starting, ensure the following are installed:
- **Flask app**: This web app sends requests to the ML model.
- **FastAPI app**: This web app serves the ML model and provides functional predictions.
- **Prometheus**: A tool to scrape and store metrics.
- **Grafana**: A visualization tool for creating dashboards using Prometheus metrics.

## Step 1: Expose Prometheus metrics from Flask and FastAPI
To monitor both apps, we need to expose metrics from both Flask and FastAPI. We'll track operational metrics for **both apps**, and functional metrics for **FastAPI**, since it serves the ML model.

#### 1.1 Install Prometheus Client libraries
Install the **Prometheus Python Client** for both Flask and FastAPI apps:
```bash
pip install prometheus_client
```

### 1.2 Expose metrics from the Flask app
We will modify the Flask app to expose operational metrics, such as request counts and latencies, that Prometheus can scrape. In our Flask app, add the following code to expose a `/metrics` endpoint:

```python
from prometheus_client import generate_latest, Counter, Histogram
from flask import Flask, Response, request
import time

app = Flask(__name__)

# Prometheus metrics
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('flask_request_count', 'Request Count', ['endpoint', 'http_status'])

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_metrics(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.path, response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(port=5000)
```

Here, we are tracking:
- **Request latency**: How long each request takes.
- **Request count**: The number of requests to each endpoint.

### 1.3 Expose metrics from the FastAPI app
Similarly, we will add operational metrics to the FastAPI app, as well as functional metrics to track the ML model's behavior. First, modify our FastAPI app to include the following:

```python
from prometheus_client import generate_latest, Counter, Histogram, Gauge
from fastapi import FastAPI, Request
from starlette.responses import Response
import time

app = FastAPI()

# Operational metrics
REQUEST_LATENCY = Histogram('fastapi_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('fastapi_request_count', 'Request count', ['endpoint', 'http_status'])

# Functional metrics (for the ML model)
MODEL_PREDICTIONS = Counter('model_predictions_total', 'Total number of model predictions', ['model'])
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of model predictions', ['model'])

@app.middleware("http")
async def track_request_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(request.url.path).observe(latency)
    REQUEST_COUNT.labels(request.url.path, response.status_code).inc()
    return response

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.post("/predict")
async def predict():
    start_time = time.time()

    # Our model prediction logic here
    predictions = ["yes", "no", "yes"]  # Example placeholder for model predictions
    
    # Track prediction metrics
    PREDICTION_LATENCY.labels("ml_model").observe(time.time() - start_time)
    MODEL_PREDICTIONS.labels("ml_model").inc(len(predictions))

    return {"predictions": predictions}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
```

In this example:
- **Operational metrics** are similar to those in the Flask app.
- **Functional metrics**:
  - `MODEL_PREDICTIONS` tracks how many predictions the model has made.
  - `PREDICTION_LATENCY` tracks how long it takes the model to make predictions.

## Step 2: Set up Prometheus to scrape metrics
Prometheus needs to be configured to scrape the `/metrics` endpoints of both Flask and FastAPI apps.

### 2.1 Configure Prometheus
Edit the `prometheus.yml` configuration file to include both Flask and FastAPI scrape jobs:
```yaml
  - job_name: 'flask_app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['localhost:5000']  # Flask app metrics

  - job_name: 'fastapi_app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['localhost:8000']  # FastAPI app metrics
```

### 2.2 Start Prometheus
Start Prometheus using the configuration file:
```bash
prometheus --config.file=prometheus.yml --web.enable-lifecycle
```

Prometheus will now begin scraping metrics from both the Flask and FastAPI applications.

## Step 3: Visualize metrics in Grafana
After Prometheus starts scraping metrics, we can visualize them using Grafana by creating dashboards for both operational and functional metrics.

### 3.1 Create dashboard panels for operational metrics
In Grafana, we can create panels to visualize operational metrics for both Flask and FastAPI apps.

- **Request latency for Flask**:
  ```promql
  histogram_quantile(0.95, sum(rate(flask_request_latency_seconds_bucket[5m])) by (le, endpoint))
  ```
  
- **Request count for FastAPI**:
  ```promql
  sum(rate(fastapi_request_count[5m])) by (endpoint)
  ```

### 3.2 Create dashboard panels for functional metrics (FastAPI only)
Create panels to monitor the ML model's behavior, such as prediction counts and latencies.

- **Total model predictions**:
  ```promql
  sum(model_predictions_total) by (model)
  ```

- **Prediction latency (p95)**:
  ```promql
  histogram_quantile(0.95, sum(rate(prediction_latency_seconds_bucket[5m])) by (le, model))
  ```

## Step 4: Set alerts for key metrics (Optional)
Optionally, we can configure alerts in either Prometheus or Grafana to trigger notifications if key metrics (like request latency or prediction errors) exceed a threshold.