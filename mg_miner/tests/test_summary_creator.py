# mg_miner/tests/test_summary_creator.py

import unittest
from unittest.mock import patch, mock_open
import os
from mg_miner.core.summary_creator import SummaryCreator
from mg_miner.utils import ensure_dir_exists, save_json

class TestSummaryCreator(unittest.TestCase):

    def setUp(self):
        self.output_dir = 'test_output'
        ensure_dir_exists(self.output_dir)
        
        # Create a mock components.json file
        self.components_path = os.path.join(self.output_dir, 'components.json')
        components_data = {
            "backend": ["file1.py"],
            "frontend": ["file2.js"]
        }
        save_json(components_data, self.components_path)

    @patch('builtins.open', new_callable=mock_open, read_data='{"backend": ["file1.py"], "frontend": ["file2.js"]}')
    @patch('os.path.exists')
    @patch('mg_miner.core.summary_creator.ensure_dir_exists')
    def test_create_summary(self, mock_ensure_dir_exists, mock_exists, mock_open):
        mock_exists.return_value = True
        summary_creator = SummaryCreator(output_dir='output', theme='default', silent=False)
        summary_creator.create_summary()
        mock_open.assert_any_call('output/components.json', 'r')

    @patch('builtins.open', new_callable=mock_open, read_data='{"backend": ["file1.py"], "frontend": ["file2.js"]}')
    @patch('os.path.exists')
    def test_create_summary_file_not_found(self, mock_exists, mock_open):
        mock_exists.return_value = False
        summary_creator = SummaryCreator(output_dir='output', theme='default', silent=False)
        with self.assertRaises(FileNotFoundError):
            summary_creator.create_summary()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_save_summary(self, mock_makedirs, mock_open):
        summary_creator = SummaryCreator(output_dir='output', theme='default', silent=False)
        summary_creator.save_summary('Summary content', 'output/summary.txt')
        mock_makedirs.assert_called_once_with('output', exist_ok=True)
        mock_open.assert_any_call('output/summary.txt', 'w')
        mock_open().write.assert_called_once_with('Summary content')

if __name__ == '__main__':
    unittest.main()
