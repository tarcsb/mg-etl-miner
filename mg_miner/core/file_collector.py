# mg_miner/core/file_collector.py

import os
import shutil
import fnmatch
import logging
from typing import List, Dict, Any
from mg_miner.utils import setup_logging, ensure_dir_exists, validate_config, load_config

class FileCollector:
    """Collects files from the input directory to the output directory, excluding specified patterns."""

    def __init__(self, input_dir: str, output_dir: str, exclude_dirs: List[str], exclude_extensions: List[str], silent: bool = False) -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.exclude_dirs = exclude_dirs
        self.exclude_extensions = exclude_extensions
        self.silent = silent

        # Setup logging
        setup_logging()

    def collect_files(self) -> None:
        """Collects files from input_dir to output_dir, excluding those that match exclude_patterns."""
        if not self.silent:
            logging.info(f"Collecting files from {self.input_dir} to {self.output_dir}")

        # Ensure the output directory exists
        ensure_dir_exists(self.output_dir)

        for root, dirs, files in os.walk(self.input_dir):
            # Exclude specified directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for file in files:
                if not self._is_excluded(file):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, self.input_dir)
                    dest_path = os.path.join(self.output_dir, rel_path)
                    ensure_dir_exists(os.path.dirname(dest_path))
                    shutil.copy2(src_path, dest_path)
                    if not self.silent:
                        logging.info(f"Copied {src_path} to {dest_path}")

    def _is_excluded(self, file_name: str) -> bool:
        """Checks if a file matches any of the exclude patterns or extensions."""
        if any(file_name.endswith(ext) for ext in self.exclude_extensions):
            if not self.silent:
                logging.info(f"Excluded file {file_name} due to extension")
            return True
        return False

    @classmethod
    def from_config(cls, config_path: str) -> 'FileCollector':
        """Creates an instance of FileCollector from a configuration file."""
        config = load_config(config_path)

        required_fields = {
            "input_dir": str,
            "output_dir": str,
            "excluded_dirs": list,
            "excluded_extensions": list,
            "silent": bool
        }

        if not validate_config(config, required_fields):
            raise ValueError("Invalid configuration")

        return cls(
            input_dir=config["input_dir"],
            output_dir=config["output_dir"],
            exclude_dirs=config["excluded_dirs"],
            exclude_extensions=config["excluded_extensions"],
            silent=config["silent"]
        )
