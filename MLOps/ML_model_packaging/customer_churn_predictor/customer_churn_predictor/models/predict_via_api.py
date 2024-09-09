import pandas as pd
import requests
import logging

def predict_via_api(data, model_url):
    """
    Send data to an MLflow model serving endpoint and get predictions.

    Args:
    - data (pd.DataFrame or dict): The input data to send for prediction.
    - model_url (str): The HTTP address of the MLflow model serving endpoint.

    Returns:
    - predictions (dict): A dictionary with the predictions returned by the model.
    """

    if isinstance(data, pd.DataFrame):
        # Convert the DataFrame to a list of lists
        data = data.values.tolist()
    elif isinstance(data, dict):
        # Convert dict to a list of lists assuming it is a single record
        data = [list(data.values())]
    else:
        logging.error("Error: Data should be a dictionary or a pandas DataFrame.")
        print("Error: Data should be a dictionary or a pandas DataFrame.")
        return None

    # Prepare the payload for the request
    payload = {
        "inputs": data
    }

    try:
        # Send the POST request to the model's API endpoint
        response = requests.post(model_url, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            predictions = response.json()
            logging.info("Predictions received successfully.")
            print("Predictions received successfully.")
            return predictions
        else:
            logging.error(f"Error: Received unexpected status code {response.status_code}.")
            print(f"Error: Received unexpected status code {response.status_code}.")
            print(f"Response content: {response.content.decode()}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error: An exception occurred while making the API request: {e}")
        print(f"Error: An exception occurred while making the API request: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        return None