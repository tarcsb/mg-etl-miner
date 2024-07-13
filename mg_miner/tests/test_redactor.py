import unittest
from unittest.mock import patch, mock_open
from mg_miner.core.redactor import Redactor

class TestRedactor(unittest.TestCase):
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='Sensitive data: 123-45-6789')
    @patch('json.load')
    def test_redact_sensitive_info(self, mock_json_load, mock_open, mock_os_walk):
        # Mock the JSON patterns
        mock_json_load.return_value = {
            "GDPR": [r'\d{3}-\d{2}-\d{4}'],
            "HIPAA": [r'Sensitive data: \d{3}-\d{2}-\d{4}']
        }

        mock_os_walk.return_value = [
            ('/output', ('subdir',), ('file1.txt',))
        ]

        redactor = Redactor(output_dir='/output', compliance_standards=['GDPR', 'HIPAA'])
        redactor.redact_sensitive_info()

        # Check that the file was read and written correctly
        mock_open.assert_any_call('/output/file1.txt', 'r')
        mock_open.assert_any_call('/output/file1.txt', 'w')

        # Check the write operation contains the redacted data
        handle = mock_open()
        handle.write.assert_called_once_with('Sensitive data: [REDACTED]')

if __name__ == '__main__':
    unittest.main()
