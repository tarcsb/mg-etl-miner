import os
import logging
from typing import Dict, List
from retrying import retry
from mg_miner.utils.utils import load_config, save_data

class SummaryCreator:
    """Creates a summary HTML file from components.json in the output directory."""

    def __init__(self, output_dir: str, silent: bool, theme: str) -> None:
        self.output_dir = output_dir
        self.silent = silent
        self.theme = theme

    @retry(wait_fixed=2000, stop_max_attempt_number=3)
    def create_summary(self) -> None:
        """Creates the summary HTML file."""
        logging.info("Creating summary...")
        try:
            components_path = os.path.join(self.output_dir, 'components.json')
            if not os.path.exists(components_path):
                raise FileNotFoundError(f"{components_path} does not exist")

            components = load_config(components_path)

            summary_html = self._generate_html(components)

            summary_path = os.path.join(self.output_dir, 'summary.html')
            with open(summary_path, 'w') as f:
                f.write(summary_html)
                f.flush()
                os.fsync(f.fileno())

            if not self.silent:
                logging.info(f"Summary created and saved to {summary_path}")

        except Exception as e:
            logging.error(f"Error creating summary: {e}", exc_info=True)
            raise

    def _generate_html(self, components: Dict[str, List[str]]) -> str:
        """Generates HTML content based on the components and theme."""
        html_content = f"<html><head><title>Project Summary</title></head><body>"
        html_content += f"<h1>Project Components Summary</h1>"
        for category, files in components.items():
            html_content += f"<h2>{category}</h2><ul>"
            for file in files:
                html_content += f"<li>{file}</li>"
            html_content += f"</ul>"
        html_content += f"</body></html>"
        return html_content
