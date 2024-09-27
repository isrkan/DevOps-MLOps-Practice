from fastapi import FastAPI, HTTPException, Request
from customer_churn_predictor import customer_churn_predictor
from customer_churn_predictor.models import load_saved_model, predict_model
from customer_churn_predictor.data.load_data import load_data
from customer_churn_predictor.data.preprocess import preprocess_data
from customer_churn_predictor.features.build_features import feature_engineering
from customer_churn_predictor.data.split_data import perform_train_test_split
from prometheus_client import generate_latest, Counter, Histogram, Gauge
from starlette.responses import Response
import time

# Initialize the FastAPI app
app = FastAPI()

# Operational metrics
REQUEST_LATENCY = Histogram('fastapi_request_latency_seconds', 'Request latency', ['endpoint'])
REQUEST_COUNT = Counter('fastapi_request_count', 'Request count', ['endpoint', 'http_status'])

# Functional metrics (for the ML model)
MODEL_PREDICTIONS = Counter('model_predictions_total', 'Total number of model predictions', ['model'])
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of model predictions', ['model'])

# Initialize the churn predictor
churn_predictor = customer_churn_predictor.CustomerChurnPredictor()
# Define paths to data and model
data_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
model_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/models/saved_models/Logistic regression_model.pkl'

@app.middleware("http")
async def track_request_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(request.url.path).observe(latency)
    REQUEST_COUNT.labels(request.url.path, response.status_code).inc()
    return response

@app.get("/predict")
async def run_predict():
    try:
        start_time = time.time()

        # Load the model
        model = load_saved_model.load_model(model_path)

        # Load and preprocess the data
        data = load_data(data_path)
        preprocessed_data = preprocess_data(data)
        processed_data = feature_engineering(preprocessed_data)
        
        # Split the data to get X_test
        _, X_test, _, _ = perform_train_test_split(
            processed_data, 
            test_size=churn_predictor.config.get('test_size'),
            random_state=churn_predictor.config.get('random_state')
        )
        
        # Make predictions using the loaded model
        predictions = predict_model.predict_models(model, X_test)

        # Track prediction metrics
        PREDICTION_LATENCY.labels("ml_model").observe(time.time() - start_time)
        MODEL_PREDICTIONS.labels("ml_model").inc(len(predictions))

        # Ensure predictions are in a JSON-serializable format
        serializable_predictions = {}
        for model_name, pred in predictions.items():
            serializable_predictions[model_name] = pred.tolist() if hasattr(pred, 'tolist') else pred

        return {"predictions": serializable_predictions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type="text/plain")