import joblib
import pandas as pd
import logging

def load_model(filepath):
    """
    Load a model from a pickle file.

    Args:
    - filepath (str): Path to the pickle file.

    Returns:
    - model: The loaded model.
    """
    try:
        model = joblib.load(filepath)
        logging.info(f"Model loaded successfully from {filepath}")
        print(f"Model loaded successfully from {filepath}")
        return {'loaded_model': model}
    except FileNotFoundError:
        logging.error(f"Error: The file {filepath} was not found.")
        print(f"Error: The file {filepath} was not found.")
        return None
    except joblib.JobsLibException as e:
        logging.error(f"Error loading the model from {filepath}: {e}")
        print(f"Error loading the model from {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading the model: {e}")
        print(f"An unexpected error occurred while loading the model: {e}")
        return None