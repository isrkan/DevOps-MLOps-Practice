from flask import Flask, render_template, jsonify, request, Response
from prometheus_client import generate_latest, Counter, Histogram
import requests
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)

# Prometheus metrics
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('flask_request_count', 'Request Count', ['endpoint', 'http_status'])

# FastAPI service URL
fastapi_url = 'http://127.0.0.1:8000/predict'

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_metrics(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.path, response.status_code).inc()
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        # Send a GET request to the FastAPI model service
        response = requests.get(fastapi_url)

        # Handle errors in the response
        if response.status_code != 200:
            return jsonify({"error": "Failed to get prediction from FastAPI service"}), response.status_code

        # Get the predictions from the response
        predictions = response.json().get('predictions')

        if not predictions:
            return jsonify({"error": "No predictions found"}), 500

        # Choose one model to plot
        model_name = list(predictions.keys())[0]
        model_predictions = predictions[model_name]

        # Generate the plot
        plt.figure(figsize=(10, 6))
        plt.scatter(range(len(model_predictions)), model_predictions, alpha=0.5)
        plt.title(f'Predicted Churn')
        plt.xlabel('Sample Index')
        plt.ylabel('Predicted Churn')
        plt.grid(True)

        # Save the plot to a PNG image in memory
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Render the template with the plot
        return render_template('predict_results.html', plot_url=plot_url)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True, port=5000)