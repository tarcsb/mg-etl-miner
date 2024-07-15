from setuptools import setup, find_packages

setup(
    name="mg-miner",
    version="1.0.0",
    author="Jeffrey Plewak",
    author_email="plewak.jeff@gmail.com",
    description="A comprehensive tool to mine and summarize project files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tarcsb/mg-etl-miner",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "flake8",
        "black",
        "pytest",
        "mypy",
        "bandit",
        "selenium",
        "behave",
        "locust",
        "prometheus-client",
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-prometheus",
        "grafanalib",
        "tqdm"
    ],
    extras_require={
        "dev": [
            "pytest-cov",
            "sphinx",
            "sphinx_rtd_theme",
        ],
    },
    entry_points={
        "console_scripts": [
            "mg_miner=mg_miner.cli:main",
        ],
    },
)

