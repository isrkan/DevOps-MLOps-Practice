from customer_churn_predictor.config.config import Config


class CustomerChurnPredictor:
    def __init__(self, custom_config_path=None):
        """
        Initialize the CustomerChurnPredictor with configuration.
        
        Args:
        - custom_config_path (str): Path to the custom configuration file (optional).
        """
        self.config = Config(custom_config_path=custom_config_path)

    def get_config(self):
        """
        Retrieve the configuration object.
        """
        return self.config