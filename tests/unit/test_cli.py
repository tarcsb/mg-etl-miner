import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from mg_miner.cli import cli

class TestCLI(unittest.TestCase):

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.load_config')
    def test_collect(self, mock_load_config, mock_file_collector):
        mock_load_config.return_value = {'root_dir': 'test_input', 'output_dir': 'test_output'}
        runner = CliRunner()
        result = runner.invoke(cli, ['collect'])
        self.assertEqual(result.exit_code, 0)
        mock_file_collector.from_config.assert_called_once()

    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.load_config')
    def test_detect(self, mock_load_config, mock_component_detector):
        mock_load_config.return_value = {'output_dir': 'test_output'}
        runner = CliRunner()
        result = runner.invoke(cli, ['detect'])
        self.assertEqual(result.exit_code, 0)
        mock_component_detector.return_value.detect_components.assert_called_once()

    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.load_config')
    def test_redact(self, mock_load_config, mock_redactor):
        mock_load_config.return_value = {'output_dir': 'test_output'}
        runner = CliRunner()
        result = runner.invoke(cli, ['redact'])
        self.assertEqual(result.exit_code, 0)
        mock_redactor.return_value.redact_sensitive_info.assert_called_once()

    @patch('mg_miner.cli.SummaryCreator')
    @patch('mg_miner.cli.load_config')
    def test_summary(self, mock_load_config, mock_summary_creator):
        mock_load_config.return_value = {'output_dir': 'test_output'}
        runner = CliRunner()
        result = runner.invoke(cli, ['summary'])
        self.assertEqual(result.exit_code, 0)
        mock_summary_creator.return_value.create_summary.assert_called_once()

    @patch('mg_miner.cli.time.sleep', return_value=None)
    def test_run_tasks(self, mock_sleep):
        runner = CliRunner()
        result = runner.invoke(cli, ['run_tasks'])
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()
