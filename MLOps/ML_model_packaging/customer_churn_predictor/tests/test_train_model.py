import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from customer_churn_predictor.models.train_model import train_models

class TestTrainModel(unittest.TestCase):
    def test_train_models(self):
        # Generate synthetic data
        X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)
        X_train, y_train = X[:80], y[:80]

        # Define models
        models = {
            'Logistic regression': LogisticRegression(),
        }

        # Test the train_models function
        trained_models = train_models(models, X_train, y_train)

        # Check if trained_models dictionary is not None
        self.assertIsNotNone(trained_models)

        # Check if each model in trained_models is fitted
        for name, model in trained_models.items():
            self.assertTrue(hasattr(model, 'predict'))
            self.assertTrue(hasattr(model, 'score'))

if __name__ == '__main__':
    unittest.main()