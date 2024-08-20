import yaml
from pathlib import Path

class Config:
    def __init__(self, default_config_path=None, custom_config_path=None):
        # Determine the path to the default_config.yaml relative to this module's location
        if default_config_path is None:
            default_config_path = Path(__file__).resolve().parent / 'default_config.yaml'
        
        # Load the default configuration
        self.config = self.load_config(default_config_path)
        
        # If a custom configuration path is provided, load and update the configuration
        if custom_config_path:
            self.update_config(custom_config_path)
        
        # Setup directories
        self.setup_directories()

    def load_config(self, config_path):
        """Load the configuration file."""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_path} not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {config_path}: {e}")

    def update_config(self, config_path):
        """Update the configuration with values from a custom config file."""
        try:
            with open(config_path, 'r') as file:
                custom_config = yaml.safe_load(file)
            self.config.update(custom_config)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_path} not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {config_path}: {e}")

    def get(self, key, default=None):
        """Retrieve a value from the configuration."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a value in the configuration."""
        self.config[key] = value

    def save_config(self, config_path):
        """Save the configuration to a file."""
        try:
            with open(config_path, 'w') as file:
                yaml.safe_dump(self.config, file)
        except Exception as e:
            raise Exception(f"Error saving configuration to file {config_path}: {e}")

    def setup_directories(self):
        """Set up the directory structure for outputs."""
        # Root directory for all outputs
        proj_root = Path.cwd() / 'churn_predictor_outputs'
        proj_root.mkdir(parents=True, exist_ok=True)

        # Define the directory paths
        data_dir = proj_root / 'data'
        processed_data_dir = data_dir / 'processed'
        models_dir = proj_root / 'models'
        reports_dir = proj_root / 'reports'
        figures_dir = reports_dir / 'figures'

        # Create the directories if they don't exist
        for directory in [data_dir, processed_data_dir, models_dir, reports_dir, figures_dir]:
            print(f"Creating directory: {directory}")  # Debug statement
            directory.mkdir(parents=True, exist_ok=True)

        # Store the paths in the configuration
        self.set('proj_root', str(proj_root))
        self.set('data_dir', str(data_dir))
        self.set('processed_data_dir', str(processed_data_dir))
        self.set('models_dir', str(models_dir))
        self.set('reports_dir', str(reports_dir))
        self.set('figures_dir', str(figures_dir))