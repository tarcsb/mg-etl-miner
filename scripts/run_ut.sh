#!/bin/bash

# Ensure we are in the correct directory
cd "$(dirname "$0")/.."

# Set the PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Load environment variables
source ./scripts/env/load_env.sh

# Run tests with coverage
pytest --cov=mg_miner --cov-report=html

# Check the coverage report
echo "Coverage report generated in htmlcov directory. Open htmlcov/index.html to view it."

# Ask the user if they want to view the HTML coverage report
read -p "Do you want to view the HTML coverage report now? (y/n): " choice

if [[ "$choice" == [Yy]* ]]; then
    # Start a simple HTTP server to serve the coverage report
    cd htmlcov
    python3 -m http.server 8000 &

    # Open the default web browser to view the coverage report
    if which xdg-open > /dev/null
    then
      xdg-open http://localhost:8000/index.html
    elif which gnome-open > /dev/null
    then
      gnome-open http://localhost:8000/index.html
    elif which open > /dev/null
    then
      open http://localhost:8000/index.html
    else
      echo "Could not detect the web browser to use."
    fi
fi

