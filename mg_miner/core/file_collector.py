import os
import logging
import shutil
import fnmatch
from typing import Dict, Any
from mg_miner.utils.utils import ensure_dir_exists, save_data, load_config, load_env
from mg_miner.utils.cloud import upload_to_aws, upload_to_gcp, upload_to_azure

class FileCollector:
    """Collects files from the root directory based on the provided configuration."""

    def __init__(self, root_dir: str, output_dir: str, config: Dict[str, Any], silent: bool = False) -> None:
        self.root_dir = root_dir
        self.output_dir = output_dir
        self.config = config
        self.silent = silent
        load_env()

    @classmethod
    def from_config(cls, config_path: str) -> "FileCollector":
        """Creates an instance of FileCollector from a config file."""
        config = load_config(config_path)
        return cls(config['root_dir'], config['output_dir'], config)

    def collect_files(self) -> None:
        """Collects files based on the configuration and saves them to the output directory."""
        logging.info("Collecting files...")
        ensure_dir_exists(self.output_dir)

        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if not self._is_excluded(file, root):
                    self._copy_file(file, root)

        if not self.silent:
            logging.info("File collection complete.")

        # Upload results to cloud storage
        self.upload_results()

    def _is_excluded(self, file: str, root: str) -> bool:
        """Determines if a file should be excluded based on the configuration."""
        for pattern in self.config.get('excluded_extensions', []):
            if fnmatch.fnmatch(file, pattern):
                return True
        for pattern in self.config.get('excluded_dirs', []):
            if fnmatch.fnmatch(root, pattern):
                return True
        return False

    def _copy_file(self, file: str, root: str) -> None:
        """Copies a file to the output directory."""
        src_path = os.path.join(root, file)
        dest_path = os.path.join(self.output_dir, os.path.relpath(src_path, self.root_dir))
        ensure_dir_exists(os.path.dirname(dest_path))
        shutil.copy2(src_path, dest_path)
        logging.info(f"Copied {src_path} to {dest_path}")

    def upload_results(self) -> None:
        """Uploads results to cloud storage."""
        logging.info("Uploading results to cloud storage...")

        # AWS
        aws_config = self.config.get('cloud', {}).get('aws', {})
        upload_to_aws(self.output_dir, aws_config)

        # GCP
        gcp_config = self.config.get('cloud', {}).get('gcp', {})
        upload_to_gcp(self.output_dir, gcp_config)

        # Azure
        azure_config = self.config.get('cloud', {}).get('azure', {})
        upload_to_azure(self.output_dir, azure_config)
