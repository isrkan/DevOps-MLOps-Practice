from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def train_models(models, X_train, y_train):
    trained_models = {}
    try:
        for name, model in models.items():
            model.fit(X_train, y_train)
            trained_models[name] = model
        return trained_models

    except Exception as e:
        print(f"An unexpected error occurred while training models: {e}")
        return None