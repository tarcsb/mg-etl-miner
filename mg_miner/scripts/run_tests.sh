#!/bin/bash

# Ensure we are in the correct directory
cd "$(dirname "$0")/.."

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Run tests
coverage run --source=mg_miner -m unittest discover -s tests/unit

# Generate coverage report
coverage html
