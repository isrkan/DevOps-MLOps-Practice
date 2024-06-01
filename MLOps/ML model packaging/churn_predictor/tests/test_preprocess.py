import unittest
from src.data.preprocess import preprocess_data
import pandas as pd

class TestDataPreprocess(unittest.TestCase):
    def test_preprocess_data(self):
        # Create a sample DataFrame
        data = pd.DataFrame({
            'gender': ['Male', 'Female'],
            'Partner': ['Yes', 'No'],
            'Dependents': ['Yes', 'No'],
            'PhoneService': ['Yes', 'No'],
            'PaperlessBilling': ['Yes', 'No'],
            'MultipleLines': ['No', 'Yes'],
            'InternetService': ['DSL', 'Fiber optic'],
            'OnlineSecurity': ['No', 'Yes'],
            'OnlineBackup': ['Yes', 'No'],
            'DeviceProtection': ['No', 'Yes'],
            'TechSupport': ['No', 'Yes'],
            'StreamingTV': ['No', 'Yes'],
            'StreamingMovies': ['Yes', 'No'],
            'Contract': ['Month-to-month', 'Two year'],
            'PaymentMethod': ['Electronic check', 'Mailed check'],
            'tenure': [12, 24],
            'MonthlyCharges': [50.0, 80.0],
            'TotalCharges': [600.0, 1920.0],
            'Churn': ['Yes', 'No']
        })

        # Test the preprocess_data function
        preprocessed_data = preprocess_data(data)
        self.assertIsNotNone(preprocessed_data)
        self.assertFalse(preprocessed_data.empty)

if __name__ == '__main__':
    unittest.main()