import unittest
from unittest.mock import patch, mock_open
import os
import shutil
from mg_miner.core.file_collector import FileCollector
from mg_miner.utils.utils import ensure_dir_exists, save_data, load_config

class TestFileCollector(unittest.TestCase):

    def setUp(self):
       
        self.test_dir = 'test_input'
        self.output_dir = 'test_output'
        ensure_dir_exists(self.test_dir)
        ensure_dir_exists(self.output_dir)

        self.config_path = os.path.join(self.output_dir, 'config.yaml')
        config_data = {
            "root_dir": self.test_dir,
            "output_dir": self.output_dir,
            "excluded_dirs": [],
            "excluded_extensions": ["*.log"],
            "cloud": {
                "aws": {
                    "access_key_id": "fake_access_key",
                    "secret_access_key": "fake_secret_key",
                    "region": "us-east-1",
                    "bucket_name": "test_bucket"
                },
                "gcp": {
                    "project_id": "fake_project_id",
                    "credentials": "fake_credentials.json",
                    "bucket_name": "test_bucket"
                },
                "azure": {
                    "connection_string": "fake_connection_string",
                    "container_name": "test_container"
                }
            }
        }
        save_data(config_data, self.config_path, format='yaml')

    @patch('os.walk')
    @patch('shutil.copy2')
    @patch('mg_miner.utils.cloud.upload_to_aws')
    @patch('mg_miner.utils.cloud.upload_to_gcp')
    @patch('mg_miner.utils.cloud.upload_to_azure')
    def test_collect_files(self, mock_azure_upload, mock_gcp_upload, mock_aws_upload, mock_copy, mock_os_walk):
        mock_os_walk.return_value = [
            (self.test_dir, ('subdir',), ('file1.py', 'file2.log'))
        ]
        config = load_config(self.config_path)
        file_collector = FileCollector(self.test_dir, self.output_dir, config, silent=True)
        file_collector.collect_files()

        mock_copy.assert_called_once_with(os.path.join(self.test_dir, 'file1.py'), os.path.join(self.output_dir, 'file1.py'))
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, 'file2.log')))
        mock_aws_upload.assert_called_once()
        mock_gcp_upload.assert_called_once()
        mock_azure_upload.assert_called_once()

if __name__ == '__main__':
    unittest.main()
