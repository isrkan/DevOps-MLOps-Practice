import unittest
from src.models.feature_importance import calculate_feature_importance
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

class TestFeatureImportance(unittest.TestCase):
    def test_calculate_feature_importance(self):
        # Generate synthetic data for testing
        X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)

        # Define and train a random forest classifier
        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)

        # Get feature names
        feature_names = [f'feature_{i}' for i in range(X.shape[1])]

        # Test the calculate_feature_importance function
        calculate_feature_importance(model, feature_names)

if __name__ == '__main__':
    unittest.main()