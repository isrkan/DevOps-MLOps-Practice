from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import logging

def train_models(models, X_train, y_train):
    """
    Train a set of machine learning models on the provided training data.

    Args:
    - models (dict): A dictionary of model names and their corresponding untrained model instances.
    - X_train (DataFrame): The training features.
    - y_train (Series): The true labels for the training data.

    Returns:
    - trained_models (dict): A dictionary of model names and their corresponding trained model instances.
    """
    trained_models = {}
    try:
        for name, model in models.items():
            model.fit(X_train, y_train)
            trained_models[name] = model
            logging.info(f"Model {name} trained successfully.")
        return trained_models

    except Exception as e:
        logging.error(f"An unexpected error occurred while training models: {e}")
        print(f"An unexpected error occurred while training models: {e}")
        return None