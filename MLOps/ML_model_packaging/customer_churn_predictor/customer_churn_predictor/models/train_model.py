from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import logging

def train_models(models, X_train, y_train):
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