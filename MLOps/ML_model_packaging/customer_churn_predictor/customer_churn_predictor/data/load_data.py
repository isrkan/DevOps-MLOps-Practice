import pandas as pd
import logging

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully")
        logging.info("Data loaded successfully from %s", file_path)
        return data
    except FileNotFoundError:
        logging.error(f"File not found at path: {file_path}")
        print(f"File not found at path: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        logging.error("No data: File is empty")
        print("No data: File is empty")
        return None
    except pd.errors.ParserError:
        logging.error("Error parsing data")
        print("Error parsing data")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading data: {e}")
        return None