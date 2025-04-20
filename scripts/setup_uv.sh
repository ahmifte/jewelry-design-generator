#!/bin/bash
# Helper script to set up the environment with uv

# Ensure we're in the project root directory
SCRIPT_DIR=$(dirname "$0")
cd "${SCRIPT_DIR}/.." || exit 1

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing now..."
    curl -fsSL https://astral.sh/uv/install.sh | bash
    echo "Please restart your terminal or source your shell config file."
    exit 1
fi

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
fi

# Activate virtual environment if not already activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies with uv..."
uv pip install -e ".[dev]"

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ] && [ ! -f ".env.local" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your Meshy API key."
fi

echo "Setup complete! Your environment is ready."
echo "Run 'source .venv/bin/activate' if you're in a new terminal."
echo "Pre-commit hooks are installed and will run automatically on git commit."
echo "Run 'python main.py generate --material silver --type ring --mock' to test."
