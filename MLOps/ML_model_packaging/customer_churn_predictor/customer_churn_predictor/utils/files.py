import pandas as pd


def read_csv(file_path):
    """
    Reads a CSV file and returns a DataFrame.

    Args:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The DataFrame containing the CSV data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def save_csv(data, file_path):
    """
    Saves a DataFrame to a CSV file.

    Args:
    - data (pd.DataFrame): The DataFrame to save.
    - file_path (str): The path to the CSV file.
    """
    try:
        data.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")