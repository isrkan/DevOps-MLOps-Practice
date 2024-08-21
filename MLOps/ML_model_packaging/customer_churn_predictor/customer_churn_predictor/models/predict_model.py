import logging

def predict_models(trained_models, X_test):
    """
    Generate predictions using trained machine learning models.

    Args:
    - trained_models (dict): A dictionary of trained models.
    - X_test (DataFrame): The test features to make predictions on.

    Returns:
    - predictions (dict): A dictionary where keys are model names and values are the corresponding predictions.
    """
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