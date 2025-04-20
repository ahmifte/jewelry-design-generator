#!/bin/bash
# Run tests with coverage report

set -e

echo "Running tests with coverage for Python Jewelry Design Generator..."

pip install pytest pytest-cov python-dotenv

if [ -f ".env.local" ]; then
    echo "Found .env.local file, using it for local testing"
    export DOTENV_FILE=".env.local"
else
    echo "No .env.local file found. Create one for local testing configuration."
    export DOTENV_FILE=".env"
fi

python -m pytest tests/ --cov=python_jewelry_design_gen --cov-report=term-missing

echo "\n\n"
echo "Test complete! You can see missing lines above."
echo "For a more detailed report, run: python -m pytest tests/ --cov=python_jewelry_design_gen --cov-report=html"
echo "Then open 'htmlcov/index.html' in your browser."
echo "\n\n"

if [ "$1" = "--with-sample" ]; then
    echo ""
    echo "Running a sample batch generation with size=1 from .env.local..."
    python -c "
import os
from dotenv import load_dotenv
from python_jewelry_design_gen.generators.meshy_generator import MeshyJewelryGenerator
from python_jewelry_design_gen.models.jewelry_design import Material, JewelryType

# Load environment variables from .env.local
load_dotenv(dotenv_path='$DOTENV_FILE')

# Create generator
generator = MeshyJewelryGenerator()

# Generate a batch with size=1 (uses BATCH_SIZE from .env.local)
batch_size = int(os.getenv('BATCH_SIZE', 1))
print(f'Generating a batch of {batch_size} designs...')

try:
    # Only print info, don't actually generate unless MESHY_API_KEY is properly set
    if os.getenv('MESHY_API_KEY') == 'your_test_api_key_here':
        print('Skipping actual generation since MESHY_API_KEY is not properly set.')
        print('Please update your .env.local file with a valid API key to run actual generation.')
    else:
        designs = generator.generate_batch(
            batch_size=batch_size,
            material=Material.GOLD,
            jewelry_type=JewelryType.RING,
            max_workers=int(os.getenv('MAX_WORKERS', 1))
        )
        print(f'Generated {len(designs)} designs')
except Exception as e:
    print(f'Error generating designs: {e}')
"
fi 