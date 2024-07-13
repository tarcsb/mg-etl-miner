from setuptools import setup, find_packages

# Read the long description from a separate file if necessary
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mg-miner",
    version="1.0.0",
    author="Jeffrey Plewak",
    author_email="plewak.jeff@gmail.com",
    description="A comprehensive tool to mine and summarize project files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tarcsb/mg-miner",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mg_miner=mg_miner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },
    python_requires='>=3.6',
    install_requires=[
        "flake8",
        "black",
        "pytest",
        "pytest-cov",
        "mypy",
        "bandit",
        "selenium",
        "behave",
        "locust",
        "prometheus-client",
        "opentelemetry-api==1.7.0",
        "opentelemetry-sdk==1.7.0",
        "opentelemetry-exporter-prometheus==0.17b0",
        "grafanalib"
    ],
    extras_require={
        "dev": ["pytest-cov", "sphinx", "sphinx_rtd_theme", "coverage"]
    }
)
