from src.pipeline import run_pipeline
from src.config.config import Config

if __name__ == "__main__":
    # Load configuration
    config = Config(default_config_path='src/config/default_config.yaml',
                    custom_config_path='src/config/custom_config.yaml')

    # Run pipeline
    run_pipeline(config)