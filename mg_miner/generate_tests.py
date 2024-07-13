import os
import json
import shutil

def create_test_environment(test_dir, output_dir):
    # Create test directories
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Create test files
    with open(os.path.join(test_dir, "test_file.py"), "w") as f:
        f.write("print('Hello, World!')\n")
    
    with open(os.path.join(test_dir, "test_file.log"), "w") as f:
        f.write("This is a log file.\n")

    with open(os.path.join(test_dir, "test_file.html"), "w") as f:
        f.write("<html><body>Hello, World!</body></html>\n")

    with open(os.path.join(test_dir, "pytest.ini"), "w") as f:
        f.write("[pytest]\n")

    # Create a config file
    config = {
        "excluded_dirs": [".git", "__pycache__", "node_modules", "venv", ".env", ".mypy_cache"],
        "excluded_extensions": ["zip", "tar", "gz", "rar", "7z", "db", "sqlite", "bak", "log", "package-lock.json"],
        "project_types": {
            "Python": ["*.py"]
        },
        "frontend_indicators": {
            "HTML": ["*.html", "*.css", "*.js"]
        },
        "testing_frameworks": {
            "Python": ["pytest.ini", "conftest.py", "tox.ini"]
        },
        "performance_testing": {
            "Locust": ["*.locust"]
        },
        "static_code_analysis": {
            "Python": ["*.py"]
        },
        "optional_dirs": [".vscode", ".github", ".eclipse", "coverage", ".config", ".aws"]
    }

    with open(os.path.join(output_dir, "config.json"), "w") as f:
        json.dump(config, f)

def create_test_script(test_dir, output_dir):
    test_script = f"""
import os
import shutil
import json
import pytest
from mg_miner.core.file_collector import FileCollector
from mg_miner.core.component_detector import ComponentDetector
from mg_miner.core.redactor import Redactor
from mg_miner.core.summary_creator import SummaryCreator

@pytest.fixture(scope="module")
def setup_test_environment():
    test_dir = "{test_dir}"
    output_dir = "{output_dir}"
    create_test_environment(test_dir, output_dir)
    yield test_dir, output_dir
    shutil.rmtree(test_dir)
    shutil.rmtree(output_dir)

def test_file_collector(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    file_collector = FileCollector(test_dir, output_dir, ["*.log"], True)
    file_collector.collect_files()
    assert os.path.exists(os.path.join(output_dir, "test_file.py"))
    assert not os.path.exists(os.path.join(output_dir, "test_file.log"))

def test_file_collector_excluded_dirs(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    nested_dir = os.path.join(test_dir, "node_modules")
    os.makedirs(nested_dir)
    with open(os.path.join(nested_dir, "nested_file.js"), "w") as f:
        f.write("console.log('Nested file');\\n")

    file_collector = FileCollector(test_dir, output_dir, ["*.log"], True)
    file_collector.collect_files()
    assert not os.path.exists(os.path.join(output_dir, "nested_file.js"))

def test_component_detector(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    file_collector = FileCollector(test_dir, output_dir, ["*.log"], True)
    file_collector.collect_files()
    component_detector = ComponentDetector(output_dir, True)
    component_detector.detect_components()
    assert os.path.exists(os.path.join(output_dir, "components.json"))

def test_redactor(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    sensitive_content = "Sensitive information: 123-45-6789"
    sensitive_file = os.path.join(output_dir, "sensitive.txt")
    with open(sensitive_file, "w") as f:
        f.write(sensitive_content)
    
    redactor = Redactor(output_dir, True)
    redactor.redact_sensitive_info()
    
    with open(sensitive_file, "r") as f:
        content = f.read()
    
    assert "[REDACTED]" in content
    assert "123-45-6789" not in content

def test_summary_creator(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    file_collector = FileCollector(test_dir, output_dir, ["*.log"], True)
    file_collector.collect_files()
    component_detector = ComponentDetector(output_dir, True)
    component_detector.detect_components()
    summary_creator = SummaryCreator(output_dir, True, 'light')
    summary_creator.create_summary()
    assert os.path.exists(os.path.join(output_dir, "summary.html"))

def test_file_collector_with_exclude_files(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    file_collector = FileCollector(test_dir, output_dir, ["*.py", "*.log"], True)
    file_collector.collect_files()
    assert not os.path.exists(os.path.join(output_dir, "test_file.py"))
    assert not os.path.exists(os.path.join(output_dir, "test_file.log"))
    assert os.path.exists(os.path.join(output_dir, "test_file.html"))

def test_component_detector_unmatched_files(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    file_collector = FileCollector(test_dir, output_dir, ["*.log"], True)
    file_collector.collect_files()
    with open(os.path.join(output_dir, "unknown.xyz"), "w") as f:
        f.write("Unknown content")
    component_detector = ComponentDetector(output_dir, True)
    component_detector.detect_components()
    with open(os.path.join(output_dir, "components.json"), "r") as f:
        components = json.load(f)
    assert "unknown.xyz" in components["unmatched"]

def test_redactor_no_sensitive_info(setup_test_environment):
    test_dir, output_dir = setup_test_environment
    non_sensitive_content = "This is a normal text."
    non_sensitive_file = os.path.join(output_dir, "normal.txt")
    with open(non_sensitive_file, "w") as f:
        f.write(non_sensitive_content)
    
    redactor = Redactor(output_dir, True)
    redactor.redact_sensitive_info()
    
    with open(non_sensitive_file, "r") as f:
        content = f.read()
    
    assert non_sensitive_content in content
    assert "[REDACTED]" not in content
    """
    with open(os.path.join("tests", "test_mg_miner.py"), "w") as f:
        f.write(test_script)

if __name__ == "__main__":
    test_dir = "test_dir"
    output_dir = "test_output"
    
    if not os.path.exists("tests"):
        os.makedirs("tests")
    
    create_test_environment(test_dir, output_dir)
    create_test_script(test_dir, output_dir)
    print("Test environment and test script created successfully.")
    

    with open("my_project/generate_tests.py", 'w') as f:
        f.write(generate_tests_script)

if __name__ == "__main__":
    test_dir = "test_dir"
    output_dir = "test_output"
    
    if not os.path.exists("tests"):
        os.makedirs("tests")
    
    create_test_environment(test_dir, output_dir)
    create_test_script(test_dir, output_dir)
    print("Test environment and test script created successfully.")

