# Testing

We've included tests to make sure everything works correctly. Here's how to run them:

## Running Tests

```bash
# First, activate your virtual environment
poetry shell   # if you're using Poetry
# Or
source .venv/bin/activate   # if you're using pip

# Run all tests
python -m pytest

# Run a specific test file
python -m pytest tests/test_generator.py

# See detailed test output
python -m pytest -v

# Check code coverage
python -m pytest --cov=python_jewelry_design_gen
```

## Troubleshooting Tests

If your tests aren't working:
1. Make sure your virtual environment is active
2. Check that you installed the package in dev mode
3. Verify all dependencies are installed

```bash
# Install in dev mode
pip install -e .

# Install test dependencies
pip install pytest pytest-cov
```

## Mock Mode for Testing

Don't want to use up API credits during development? Use mock mode:

- Works without an API key
- Uses no API credits
- Works offline
- Perfect for CI/CD

### Command Line Mock Mode

Just add `--mock` to any command:

```bash
# Generate a design locally
python main.py generate --material gold --type ring --mock

# Create multiple test designs
python main.py batch --material silver --type earrings --batch-size 3 --mock
```

### Mock Mode in Code

```python
# Create a mock generator
generator = MeshyJewelryGenerator(mock_mode=True)

# Generate a test design
design = generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.RING
)

# You'll get mock URLs
print(design.model_urls)  # These will be fake URLs
```

Mock mode creates the same folder structure and metadata but without actual 3D files. It's perfect for testing your code without using API credits.
