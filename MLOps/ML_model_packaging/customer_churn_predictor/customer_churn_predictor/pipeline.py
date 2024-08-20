from customer_churn_predictor.data.load_data import load_data
from customer_churn_predictor.data.preprocess import preprocess_data
from customer_churn_predictor.visualization.visualize import visualize_categorical_distribution, visualize_numerical_distribution
from customer_churn_predictor.features.build_features import feature_engineering
from customer_churn_predictor.models.define_models import define_models
from customer_churn_predictor.models.train_model import train_models
from customer_churn_predictor.models.evaluate_model import evaluate_models
from customer_churn_predictor.data.split_data import perform_train_test_split
from customer_churn_predictor.models.feature_importance import calculate_feature_importance
from customer_churn_predictor.models.predict_model import predict_models
from customer_churn_predictor.models.model_serialization import save_model
from customer_churn_predictor.config.config import Config
import os
import logging

def run_pipeline(config, data_path):
    try:
        logging.info("Pipeline started.")

        # Load data
        data = load_data(data_path)

        # Visualize distributions (categorical and numerical)
        categorical_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
        numerical_features = ['tenure', 'MonthlyCharges']

        for feature in categorical_features:
            save_path = os.path.join(config.get('figures_dir'), f'{feature}_categorical_distribution.png')
            visualize_categorical_distribution(data, feature, save_path)

        for feature in numerical_features:
            save_path = os.path.join(config.get('figures_dir'), f'{feature}_numerical_distribution.png')
            visualize_numerical_distribution(data, feature, save_path)

        # Preprocess data
        preprocessed_data = preprocess_data(data)

        # Feature engineering
        processed_data = feature_engineering(preprocessed_data)


        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = perform_train_test_split(processed_data, test_size=config.get('test_size'),
                                                      random_state=config.get('random_state'))

        # Define models
        models = define_models()

        # Train model
        trained_models = train_models(models, X_train, y_train)

        # Evaluate model
        evaluate_models(trained_models, X_test, y_test)

        # Calculate and plot feature importance for each model
        for model_name, trained_model in trained_models.items():
            print(f"\nFeature importance for model: {model_name}")
            save_path = os.path.join(config.get('figures_dir'), f'{model_name}_feature_importance.png') # Define the path to save the plot
            calculate_feature_importance(trained_model, X_train.columns, save_path)

        # Make predictions using the trained models
        predictions = predict_models(trained_models, X_test)
        if predictions:
            for model_name, prediction in predictions.items():
                print(f"\nPredictions for model {model_name}: {prediction[:5]}")  # Print first 5 predictions as an example

        # Save models
        models_dir = config.get('models_dir')  # Directory to save models
        os.makedirs(models_dir, exist_ok=True)

        for model_name, trained_model in trained_models.items():
            # Construct a file path for each model
            model_filepath = os.path.join(config.get('models_dir'), f"{model_name}_model.pkl")
            save_model(trained_model, model_filepath)


        logging.info("Pipeline completed successfully.")
        print("Pipeline completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}")
        print(f"An error occurred during pipeline execution: {e}")