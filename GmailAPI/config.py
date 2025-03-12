import json
import os

# Define the path to your config file
current_working_directory = os.getcwd()
CONFIG_FILE_PATH = os.path.join(current_working_directory + '/configs/app_config.json')

class Config:
    def __init__(self):
        # Load the configuration data when the object is instantiated
        self.config_data = self.load_config()

    def load_config(self):
        # Load the config data from the file
        try:
            with open(CONFIG_FILE_PATH, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {CONFIG_FILE_PATH}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {CONFIG_FILE_PATH}")
            raise

    def get(self, key, default=None):
        # Retrieve a value from the config data, return default if key is not found
        return self.config_data.get(key, default)

# Instantiate the config object once
config = Config()
