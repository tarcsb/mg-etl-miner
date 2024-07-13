# mg_miner/tests/test_mg_miner.py

import unittest
from unittest.mock import patch, mock_open
import os
from mg_miner.core.file_collector import FileCollector
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.core.summary_creator import SummaryCreator
from mg_miner.core.redactor import Redactor
from mg_miner.utils import ensure_dir_exists, save_json

class TestMGMiner(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_input'
        self.output_dir = 'test_output'
        ensure_dir_exists(self.test_dir)
        ensure_dir_exists(self.output_dir)
        
        # Create mock config.json file
        self.config_path = os.path.join(self.output_dir, 'config.json')
        config_data = {
            "backend": ["*.py"],
            "frontend": ["*.js"],
            "testing_frameworks": ["test_*.py"]
        }
        save_json(config_data, self.config_path)

    @patch('os.walk')
    def test_file_collector(self, mock_os_walk):
        mock_os_walk.return_value = [
            (self.test_dir, ('subdir',), ('file1.py', 'file2.log'))
        ]
        config = {
            "excluded_dirs": [],
            "excluded_extensions": ["*.log"]
        }
        file_collector = FileCollector(self.test_dir, self.output_dir, config, silent=True)
        file_collector.collect_files()
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'file1.py')))
        self.assertFalse(os.path.exists(os.path.join(self.output_dir, 'file2.log')))

    @patch('os.walk')
    def test_component_detector(self, mock_os_walk):
        mock_os_walk.return_value = [
            (self.output_dir, ('subdir',), ('file1.py', 'file2.js'))
        ]
        detector = ComponentDetector(output_dir=self.output_dir, silent=True)
        detector.detect_components()
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'components.json')))

    @patch('builtins.open', new_callable=mock_open, read_data='Sensitive data: 123-45-6789')
    @patch('os.walk')
    @patch('json.load')
    def test_redactor(self, mock_json_load, mock_os_walk, mock_open):
        mock_json_load.return_value = {
            "GDPR": [r'\d{3}-\d{2}-\d{4}'],
            "HIPAA": [r'Sensitive data: \d{3}-\d{2}-\d{4}']
        }
        mock_os_walk.return_value = [
            ('/output', ('subdir',), ('file1.txt',))
        ]
        redactor = Redactor(output_dir='/output', compliance_standards=['GDPR', 'HIPAA'])
        redactor.redact_sensitive_info()
        mock_open.assert_any_call('/output/file1.txt', 'r')

    def test_summary_creator(self):
        summary_creator = SummaryCreator(output_dir=self.output_dir, theme='default', silent=False)
        with self.assertRaises(FileNotFoundError):
            summary_creator.create_summary()

if __name__ == '__main__':
    unittest.main()
