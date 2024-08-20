import logging
import os

def setup_logging(proj_root, log_file_name='logging_file.log'):
    """
    Sets up logging for the project.

    Args:
    - proj_root (str): The root directory of the project.
    - log_file_name (str): The name of the log file.
    """
    try:
        # Ensure the logs directory exists within the project root
        log_dir = os.path.join(proj_root, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Define the log file path
        log_file_path = os.path.join(log_dir, log_file_name)

        # Configure logging settings
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f"Logging setup complete. Logs will be saved to {log_file_path}")
        print(f"Logging is set up. Logs will be saved to {log_file_path}")
    except Exception as e:
        print(f"Error setting up logging: {e}")
        logging.error(f"Failed to set up logging: {e}")