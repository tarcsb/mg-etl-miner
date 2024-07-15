import unittest
from unittest.mock import patch, mock_open
from mg_miner.core.redactor import Redactor

class TestRedactor(unittest.TestCase):

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open, read_data='Sensitive data: 123-45-6789')
    @patch('mg_miner.utils.utils.load_config')
    def test_redact_sensitive_info(self, mock_load_config, mock_open, mock_os_walk):
        mock_load_config.return_value = {
            "GDPR": ["\\d{3}-\\d{2}-\\d{4}"],
            "HIPAA": ["Sensitive data: \\d{3}-\\d{2}-\\d{4}"]
        }
        mock_os_walk.return_value = [
            ('/output', ('subdir',), ('file1.txt',))
        ]

        redactor = Redactor(output_dir='/output', compliance_standards=['GDPR', 'HIPAA'])
        redactor.redact_sensitive_info()

        mock_open.assert_any_call('/output/file1.txt', 'r')
        mock_open.assert_any_call('/output/file1.txt', 'w')

        handle = mock_open()
        handle.write.assert_called_once_with('Sensitive data: [REDACTED]')

if __name__ == '__main__':
    unittest.main()
