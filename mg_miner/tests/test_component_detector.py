# mg_miner/tests/test_component_detector.py

import unittest
from unittest.mock import patch, mock_open
import os
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.utils import ensure_dir_exists, save_json

class TestComponentDetector(unittest.TestCase):

    def setUp(self):
        self.output_dir = 'test_output'
        ensure_dir_exists(self.output_dir)
        
        # Create a mock config.json file
        self.config_path = os.path.join(self.output_dir, 'config.json')
        config_data = {
            "backend": ["*.py"],
            "frontend": ["*.js"],
            "testing_frameworks": ["test_*.py"]
        }
        save_json(config_data, self.config_path)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='{"backend": ["file1.py"], "frontend": ["file2.js"]}')
    def test_component_detector(self, mock_open, mock_os_walk):
        mock_os_walk.return_value = [
            (self.output_dir, ('subdir',), ('file1.py', 'file2.js'))
        ]
        detector = ComponentDetector(output_dir=self.output_dir, silent=True)
        detector.detect_components()
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'components.json')))

if __name__ == '__main__':
    unittest.main()
