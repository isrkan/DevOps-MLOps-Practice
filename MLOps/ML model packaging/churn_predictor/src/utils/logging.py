import logging


def setup_logging(log_file='app.log'):
    """
    Sets up logging for the application.

    Args:
    - log_file (str): The file to log messages to.
    """
    try:
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        print(f"Logging is set up. Logs will be saved to {log_file}")
    except Exception as e:
        print(f"Error setting up logging: {e}")