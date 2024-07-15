#!/bin/bash

# Ensure we are in the correct directory
cd "$(dirname "$0")"

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Run tests
coverage run -m unittest discover -s mg_miner/tests

# Generate coverage report
coverage html
coverage report -m
