from flask import Flask, render_template, jsonify, Response, request
from prometheus_client import generate_latest, Counter, Histogram, Gauge
from customer_churn_predictor import customer_churn_predictor, pipeline
from customer_churn_predictor.models import load_saved_model, predict_model
from customer_churn_predictor.data.load_data import load_data
from customer_churn_predictor.data.preprocess import preprocess_data
from customer_churn_predictor.features.build_features import feature_engineering
from customer_churn_predictor.data.split_data import perform_train_test_split
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)

# Initialize the churn predictor
churn_predictor = customer_churn_predictor.CustomerChurnPredictor()
data_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
model_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/models/saved_models/Logistic regression_model.pkl'

# Create some Prometheus metrics
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('flask_request_count', 'App Request Count', ['endpoint', 'http_status'])
MODEL_PREDICTIONS = Counter('model_predictions_total', 'Total number of model predictions', ['model'])
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of model predictions', ['model'])
MODEL_ACCURACY = Gauge('model_accuracy', 'Accuracy of the model over time', ['model'])
MONTHLYCHARGES_MEAN = Gauge('monthly_charges_mean', 'Mean of Monthly Charges over time')
MONTHLYCHARGES_STDDEV = Gauge('monthly_charges_stddev', 'Standard deviation of Monthly Charges over time')
PREDICTION_MEAN = Gauge('prediction_mean', 'Mean of predicted churn probabilities')
PREDICTION_STDDEV = Gauge('prediction_stddev', 'Standard deviation of predicted churn probabilities')

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_request_data(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(request_latency)
    REQUEST_COUNT.labels(request.path, response.status_code).inc()
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pipeline', methods=['GET'])
def run_pipeline():
    try:
        # Run the pipeline with the data
        pipeline.run_pipeline(churn_predictor.config, data_path=data_path)
        return render_template('pipeline_success.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['GET'])
def run_predict():
    try:
        start_time = time.time()

        # Load the saved model
        trained_model = load_saved_model.load_model(model_path)
        
        # Load and preprocess the data
        data = load_data(data_path)
        preprocessed_data = preprocess_data(data)

        # Calculate data statistics
        monthly_charges_mean = preprocessed_data['MonthlyCharges'].mean()
        monthly_charges_stddev = preprocessed_data['MonthlyCharges'].std()

        # Record these statistics
        MONTHLYCHARGES_MEAN.set(monthly_charges_mean)
        MONTHLYCHARGES_STDDEV.set(monthly_charges_stddev)

        processed_data = feature_engineering(preprocessed_data)
        
        # Split the data to get X_test
        _, X_test, _, y_test = perform_train_test_split(processed_data, test_size=churn_predictor.config.get('test_size'),
                                                   random_state=churn_predictor.config.get('random_state'))
        
        # Make predictions using the loaded model
        predictions = predict_model.predict_models(trained_model, X_test)

        # Extract the predictions for the "logistic_regression" model
        model_predictions = predictions['loaded_model']  # Extract predictions for the chosen model

        # Increment model predictions counter
        MODEL_PREDICTIONS.labels("logistic_regression").inc(len(predictions))

        # Calculate prediction statistics
        predictions_np = np.array(model_predictions)  # Convert to numpy array if not already
        prediction_mean = predictions_np.mean()
        prediction_stddev = predictions_np.std()

        # Record these statistics
        PREDICTION_MEAN.set(prediction_mean)
        PREDICTION_STDDEV.set(prediction_stddev)

        # Calculate accuracy (or other performance metric we want to track)
        accuracy = (predictions_np == y_test).mean()
        MODEL_ACCURACY.labels("logistic_regression").set(accuracy)

        # Measure latency and track it
        request_latency = time.time() - start_time
        PREDICTION_LATENCY.labels("logistic_regression").observe(request_latency)

        # Choose one model to plot
        model_name = list(predictions.keys())[0]
        model_predictions = predictions[model_name]

        # Generate the plot
        plt.figure(figsize=(10, 6))
        plt.scatter(X_test['MonthlyCharges'], model_predictions, alpha=0.5)
        plt.title(f'Predictions vs MonthlyCharges ({model_name})')
        plt.xlabel('MonthlyCharges')
        plt.ylabel('Predicted Churn')
        plt.grid(True)

        # Save the plot to a PNG image in memory
        # The image is not saved to a physical file anywhere on the filesystem. Instead, it exists only in memory during the execution of the route.
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