#!/bin/bash
# Test script for Python Jewelry Design Generator
set -e

# Move to project root
SCRIPT_DIR=$(realpath "$(dirname "$0")")
cd "$(dirname "$SCRIPT_DIR")" || exit 1

# Set up virtual environment if needed
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Creating virtual environment with uv..."
    uv venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    uv pip install -e ".[dev]"
fi

# Set up test environment
if [ ! -f .env.local ]; then
    echo "Creating test environment file..."
    cp .env.example .env.local
    sed -i.bak 's/your_api_key_here/test-key-for-unit-tests/g' .env.local
    rm -f .env.local.bak
fi

# Enable test mode
export PYTEST_MOCK_MODE=true

# Run tests with coverage
echo "Running tests with coverage..."
python -m pytest --cov=python_jewelry_design_gen --cov-report=term

# Run optional test batch
if [ "$1" == "--run-batch" ]; then
    echo "Running test batch generation in mock mode..."
    python main.py batch --material gold --type ring --batch-size 2 --mock
fi

echo "Tests completed successfully!"
