import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from mg_miner.cli import main

class TestIntegration(unittest.TestCase):

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.SummaryCreator')
    @patch('mg_miner.cli.load_config')
    def test_integration(self, mock_load_config, mock_summary_creator, mock_redactor, mock_component_detector, mock_file_collector):
        mock_load_config.return_value = {
            'root_dir': 'test_input',
            'output_dir': 'test_output'
        }

        runner = CliRunner()
        result = runner.invoke(main, ['--config', 'configs/config.json'])

        self.assertEqual(result.exit_code, 0)
        mock_file_collector.from_config.assert_called_once()
        mock_component_detector.return_value.detect_components.assert_called_once()
        mock_redactor.return_value.redact_sensitive_info.assert_called_once()
        mock_summary_creator.return_value.create_summary.assert_called_once()

if __name__ == '__main__':
    unittest.main()
