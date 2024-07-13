import unittest
from unittest.mock import patch
import mg_miner.cli as cli
import sys

class TestCLI(unittest.TestCase):

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.SummaryCreator')
    def test_collect_command(self, MockSummaryCreator, MockRedactor, MockComponentDetector, MockFileCollector):
        testargs = ["prog", "collect", "config.json"]
        with patch.object(sys, 'argv', testargs):
            cli.main()
            MockFileCollector.from_config.assert_called_once_with("config.json")
            MockFileCollector.from_config().collect_files.assert_called_once()

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.SummaryCreator')
    def test_detect_command(self, MockSummaryCreator, MockRedactor, MockComponentDetector, MockFileCollector):
        testargs = ["prog", "detect", "/path/to/output"]
        with patch.object(sys, 'argv', testargs):
            cli.main()
            MockComponentDetector.assert_called_once_with(output_dir="/path/to/output", silent=False)
            MockComponentDetector().detect_components.assert_called_once()

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.SummaryCreator')
    def test_redact_command(self, MockSummaryCreator, MockRedactor, MockComponentDetector, MockFileCollector):
        testargs = ["prog", "redact", "/path/to/output", "GDPR", "HIPAA"]
        with patch.object(sys, 'argv', testargs):
            cli.main()
            MockRedactor.assert_called_once_with(output_dir="/path/to/output", compliance_standards=["GDPR", "HIPAA"], silent=False)
            MockRedactor().redact_sensitive_info.assert_called_once()

    @patch('mg_miner.cli.FileCollector')
    @patch('mg_miner.cli.ComponentDetector')
    @patch('mg_miner.cli.Redactor')
    @patch('mg_miner.cli.SummaryCreator')
    def test_summary_command(self, MockSummaryCreator, MockRedactor, MockComponentDetector, MockFileCollector):
        testargs = ["prog", "summary", "/path/to/output", "dark"]
        with patch.object(sys, 'argv', testargs):
            cli.main()
            MockSummaryCreator.assert_called_once_with(output_dir="/path/to/output", silent=False, theme="dark")
            MockSummaryCreator().create_summary.assert_called_once()

if __name__ == '__main__':
    unittest.main()
