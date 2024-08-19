from src.data.load_data import load_data
from src.data.preprocess import preprocess_data
from src.models.train_model import train_models
from src.models.evaluate_model import evaluate_models
from src.data.split_data import perform_train_test_split
from src.config.config import Config

def run_pipeline(config):
    try:
        # Load data
        data = load_data(config.get('data_path'))

        # Preprocess data
        preprocessed_data = preprocess_data(data)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = perform_train_test_split(preprocessed_data, test_size=config.get('test_size'),
                                                      random_state=config.get('random_state'))

        # Train model
        model = train_models(X_train, y_train, config)

        # Evaluate model
        evaluate_models(model, X_test, y_test)

        print("Pipeline completed successfully.")

    except Exception as e:
        print(f"An error occurred during pipeline execution: {e}")


if __name__ == "__main__":
    # Load configuration
    config = Config(default_config_path='src/config/default_config.yaml',
                    custom_config_path='src/config/custom_config.yaml')

    # Run pipeline
    run_pipeline(config)
