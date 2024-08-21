import joblib
import logging

def save_model(model, filepath):
    """
    Save a trained model to a specified file path using joblib.

    Args:
    - model: The trained model to be saved.
    - filepath (str): The path where the model will be saved.

    Returns:
    - None
    """
    try:
        joblib.dump(model, filepath)
        logging.info(f"Model saved successfully at {filepath}")
        print(f"Model saved successfully at {filepath}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving the model: {e}")
        print(f"An unexpected error occurred while saving the model: {e}")

def load_model(filepath):
    """
    Load a trained model from a specified file path using joblib.

    Args:
    - filepath (str): The path to the saved model file.

    Returns:
    - model: The loaded model.
    """
    try:
        model = joblib.load(filepath)
        logging.info(f"Model loaded successfully from {filepath}")
        print(f"Model loaded successfully from {filepath}")
        return model
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading the model: {e}")
        print(f"An unexpected error occurred while loading the model: {e}")
        return None