import unittest
from src.models.define_models import define_models
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class TestModelDefinition(unittest.TestCase):
    def test_define_models(self):
        # Test the define_models function
        models = define_models()

        # Check if models dictionary is not None
        self.assertIsNotNone(models)

        # Check if each model is of the correct type
        self.assertIsInstance(models.get('Logistic regression'), LogisticRegression)
        self.assertIsInstance(models.get('Decision tree'), DecisionTreeClassifier)
        self.assertIsInstance(models.get('Random forest'), RandomForestClassifier)

        # Test accessing an attribute of an unfitted model (for NotFittedError)
        for model_name, model in models.items():
            with self.assertRaises(NotFittedError):
                model.predict([[1, 2]])


if __name__ == '__main__':
    unittest.main()