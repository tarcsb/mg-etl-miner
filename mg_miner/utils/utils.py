import logging
import json
import os
import logging.config
from typing import Any, Dict

def setup_logging(config_path: str = None):
    """Sets up logging configuration."""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads a JSON configuration file."""
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def save_json(data: Dict[str, Any], path: str):
    """Saves a dictionary to a JSON file."""
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def validate_config(config: Dict[str, Any], required_fields: Dict[str, type]) -> bool:
    """Validates the configuration against required fields."""
    for field, field_type in required_fields.items():
        if field not in config:
            logging.error(f"Missing required field: {field}")
            return False
        if not isinstance(config[field], field_type):
            logging.error(f"Incorrect type for field {field}: expected {field_type}, got {type(config[field])}")
            return False
    return True

def ensure_dir_exists(path: str):
    """Ensures that a directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def safe_write_file(path: str, content: str):
    """Safely writes content to a file, ensuring the directory exists."""
    ensure_dir_exists(os.path.dirname(path))
    with open(path, 'w') as file:
        file.write(content)
        file.flush()
        os.fsync(file.fileno())
    logging.info(f"Wrote content to file: {path}")
