def predict_models(trained_models, X_test):
    predictions = {}
    try:
        for name, model in trained_models.items():
            predictions[name] = model.predict(X_test)
        return predictions

    except Exception as e:
        print(f"An unexpected error occurred while making predictions: {e}")
        return None