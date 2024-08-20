from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import logging

def define_models():
    try:
        models = {
            'Logistic regression': LogisticRegression(),
            'Decision tree': DecisionTreeClassifier(),
            'Random forest': RandomForestClassifier()
        }
        logging.info("Models defined successfully.")
        return models
    except Exception as e:
        logging.error(f"An unexpected error occurred while defining models: {e}")
        print(f"An unexpected error occurred while defining models: {e}")
        return None