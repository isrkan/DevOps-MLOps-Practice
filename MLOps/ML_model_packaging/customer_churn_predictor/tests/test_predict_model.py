import unittest
from src.models.predict_model import predict_models
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.exceptions import NotFittedError

class TestPredictModel(unittest.TestCase):
    def test_predict_models(self):
        # Generate synthetic data for testing
        X_test, y_test = make_classification(n_samples=20, n_features=10, n_classes=2, random_state=42)

        # Define a trained logistic regression model
        model = LogisticRegression()
        model.fit(X_test, y_test)
        trained_models = {'Logistic regression': model}

        # Test the predict_models function
        predictions = predict_models(trained_models, X_test)

        # Check if predictions dictionary is not None
        self.assertIsNotNone(predictions)

        # Check if each prediction array has the correct length
        for model_name, prediction in predictions.items():
            self.assertEqual(len(prediction), len(X_test))

        # Test accessing an attribute of an unfitted model (for NotFittedError)
        unfitted_model = LogisticRegression()  # Create a new unfitted model instance
        with self.assertRaises(NotFittedError):
            unfitted_model.predict([[1] * 10])  # This should raise the NotFittedError


if __name__ == '__main__':
    unittest.main()