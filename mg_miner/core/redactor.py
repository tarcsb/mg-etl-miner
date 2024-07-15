import os
import re
import logging
from typing import List, Dict
from mg_miner.utils.utils import load_config

class Redactor:
    """Redacts sensitive information from files in the output directory based on compliance standards."""

    def __init__(self, output_dir: str, compliance_standards: List[str], silent: bool = False) -> None:
        self.output_dir = output_dir
        self.compliance_standards = compliance_standards
        self.silent = silent
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[str]:
        """Load sensitive patterns from compliance_patterns.yaml based on the given compliance standards."""
        compliance_patterns_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'compliance_patterns.yaml')
        all_patterns = load_config(compliance_patterns_path)
        patterns = []
        for standard in self.compliance_standards:
            patterns.extend(all_patterns.get(standard, []))
        return patterns

    def redact_sensitive_info(self) -> None:
        """Redacts sensitive information from files in the output directory."""
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                redacted_content = self._redact_content(content)
                with open(file_path, 'w') as f:
                    f.write(redacted_content)
                if not self.silent:
                    logging.info(f"Redacted sensitive information in {file_path}")

    def _redact_content(self, content: str) -> str:
        """Redacts sensitive information from the given content."""
        for pattern in self.patterns:
            content = re.sub(pattern, '[REDACTED]', content)
        return content
