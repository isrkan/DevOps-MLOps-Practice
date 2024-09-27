# Monitoring ML models served via Flask with Prometheus

Monitoring a Flask app that serves an ML model helps ensure that both the app and the model perform as expected. This guide will cover how to monitor both **functional** (model performance) and **operational** (system health) aspects using Prometheus.

#### Prerequisites
Before starting, ensure the following are installed:
- **Flask app**: The web app used to serve the ML model.
- **Prometheus**: The monitoring tool for collecting and querying metrics.
- **Grafana**: For visualizing metrics collected by Prometheus.

## Step 1: Expose Prometheus metrics from Flask
To start monitoring, we first need to expose metrics from the Flask app for Prometheus to scrape.

#### 1.1 Install the Prometheus Client library
First, make sure we have the **Prometheus Python Client** installed:
```bash
pip install prometheus_client
```

#### 1.2 Modify the Flask app to expose metrics
In our Flask app, add a new route (`/metrics`) that will expose application metrics to Prometheus:
```python
from prometheus_client import generate_latest, Counter, Histogram, Gauge
from flask import Flask, Response, request
import time

app = Flask(__name__)

# Create some Prometheus metrics
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('flask_request_count', 'App Request Count', ['endpoint', 'http_status'])

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_request_data(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.path, response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

This code tracks request latency and request count for each endpoint, which Prometheus can scrape and monitor. Once the Flask app is running, we can verify that the metrics are exposed by visiting `http://localhost:5000/metrics` in our browser.


## Step 2: Monitor operational aspects
Operational metrics ensure the health of the Flask app, such as request latency, throughput, and system resources.

#### 2.1 Track request latency
Use **Histograms** to track the latency of requests for each endpoint:
```python
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])
```

#### 2.2 Track request count
Use **Counters** to count the number of requests made to each endpoint:
```python
REQUEST_COUNT = Counter('flask_request_count', 'App Request Count', ['endpoint', 'http_status'])

@app.after_request
def increment_request_count(response):
    REQUEST_COUNT.labels(request.path, response.status_code).inc()
    return response
```

## Step 3: Monitor functional aspects of the ML model
In addition to operational metrics, we need to monitor how the ML model behaves in production (e.g., predictions, accuracy, model drift).

#### 3.1 Track the number of model predictions
Use **Counters** to track how many predictions our model has made:
```python
MODEL_PREDICTIONS = Counter('model_predictions_total', 'Total number of model predictions', ['model'])

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        # Load the saved model and preprocess data...
        
        # Make predictions using the model
        predictions = predict_model.predict_models(trained_model, X_test)

        # Increment model predictions counter
        MODEL_PREDICTIONS.labels("logistic_regression").inc(len(predictions))

        # Return the results...
        return render_template('predict_results.html', plot_url=plot_url)
```

#### 3.2 Track prediction latency
Use **Histograms** to track how long it takes for the model to make predictions. In the `/predict` and `/pipeline` routes, track how long each request takes:
```python
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of model predictions', ['model'])

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        start_time = time.time()
        
        # Load model, preprocess data, and make predictions
        predictions = predict_model.predict_models(trained_model, X_test)

        # Measure latency and track it
        latency = time.time() - start_time
        PREDICTION_LATENCY.labels("logistic_regression").observe(latency)

        return render_template('predict_results.html', plot_url=plot_url)
```

#### 3.3 Track model accuracy (to detect model drift)
We will use Counters and Histograms to track the model’s performance metrics over time. First, we need to modify the `/predict` route to track the model's accuracy.
```python
MODEL_ACCURACY = Gauge('model_accuracy', 'Accuracy of the model over time', ['model'])

@app.route('/predict', methods=['GET'])
def run_predict():
    try:

        # Split the data to get X_test and y_test (labels)
        _, X_test, _, y_test = perform_train_test_split(processed_data, test_size=churn_predictor.config.get('test_size'),
                                                        random_state=churn_predictor.config.get('random_state'))

        # Rest of the code

        # Make predictions using the loaded model
        predictions = predict_model.predict_models(trained_model, X_test)

        # Calculate accuracy (or any other performance metric we want to track)
        accuracy = (predictions == y_test).mean()
        MODEL_ACCURACY.labels("logistic_regression").set(accuracy)

        # Render the template with the plot
        return render_template('predict_results.html', plot_url=plot_url)
```

