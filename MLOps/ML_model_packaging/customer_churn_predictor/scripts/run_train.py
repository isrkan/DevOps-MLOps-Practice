# run_train.py

from src.models.train_model import train_models
from src.config.config import Config


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
    config = Config(default_config_path='src/config/default_config.yaml',
                    custom_config_path='src/config/custom_config.yaml')

    # Run model training
    run_train(config)
