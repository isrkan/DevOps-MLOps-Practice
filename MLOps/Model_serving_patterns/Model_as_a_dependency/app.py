from flask import Flask, render_template, jsonify
from customer_churn_predictor import customer_churn_predictor, pipeline
from customer_churn_predictor.models import load_saved_model, predict_model
from customer_churn_predictor.data.load_data import load_data
from customer_churn_predictor.data.preprocess import preprocess_data
from customer_churn_predictor.features.build_features import feature_engineering
from customer_churn_predictor.data.split_data import perform_train_test_split
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Initialize the churn predictor
churn_predictor = customer_churn_predictor.CustomerChurnPredictor()
data_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
model_path = 'C:/Users/israe/Documents/Codes/PycharmProjects/customer_churn_predictor/models/saved_models/Logistic regression_model.pkl'

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
        # Load the saved model
        trained_model = load_saved_model.load_model(model_path)
        
        # Load and preprocess the data
        data = load_data(data_path)
        preprocessed_data = preprocess_data(data)
        processed_data = feature_engineering(preprocessed_data)
        
        # Split the data to get X_test
        _, X_test, _, _ = perform_train_test_split(processed_data, test_size=churn_predictor.config.get('test_size'),
                                                   random_state=churn_predictor.config.get('random_state'))
        
        # Make predictions using the loaded model
        predictions = predict_model.predict_models(trained_model, X_test)

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
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)