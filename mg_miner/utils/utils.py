import os
import json
import yaml
import logging.config
from typing import Dict, Any
from dotenv import load_dotenv

def setup_logging(config_path: str, verbose: bool = False) -> None:
    """Sets up logging configuration."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    logging_config = config.get('logging', {})
    if verbose:
        for handler in logging_config['handlers'].values():
            handler['level'] = 'DEBUG'
        logging_config['root']['level'] = 'DEBUG'

    logging.config.dictConfig(logging_config)

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads a YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_data(data: Dict, file_path: str, format: str = 'json') -> None:
    """Saves data to a file in the specified format (json or yaml)."""
    with open(file_path, 'w') as f:
        if format == 'json':
            json.dump(data, f, indent=4)
        elif format == 'yaml':
            yaml.dump(data, f, default_flow_style=False)
        f.flush()
        os.fsync(f.fileno())

def ensure_dir_exists(directory: str) -> None:
    """Ensures that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def validate_config(config: Dict, required_fields: Dict[str, type]) -> bool:
    """Validates the configuration dictionary."""
    for field, field_type in required_fields.items():
        if field not in config:
            logging.error(f"Missing required field: {field}")
            return False
        if not isinstance(config[field], field_type):
            logging.error(f"Incorrect type for field {field}: expected {field_type}, got {type(config[field])}")
            return False
    return True

def safe_write_file(file_path: str, content
: str) -> None:
    """Safely writes content to a file, ensuring the directory exists and the file is synced to disk."""
    ensure_dir_exists(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
        logging.info(f"Wrote content to file: {file_path}")

def load_env() -> None:
    """Loads environment variables from a .env file."""
    load_dotenv()
