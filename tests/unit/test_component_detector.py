import unittest
from unittest.mock import patch, MagicMock
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.utils.utils import ensure_dir_exists, save_data, load_config

class TestComponentDetector(unittest.TestCase):

    def setUp(self):
        self.output_dir = 'test_output'
        ensure_dir_exists(self.output_dir)

        self.config_path = os.path.join(self.output_dir, 'config.yaml')
        config_data = {
            "backend": ["*.py"],
            "frontend": ["*.js"],
            "testing_frameworks": ["test_*.py"]
        }
        save_data(config_data, self.config_path, format='yaml')

    @patch('os.walk')
    @patch('mg_miner.utils.utils.load_config')
    def test_detect_components(self, mock_load_config, mock_os_walk):
        mock_load_config.return_value = {
            "backend": ["*.py"],
            "frontend": ["*.js"],
            "testing_frameworks": ["test_*.py"]
        }
        mock_os_walk.return_value = [
            (self.output_dir, ('subdir',), ('file1.py', 'file2.js', 'test_file.py'))
        ]

        detector = ComponentDetector(output_dir=self.output_dir, silent=True)
        detector.detect_components()

        components_path = os.path.join(self.output_dir, 'components.json')
        self.assertTrue(os.path.exists(components_path))

        with open(components_path, 'r') as f:
            components = json.load(f)

        self.assertIn('backend', components)
        self.assertIn('frontend', components)
        self.assertIn('testing_frameworks', components)
        self.assertEqual(components['backend'], ['file1.py'])
        self.assertEqual(components['frontend'], ['file2.js'])
        self.assertEqual(components['testing_frameworks'], ['test_file.py'])

if __name__ == '__main__':
    unittest.main()
