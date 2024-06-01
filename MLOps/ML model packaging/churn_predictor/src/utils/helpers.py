import numpy as np

def handle_missing_values(data):
    """
    Handle missing values in the dataset by filling with median for numerical columns.

    Args:
    - data (pd.DataFrame): Input DataFrame with potential missing values.

    Returns:
    - pd.DataFrame: DataFrame with missing values handled.
    """
    try:
        numerical_cols = data.select_dtypes(include=np.number).columns
        data[numerical_cols] = data[numerical_cols].fillna(data[numerical_cols].median())
        return data
    except Exception as e:
        print(f"Error handling missing values: {e}")
        return data

def calculate_class_distribution(data):
    """
    Calculate and print the class distribution of the target variable.

    Args:
    - data (pd.DataFrame): Input DataFrame.

    Returns:
    - None
    """
    try:
        class_counts = data['Churn'].value_counts()
        print("Class distribution:")
        print(class_counts)
    except KeyError as e:
        print(f"Error: {e}. Ensure that the 'Churn' column exists in the dataset.")