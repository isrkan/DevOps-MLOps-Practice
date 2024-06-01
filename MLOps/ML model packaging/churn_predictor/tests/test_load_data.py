import unittest
from src.data.load_data import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        # Test with the correct path
        data = load_data('../data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

        # Test with incorrect path
        data = load_data('wrong/path/to/file.csv')
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()