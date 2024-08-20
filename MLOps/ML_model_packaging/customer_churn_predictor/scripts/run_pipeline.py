from customer_churn_predictor.pipeline import run_pipeline
from customer_churn_predictor.config.config import Config

if __name__ == "__main__":
    # Load configuration
    config = Config(default_config_path='customer_churn_predictor/config/default_config.yaml',
                    custom_config_path='customer_churn_predictor/config/custom_config.yaml')

    # Run pipeline
    run_pipeline(config)