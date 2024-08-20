import unittest
from customer_churn_predictor.features.build_features import feature_engineering
import pandas as pd

class TestFeatureEngineering(unittest.TestCase):
    def test_feature_engineering(self):
        # Create a sample DataFrame
        preprocessed_data = pd.DataFrame({
            'tenure': [12, 24],
            'MonthlyCharges': [50.0, 80.0]
        })

        # Test the feature_engineering function
        engineered_data = feature_engineering(preprocessed_data)
        self.assertIsNotNone(engineered_data)
        self.assertFalse(engineered_data.empty)

if __name__ == '__main__':
    unittest.main()