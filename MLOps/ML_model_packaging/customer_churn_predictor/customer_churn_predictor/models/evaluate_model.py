from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import logging

def evaluate_models(trained_models, X_test, y_test):
    try:
        for name, model in trained_models.items():
            # Predict
            y_pred = model.predict(X_test)

            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            print(f'{name} Model accuracy: {accuracy:.2f}')
            logging.info(f'{name} Model accuracy: {accuracy:.2f}')

            print(f'Classification report for {name} model:')
            print(classification_report(y_test, y_pred))
            logging.info(f'Classification report for {name} model:\n{classification_report(y_test, y_pred)}')

            print(f'Confusion matrix for {name} model:')
            print(confusion_matrix(y_test, y_pred))
            logging.info(f'Confusion matrix for {name} model:\n{confusion_matrix(y_test, y_pred)}')

    except Exception as e:
        logging.error(f"An unexpected error occurred while evaluating models: {e}")
        print(f"An unexpected error occurred while evaluating models: {e}")