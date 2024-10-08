from sklearn.model_selection import train_test_split
import logging

def perform_train_test_split(data, test_size=0.2, random_state=42):
    """
    Splits the input data into training and testing sets.

    Parameters:
    - data (DataFrame): The processed dataset.
    - test_size (float): Proportion of the dataset to include in the test split.
    - random_state (int): Controls the shuffling applied to the data before applying the split.

    Returns:
    - X_train (DataFrame): Training features.
    - X_test (DataFrame): Testing features.
    - y_train (Series): Training target variable.
    - y_test (Series): Testing target variable.
    """
    try:
        logging.info("Performing train-test split with test_size=%s and random_state=%s", test_size, random_state)

        # Split the dataset into features (X) and target variable (y)
        X = data.drop(columns=['Churn_encoded'])  # Features
        y = data['Churn_encoded']  # Target variable
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        logging.info("Train-test split completed successfully.")
        return X_train, X_test, y_train, y_test
    except ValueError as ve:
        logging.error(f"ValueError occurred during train-test split: {ve}")
        print(f"ValueError occurred during train-test split: {ve}")
        return None, None, None, None
    except Exception as e:
        logging.error(f"An unexpected error occurred during train-test split: {e}")
        print(f"An unexpected error occurred during train-test split: {e}")
        return None, None, None, None