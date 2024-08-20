import joblib

def save_model(model, filepath):
    try:
        joblib.dump(model, filepath)
        print(f"Model saved successfully at {filepath}")

    except Exception as e:
        print(f"An unexpected error occurred while saving the model: {e}")

def load_model(filepath):
    try:
        model = joblib.load(filepath)
        print(f"Model loaded successfully from {filepath}")
        return model

    except Exception as e:
        print(f"An unexpected error occurred while loading the model: {e}")
        return None