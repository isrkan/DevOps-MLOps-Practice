import yaml

class Config:
    def __init__(self, default_config_path='default_config.yaml', custom_config_path=None):
        self.config = self.load_config(default_config_path)
        if custom_config_path:
            self.update_config(custom_config_path)

    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_path} not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {config_path}: {e}")

    def update_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                custom_config = yaml.safe_load(file)
            self.config.update(custom_config)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_path} not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {config_path}: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def save_config(self, config_path):
        try:
            with open(config_path, 'w') as file:
                yaml.safe_dump(self.config, file)
        except Exception as e:
            raise Exception(f"Error saving configuration to file {config_path}: {e}")