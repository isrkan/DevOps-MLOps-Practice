# run_train.py

from customer_churn_predictor.models.train_model import train_models
from customer_churn_predictor.config.config import Config


def run_train(config):
    try:
        # Train model
        model = train_models(config)

        # Save trained model
        model.save_model(config.get('model_path'))

        print("Model training completed successfully.")

    except Exception as e:
        print(f"An error occurred during model training: {e}")


if __name__ == "__main__":
    # Load configuration
    config = Config(default_config_path='customer_churn_predictor/config/default_config.yaml',
                    custom_config_path='customer_churn_predictor/config/custom_config.yaml')

    # Run model training
    run_train(config)
