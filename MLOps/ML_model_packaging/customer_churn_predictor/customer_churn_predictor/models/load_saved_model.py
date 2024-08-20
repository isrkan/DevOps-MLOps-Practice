import joblib
import pandas as pd

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
        print(f"Model loaded successfully from {filepath}")
        return {'loaded_model': model}
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None
    except joblib.JobsLibException as e:
        print(f"Error loading the model from {filepath}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the model: {e}")
        return None