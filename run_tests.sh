#!/bin/bash

# Ensure we are in the correct directory
cd "$(dirname "$0")"

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Run tests with coverage
pytest --cov=mg_miner --cov-report=term-missing --cov-config=.coveragerc

# Generate coverage report
coverage html
coverage report -m

