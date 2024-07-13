import os
import json
import logging
import fnmatch
from typing import Dict, List
from prometheus_client import Counter
from opentelemetry import trace
from mg_miner.utils.utils import load_config, save_json

tracer = trace.get_tracer(__name__)
component_detector_counter = Counter('component_detector_operations', 'Number of component detection operations')

class ComponentDetector:
    """Detects various components of the project (backend, frontend, testing frameworks)
    based on the file types present in the output directory. Keeps track of unmatched files."""

    def __init__(self, output_dir: str, silent: bool) -> None:
        self.output_dir = output_dir
        self.silent = silent

    def detect_components(self) -> None:
        """Detects components and saves the information to a JSON file."""
        logging.info("Detecting components...")
        component_detector_counter.inc()

        with tracer.start_as_current_span("detect_components"):
            try:
                config = load_config(os.path.join(self.output_dir, 'config.json'))

                components = self._initialize_components()
                self._analyze_files(config, components)

                save_json(components, os.path.join(self.output_dir, 'components.json'))

                if not self.silent:
                    logging.info(f"Components detected and saved to {os.path.join(self.output_dir, 'components.json')}")

            except Exception as e:
                logging.error(f"Error detecting components: {e}", exc_info=True)

    def _initialize_components(self) -> Dict[str, List[str]]:
        """Initialize the components dictionary."""
        return {
            "backend": [],
            "frontend": [],
            "testing_frameworks": [],
            "performance_testing": [],
            "static_code_analysis": [],
            "unmatched": []
        }

    def _analyze_files(self, config: Dict, components: Dict[str, List[str]]) -> None:
        """Analyze files and categorize them into components."""
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                matched = self._categorize_file(config, components, file)
                if not matched:
                    components['unmatched'].append(file)

    def _categorize_file(self, config: Dict, components: Dict[str, List[str]], file: str) -> bool:
        """Categorize a file into the appropriate component."""
        for category, patterns in config.items():
            if category in components:
                if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                    components[category].append(file)
                    return True
        return False
