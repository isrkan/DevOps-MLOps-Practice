import logging

def predict_models(trained_models, X_test):
    predictions = {}
    try:
        for name, model in trained_models.items():
            predictions[name] = model.predict(X_test)
        logging.info("Predictions made successfully for all models.")
        return predictions

    except Exception as e:
        logging.error(f"An unexpected error occurred while making predictions: {e}")
        print(f"An unexpected error occurred while making predictions: {e}")
        return None