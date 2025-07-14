import os
import json
from pathlib import Path

# Define the application name for creating a dedicated config directory
APP_NAME = "AlzheimerMemoryAssistant"

# Determine the user's config directory based on the OS
if os.name == 'nt':  # Windows
    config_dir = Path(os.getenv('APPDATA')) / APP_NAME
else:  # Linux, macOS, etc.
    config_dir = Path.home() / '.config' / APP_NAME

# Define the root directory of the project
# This assumes settings.py is in src/config/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings:
    """Application configuration settings"""

    def __init__(self, config_path=None):
        """
        Initializes the Settings object.

        Args:
            config_path (str, optional): Path to the config file.
                                         Defaults to a user-specific directory.
        """
        if config_path:
            self.config_file = Path(config_path)
        else:
            self.config_file = config_dir / 'config.json'

        self.config = {}
        self.load_config()

    def _create_default_config(self):
        """Creates a default configuration dictionary."""
        return {
            "paths": {
                "data_directory": str(PROJECT_ROOT / 'data' / 'user_data'),
                "ai_model_directory": str(PROJECT_ROOT / 'models'),
                "log_file": str(config_dir / 'app.log')
            },
            "accessibility": {
                "font_size": 14,
                "high_contrast_mode": False
            },
            "logging": {
                "level": "INFO"
            }
        }

    def load_config(self):
        """
        Loads configuration from the JSON file.
        If the file doesn't exist, it creates a default one.
        """
        if not self.config_file.exists():
            print(f"Config file not found. Creating default config at {self.config_file}")
            self.config = self._create_default_config()
            self.save_config()
        else:
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}. Using default settings.")
                self.config = self._create_default_config()

    def save_config(self):
        """Saves the current configuration to the JSON file."""
        try:
            # Ensure the directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config file: {e}")

    def get(self, key, default=None):
        """Retrieves a value from the config, using dot notation for nested keys."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key, value):
        """Sets a value in the config, using dot notation for nested keys."""
        keys = key.split('.')
        d = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
        self.save_config()

    def get_ai_model_path(self):
        """Get path to AI model files"""
        return self.get('paths.ai_model_directory')

    def get_data_directory(self):
        """Get data storage directory"""
        return self.get('paths.data_directory')

    def get_accessibility_settings(self):
        """Get accessibility configuration"""
        return self.get('accessibility', {})
