import argparse
from customer_churn_predictor import customer_churn_predictor
from customer_churn_predictor import pipeline
from customer_churn_predictor.models.train_model import train_models
from customer_churn_predictor.models.model_serialization import save_model
import os

def main():
    """
    Main function to train models for customer churn prediction.
    Parses command-line arguments for data path, configuration path, and models directory.
    """
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Train models for customer churn prediction.")
    parser.add_argument('--data_path', type=str, required=True, help="Path to the CSV data file.")
    parser.add_argument('--config_path', type=str, help="Optional path to a custom configuration file.")
    parser.add_argument('--models_dir', type=str, required=True, help="Directory to save the trained models.")

    # Parse arguments
    args = parser.parse_args()

    # Initialize the churn predictor with optional custom config path
    if args.config_path:
        churn_predictor = customer_churn_predictor.CustomerChurnPredictor(config_path=args.config_path)
    else:
        churn_predictor = customer_churn_predictor.CustomerChurnPredictor()

    # Run the pipeline up to the training step
    data = pipeline.load_data(args.data_path)
    preprocessed_data = pipeline.preprocess_data(data)
    processed_data = pipeline.feature_engineering(preprocessed_data)
    X_train, X_test, y_train, y_test = pipeline.perform_train_test_split(
        processed_data,
        test_size=churn_predictor.config.get('test_size'),
        random_state=churn_predictor.config.get('random_state')
    )

    # Define and train models
    models = pipeline.define_models()
    trained_models = train_models(models, X_train, y_train)

    # Ensure the directory for saving models exists
    os.makedirs(args.models_dir, exist_ok=True)

    # Save trained models
    for model_name, trained_model in trained_models.items():
        model_filepath = os.path.join(args.models_dir, f"{model_name}_model.pkl")
        save_model(trained_model, model_filepath)


    print("Model training completed successfully.")

if __name__ == "__main__":
    main()