import pandas as pd

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully")
        return data
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print("No data: File is empty")
        return None
    except pd.errors.ParserError:
        print("Error parsing data")
        return None