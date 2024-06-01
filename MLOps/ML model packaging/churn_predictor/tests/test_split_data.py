import unittest
import pandas as pd
from src.data.split_data import perform_train_test_split

class TestTrainTestSplit(unittest.TestCase):
    def test_perform_train_test_split(self):
        # Create a sample DataFrame
        data = pd.DataFrame({
            'Feature1': [1, 2, 3, 4, 5],
            'Feature2': [6, 7, 8, 9, 10],
            'Churn_encoded': [0, 1, 0, 1, 0]
        })

        # Test the perform_train_test_split function
        X_train, X_test, y_train, y_test = perform_train_test_split(data, test_size=0.2, random_state=42)

        # Check if splits are not None
        self.assertIsNotNone(X_train)
        self.assertIsNotNone(X_test)
        self.assertIsNotNone(y_train)
        self.assertIsNotNone(y_test)

        # Check if splits are of correct lengths
        self.assertEqual(len(X_train), 4)
        self.assertEqual(len(X_test), 1)
        self.assertEqual(len(y_train), 4)
        self.assertEqual(len(y_test), 1)

if __name__ == '__main__':
    unittest.main()