#### 3.4 Monitor data distribution (to detect data drift)
Let’s track the mean and standard deviation of the `MonthlyCharges` feature (or any other key features) and compare it to historical data. We can use Histograms to track the distribution.
```python
MONTHLYCHARGES_MEAN = Gauge('monthly_charges_mean', 'Mean of Monthly Charges over time')
MONTHLYCHARGES_STDDEV = Gauge('monthly_charges_stddev', 'Standard deviation of Monthly Charges over time')

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        # Load and preprocess the data
        data = load_data(data_path)
        preprocessed_data = preprocess_data(data)

        # Calculate data statistics
        monthly_charges_mean = preprocessed_data['MonthlyCharges'].mean()
        monthly_charges_stddev = preprocessed_data['MonthlyCharges'].std()

        # Record these statistics
        MONTHLYCHARGES_MEAN.set(monthly_charges_mean)
        MONTHLYCHARGES_STDDEV.set(monthly_charges_stddev)

        return render_template('predict_results.html')
```

#### 3.5 Monitor prediction distribution (to detect prediction drift)
We can monitor the distribution of the predicted churn probabilities by tracking their mean and standard deviation.
```python
PREDICTION_MEAN = Gauge('prediction_mean', 'Mean of predicted churn probabilities')
PREDICTION_STDDEV = Gauge('prediction_stddev', 'Standard deviation of predicted churn probabilities')

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        # Make predictions using the model
        predictions = predict_model.predict_models(trained_model, X_test)

        # Calculate prediction statistics
        prediction_mean = predictions.mean()
        prediction_stddev = predictions.std()

        # Record these statistics
        PREDICTION_MEAN.set(prediction_mean)
        PREDICTION_STDDEV.set(prediction_stddev)

        return render_template('predict_results.html')
```

## Step 4: Set up Prometheus to scrape metrics
Prometheus needs to scrape the `/metrics` endpoint of our Flask app.

#### 4.1 Configure Prometheus
Edit the `prometheus.yml` configuration file to include our Flask app:
```yaml
scrape_configs:
  - job_name: 'flask_app'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['localhost:5000']  # Adjust this to the address of our Flask app
```

This tells Prometheus to scrape the `/metrics` endpoint of the Flask app running on `localhost:5000`.

#### 4.2 Start Prometheus
Run Prometheus from our installation directory:
```bash
prometheus --config.file=prometheus.yml --web.enable-lifecycle
```

## Step 5: Visualize metrics in Grafana
Once Prometheus is scraping our metrics, we can visualize them in Grafana. Create dashboards to visualize the key metrics:
- **Request latency**: Use the query `rate(flask_request_latency_seconds_bucket[5m])` to visualize the request latency histogram.
- **Prediction count**: Use the query `sum(model_predictions_total)` to track how many predictions our model has made.
- **Prediction latency**: Use `rate(prediction_latency_seconds_bucket[5m])` to view how long predictions are taking.

#### Example dashboard panels:
- **Panel 1**: "Request Latency per Endpoint" with query:
  ```bash
  histogram_quantile(0.95, sum(rate(flask_request_latency_seconds_bucket[5m])) by (le, endpoint))
  ```
  
- **Panel 2**: "Total Model Predictions" with query:
  ```bash
  sum(model_predictions_total) by (model)
  ```

- **Panel 3**: "Prediction Latency (p95)" with query:
  ```bash
  histogram_quantile(0.95, sum(rate(prediction_latency_seconds_bucket[5m])) by (le, model))
  ```

## Step 6: Set alerts for key metrics (Optional)
We can configure **Prometheus** or **Grafana** to send alerts if certain thresholds are crossed (e.g., high prediction latency or a spike in error rates). In **Prometheus**, we can define alert rules in the `prometheus.yml` file. In **Grafana**, we can set up alerts based on dashboard metrics.