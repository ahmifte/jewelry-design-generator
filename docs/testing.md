# Testing

This project has tests to make sure everything works. Here's how to run them:

## Running Tests

```bash
# First, activate your virtual environment
poetry shell   # if you're using Poetry
# Or
source .venv/bin/activate   # if you're using pip

# Run all tests
python -m pytest

# Run just one test file
python -m pytest tests/test_generator.py

# See more details as tests run
python -m pytest -v

# Check code coverage
python -m pytest --cov=python_jewelry_design_gen
```

## Fixing Test Issues

If tests aren't working:
1. Make sure your virtual env is activated
2. Check that you installed the package in dev mode
3. Double-check all dependencies are installed

```bash
# Install in dev mode
pip install -e .

# Get test dependencies
pip install pytest pytest-cov
```

## Mock Mode for Testing

Don't want to waste API calls during development? Use mock mode:

- No API key needed
- No API credits used
- Works offline
- Perfect for CI/CD

### Command Line Mock Mode

Just add `--mock` to any command:

```bash
# Generate a fake design locally
python main.py generate --material gold --type ring --mock

# Make multiple fake designs
python main.py batch --material silver --type earrings --batch-size 3 --mock
```

### Mock Mode in Code

```python
# Create a mock generator
generator = MeshyJewelryGenerator(mock_mode=True)

# Make a fake design
design = generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.RING
)

# You'll get mock URLs
print(design.model_urls)  # These are fake URLs
```

Mock mode creates the same folder structure and metadata, but without actual 3D files. Perfect for testing your code without burning through API credits. 