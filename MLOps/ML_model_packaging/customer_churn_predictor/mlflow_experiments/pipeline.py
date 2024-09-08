import sys
import os
# Add the root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mlflow
import mlflow.sklearn
import argparse
from customer_churn_predictor import customer_churn_predictor
from customer_churn_predictor.data.load_data import load_data
from customer_churn_predictor.data.preprocess import preprocess_data
from customer_churn_predictor.visualization.visualize import visualize_categorical_distribution, visualize_numerical_distribution
from customer_churn_predictor.features.build_features import feature_engineering
from customer_churn_predictor.models.define_models import define_models
from customer_churn_predictor.models.train_model import train_models
from customer_churn_predictor.models.evaluate_model import evaluate_models
from customer_churn_predictor.data.split_data import perform_train_test_split
from customer_churn_predictor.models.feature_importance import calculate_feature_importance
from customer_churn_predictor.config.config import Config
import logging

def run_pipeline(config, data_path):
    """
    Runs the full data pipeline including loading data, preprocessing, feature engineering,
    model training, evaluation, and saving the results.

    Parameters:
    - config (Config): Configuration object with pipeline settings.
    - data_path (str): Path to the dataset file.

    Returns:
    None
    """
    # Set the tracking URI to the MLflow server
    mlflow.set_tracking_uri(uri="")

    mlflow.set_experiment("Customer_Churn_Prediction")  # Set the experiment name

    # Start run
    with mlflow.start_run():
        try:
            logging.info("Pipeline started.")

            # Load data
            data = load_data(data_path)

            # Visualize distributions (categorical and numerical)
            categorical_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
            numerical_features = ['tenure', 'MonthlyCharges']

            for feature in categorical_features:
                save_path = os.path.join(config.get('figures_dir'), f'{feature}_categorical_distribution.png')
                fig = visualize_categorical_distribution(data, feature, save_path)
                mlflow.log_figure(fig, f'{feature}_categorical_distribution.png')  # Log the plot as an artifact

            for feature in numerical_features:
                save_path = os.path.join(config.get('figures_dir'), f'{feature}_numerical_distribution.png')
                fig = visualize_numerical_distribution(data, feature, save_path)
                mlflow.log_figure(fig, f'{feature}_numerical_distribution.png')  # Log the plot as an artifact

            # Preprocess data
            preprocessed_data = preprocess_data(data)

            # Feature engineering
            processed_data = feature_engineering(preprocessed_data)

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = perform_train_test_split(processed_data, test_size=config.get('test_size'),
                                                                        random_state=config.get('random_state'))
            mlflow.log_param("test_size", config.get('test_size'))
            mlflow.log_param("random_state", config.get('random_state'))

            # Define models
            models = define_models()

            # Train model
            trained_models = train_models(models, X_train, y_train)
            # Log the trained models as artifacts in MLflow
            for model_name, model in trained_models.items():
                mlflow.sklearn.log_model(model, model_name)
                logging.info(f"Model {model_name} logged as an artifact in MLflow.")
                print(f"Model {model_name} logged as an artifact in MLflow.")

            # Evaluate model and log metrics
            evaluation_results = evaluate_models(trained_models, X_test, y_test)
            for model_name, metrics in evaluation_results.items():
                # Log accuracy
                mlflow.log_metric(f"{model_name}_accuracy", metrics["accuracy"])

                # Save classification report and confusion matrix
                class_report_path = os.path.join(config.get('figures_dir'), f'{model_name}_classification_report.txt')
                conf_matrix_path = os.path.join(config.get('figures_dir'), f'{model_name}_confusion_matrix.txt')

                with open(class_report_path, 'w') as f:
                    f.write(str(metrics["classification_report"]))
                with open(conf_matrix_path, 'w') as f:
                    f.write(str(metrics["confusion_matrix"]))

                # Log classification report
                mlflow.log_artifact(class_report_path)
                # Log confusion matrix
                mlflow.log_artifact(conf_matrix_path)

            # Calculate and plot feature importance for each model
            for model_name, trained_model in trained_models.items():
                print(f"\nFeature importance for model: {model_name}")
                save_path = os.path.join(config.get('figures_dir'), f'{model_name}_feature_importance.png')  # Define the path to save the plot
                fig, feature_importance_df = calculate_feature_importance(trained_model, X_train.columns, save_path)
                if fig and feature_importance_df is not None:  # Check if feature importance was successfully calculated
                    mlflow.log_figure(fig, f'{model_name}_feature_importance.png') # Log the feature importance plot as an artifact

            logging.info("Pipeline completed successfully.")
            print("Pipeline completed successfully.")

        except Exception as e:
            logging.error(f"An error occurred during pipeline execution: {e}")
            print(f"An error occurred during pipeline execution: {e}")
            mlflow.log_param("error", str(e))  # Log the error

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run ML Pipeline with MLflow Tracking")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the dataset file")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test size for train-test split")
    parser.add_argument("--random_state", type=int, default=42, help="Random state for reproducibility")

    args = parser.parse_args()

    # Initialize the churn predictor
    churn_predictor = customer_churn_predictor.CustomerChurnPredictor()

    # Run the pipeline
    run_pipeline(churn_predictor.config, args.data_path)