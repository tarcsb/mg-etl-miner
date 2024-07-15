import os
import json
import logging
import unittest
from unittest.mock import patch, mock_open, MagicMock
from mg_miner.utils.utils import (
    setup_logging,
    load_config,
    save_json,
    validate_config,
    ensure_dir_exists,
    safe_write_file
)

class TestUtils(unittest.TestCase):

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"version": 1}')
    @patch("logging.config.dictConfig")
    def test_setup_logging_with_config(self, mock_dict_config, mock_open, mock_exists):
        mock_exists.return_value = True
        setup_logging(config_path="fake_path")
        mock_open.assert_called_once_with("fake_path", "r")
        mock_dict_config.assert_called_once()

    @patch("logging.basicConfig")
    def test_setup_logging_without_config(self, mock_basic_config):
        setup_logging(config_path=None)
        mock_basic_config.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_config(self, mock_open):
        result = load_config("fake_path")
        mock_open.assert_called_once_with("fake_path", "r")
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", new_callable=mock_open)
    def test_save_json(self, mock_open):
        data = {"key": "value"}
        save_json(data, "fake_path")
        mock_open.assert_called_once_with("fake_path", "w")
        written_data = "".join(call[0][0] for call in mock_open().write.call_args_list)
        expected_data = json.dumps(data, indent=4)
        self.assertEqual(written_data, expected_data)

    def test_validate_config(self):
        config = {"field1": "value1", "field2": 2}
        required_fields = {"field1": str, "field2": int}
        self.assertTrue(validate_config(config, required_fields))

        config_missing_field = {"field1": "value1"}
        self.assertFalse(validate_config(config_missing_field, required_fields))

        config_wrong_type = {"field1": "value1", "field2": "wrong_type"}
        self.assertFalse(validate_config(config_wrong_type, required_fields))

    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    def test_ensure_dir_exists(self, mock_exists, mock_makedirs):
        ensure_dir_exists("fake_dir")
        mock_exists.assert_called_once_with("fake_dir")
        mock_makedirs.assert_called_once_with("fake_dir")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.fsync")
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    def test_safe_write_file(self, mock_makedirs, mock_exists, mock_fsync, mock_open):
        safe_write_file("fake_path/fake_file.txt", "content")
        mock_exists.assert_called_once_with("fake_path")
        mock_makedirs.assert_called_once_with("fake_path")
        mock_open.assert_called_once_with("fake_path/fake_file.txt", "w")
        mock_open().write.assert_called_once_with("content")
        mock_fsync.assert_called_once_with(mock_open().fileno())

if __name__ == "__main__":
    unittest.main()
