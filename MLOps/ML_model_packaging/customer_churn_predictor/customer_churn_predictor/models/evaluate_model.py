from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

def evaluate_models(trained_models, X_test, y_test):
    """
    Evaluate trained machine learning models on the test data.

    Args:
    - trained_models (dict): A dictionary of trained models.
    - X_test (DataFrame): The test features.
    - y_test (Series): The true labels for the test data.

    Returns:
    - evaluation_results (dict): A dictionary containing the evaluation metrics for each model.
    """
    evaluation_results = {}

    try:
        for name, model in trained_models.items():
            # Predict
            y_pred = model.predict(X_test)

            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            class_report = classification_report(y_test, y_pred, output_dict=True)
            conf_matrix = confusion_matrix(y_test, y_pred)


            # Log to console and to logging
            print(f'{name} Model accuracy: {accuracy:.2f}')
            logging.info(f'{name} Model accuracy: {accuracy:.2f}')

            print(f'Classification report for {name} model:')
            print(classification_report(y_test, y_pred))
            logging.info(f'Classification report for {name} model:\n{classification_report(y_test, y_pred)}')

            print(f'Confusion matrix for {name} model:')
            print(confusion_matrix(y_test, y_pred))
            logging.info(f'Confusion matrix for {name} model:\n{confusion_matrix(y_test, y_pred)}')

            # Store metrics in the dictionary
            evaluation_results[name] = {
                "accuracy": accuracy,
                "classification_report": class_report,
                "confusion_matrix": conf_matrix
            }

            return evaluation_results
    except Exception as e:
        logging.error(f"An unexpected error occurred while evaluating models: {e}")
        print(f"An unexpected error occurred while evaluating models: {e}")