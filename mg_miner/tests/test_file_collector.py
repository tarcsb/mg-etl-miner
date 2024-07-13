# mg_miner/tests/test_file_collector.py

import unittest
from unittest.mock import patch, mock_open
import os
from mg_miner.core.file_collector import FileCollector
from mg_miner.utils import ensure_dir_exists, save_json

class TestFileCollector(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_input'
        self.output_dir = 'test_output'
        ensure_dir_exists(self.test_dir)
        ensure_dir_exists(self.output_dir)
        
        self.config = {
            "excluded_dirs": [],
            "excluded_extensions": ["*.log"]
        }

    @patch('os.walk')
    def test_collect_files(self, mock_os_walk):
        mock_os_walk.return_value = [
            (self.test_dir, ('subdir',), ('file1.py', 'file2.log'))
        ]
        file_collector = FileCollector(self.test_dir, self.output_dir, self.config, silent=True)
        file_collector.collect_files()
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'file1.py')))
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, 'file2.log')))

if __name__ == '__main__':
    unittest.main()
