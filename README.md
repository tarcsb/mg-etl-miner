## cloud migrations Jeffrey Plewak plewak.jeff@gmail.com

# mg-etl-miner
mg-etl-miner is a comprehensive tool for extracting, transforming, and loading data from various projects to perform code maturity analysis. The tool is designed to handle multiple programming languages and detect different components of a project such as backend, frontend, testing frameworks, etc.

## Features

- File collection with exclusion patterns
- Component detection
- Redaction of sensitive information
- Summary creation

## Getting Started


# TODO
- uodate readme for package install pip instal mg-miner
- integrate wirth third parties
- clicommandexamples
- screenshots
- media
- coffee
### Prerequisites

- Python 3.8 or higher
- pip
- a computer lol

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/tarcsb/mg-etl-miner.git
    ```

2. Navigate to the project directory:
    ```
    cd mg-etl-miner
    ```

3. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate
    ```

4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

### Configuration

Create a `config.json` file in the root directory of the project. Here is an example configuration:

```
{
  "excluded_dirs": [".git", "__pycache__", "node_modules", "venv", ".env", ".mypy_cache"],
  "excluded_extensions": ["zip", "tar", "gz", "rar", "7z", "db", "sqlite", "bak", "log", "package-lock.json"],
  "project_types": {
    "Python": ["*.py"],
    "JavaScript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
    "Java": ["*.java"],
    "C++": ["*.cpp", "*.h"],
    "C": ["*.c", "*.h"],
    "HTML": ["*.html", "*.css", "*.js"],
    "YAML": ["*.yaml", "*.yml"],
    "JSON": ["*.json"],
    "INI": ["*.ini"],
    "Markdown": ["README.md", "*.md"],
    "Embedded": ["*.c", "*.cpp", "*.h", "*.ino", "*.asm", "*.S"],
    "Cloud": ["*.yaml", "*.yml", "*.json", "*.tf", "Dockerfile", "docker-compose.yml"],
    "Ruby": ["*.rb"],
    "PHP": ["*.php"],
    "Go": ["*.go"],
    "Swift": ["*.swift"],
    "Kotlin": ["*.kt"],
    "R": ["*.r"],
    "Perl": ["*.pl"],
    "Scala": ["*.scala"],
    "Haskell": ["*.hs"],
    "Rust": ["*.rs"]
  },
  "backend_indicators": {
    "Python": ["*.py", "requirements.txt", "Pipfile", "pyproject.toml"],
    "Django": ["manage.py", "django.*"],
    "Flask": ["app.py", "flask.*"],
    "FastAPI": ["main.py", "fastapi.*"],
    "Java": ["*.java", "pom.xml", "build.gradle"],
    "Spring": ["application.properties", "application.yml", "spring.*"],
    "Node.js": ["*.js", "*.ts", "package.json", "yarn.lock"],
    "Express": ["app.js", "express.*"],
    "Ruby": ["*.rb", "Gemfile"],
    "Rails": ["config.ru", "rails.*"],
    "PHP": ["*.php", "composer.json"],
    "Laravel": ["artisan", "laravel.*"],
    "Go": ["*.go", "go.mod", "go.sum"],
    "Gin": ["gin.*"],
    "Fiber": ["fiber.*"],
    "Swift": ["*.swift", "Package.swift"],
    "Kotlin": ["*.kt", "build.gradle.kts"],
    "Scala": ["*.scala", "build.sbt"],
    "Haskell": ["*.hs", "stack.yaml"],
    "Rust": ["*.rs", "Cargo.toml"],
    "ASP.NET": ["*.csproj", "*.vbproj"],
    "GCP": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf"],
    "AWS": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf", "cloudformation.json", "cloudformation.yaml"],
    "Azure": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf", "azure-pipelines.yml", "azure-pipelines.yaml"]
  },
  "frontend_indicators": {
    "HTML": ["*.html", "*.css", "*.js"],
    "React": ["*.jsx", "*.tsx", "package.json", "yarn.lock"],
    "Vue": ["*.vue", "package.json", "yarn.lock"],
    "Angular": ["*.ts", "*.html", "angular.json"],
    "Svelte": ["*.svelte", "package.json", "yarn.lock"],
    "Ember": ["ember-cli-build.js", "package.json", "yarn.lock"]
  },
  "testing_frameworks": {
    "Python": ["pytest.ini", "conftest.py", "tox.ini"],
    "JavaScript": ["jest.config.js", "karma.conf.js", "mocha.opts"],
    "Java": ["*.java", "testng.xml", "junit-platform.properties"],
    "Ruby": ["*.rb", "spec_helper.rb", "Rakefile"],
    "PHP": ["*.php", "phpunit.xml"],
    "Go": ["*_test.go"],
    "Swift": ["*.swift", "XCTestManifest.swift"],
    "Kotlin": ["*.kt", "build.gradle.kts"],
    "Scala": ["*.scala", "build.sbt"],
    "Haskell": ["*.hs", "test/Spec.hs"],
    "Rust": ["*.rs", "Cargo.toml"],
    "C++": ["*.cpp", "CMakeLists.txt", "*.h"],
    "C": ["*.c", "CMakeLists.txt", "*.h"]
  },
  "performance_testing": {
    "Locust": ["*.locust"]
  },
  "static_code_analysis": {
    "Python": ["*.py"]
  },
  "optional_dirs": [".vscode", ".github", ".eclipse", "coverage", ".config", ".aws"]
}
```

### Usage

#### Collect Files

To collect files from the input directory to the output directory, excluding specified patterns:

```
python -m mg_miner.cli collect --config config.json
```

#### Detect Components

To detect various components of the project based on the file types present in the output directory:

```
python -m mg_miner.cli detect --output-dir output
```

#### Redact Sensitive Information

To redact sensitive information based on compliance patterns from the collected files:

```
python -m mg_miner.cli redact --output-dir output --compliance-standards GDPR HIPAA
```

#### Create Summary

To create a summary of the project:

```
python -m mg_miner.cli summary --output-dir output
```

## Testing

Run the unit tests using pytest:

```
pytest tests/
```

To run the tests with coverage:

```
coverage run -m pytest tests/
coverage report -m
```

## Contributing

Thank you for considering contributing to mg-etl-miner! Here are some guidelines to help you get started:

### Reporting Bugs

If you find a bug, please create an issue on GitHub with detailed information on how to reproduce it. Provide as much detail as possible, including screenshots and logs if available.

### Suggesting Features

We welcome new ideas and feature requests. Please create an issue on GitHub and describe the feature you would like to see, including any potential use cases.

### Submitting Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Format your code with `black` and ensure it complies with `flake8`.
5. Create a pull request with a clear description of your changes.

### Code Style

We use `black` for code formatting and `flake8` for linting. Please ensure your code is formatted and linted before submitting a pull request.

### Running Tests

To run tests, use:

```
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- OpenTelemetry
- Prometheus
- All contributors and supporters

Thank you for being a part of our journey!

