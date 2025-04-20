# Usage Guide

## Command Line

Here's how to use the tool from the command line:

### Making a Single Design

```bash
# Make a gold ring
python main.py generate --material gold --type ring

# Create a silver cuban chain
python main.py generate --material silver --type chain --chain-style cuban

# Use a custom prompt and choose formats
python main.py generate --prompt "Gold bracelet with intricate Celtic patterns" --formats glb,fbx,obj

# Generate and view in your browser
python main.py generate --material gold --type pendant --open-browser

# Testing? Use mock mode (no API calls)
python main.py generate --material gold --type ring --mock
```

### Batch Generation

```bash
# Make 10 gold chains with different styles
python main.py batch --material gold --type chain --batch-size 10

# Create 5 silver rings using 2 workers (faster)
python main.py batch --material silver --type ring --batch-size 5 --max-workers 2

# Generate multiple designs and open the first one
python main.py batch --material silver --type earrings --batch-size 3 --open-browser

# Test batch generation without API calls
python main.py batch --material gold --type chain --batch-size 5 --mock
```

### Viewing Designs

```bash
# Get info about a design by ID
python main.py info abc123def456

# View a design in your browser
python main.py info abc123def456 --open-browser
```

## Using in Python Code

You can use the library directly in your code too:

```python
from python_jewelry_design_gen.models.jewelry_design import Material, JewelryType, ChainStyle
from python_jewelry_design_gen.generators.meshy_generator import MeshyJewelryGenerator

# Set up the generator
generator = MeshyJewelryGenerator(api_key="your_api_key_here")

# Make a gold cuban chain
design = generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.CHAIN,
    chain_style=ChainStyle.CUBAN,
    formats=["glb", "fbx"],
    wait_for_completion=True
)

# See what we got
print(f"Created: {design.display_name}")
print(f"Model URLs: {design.model_urls}")

# For testing without API calls
mock_generator = MeshyJewelryGenerator(mock_mode=True)
mock_design = mock_generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.RING
)

# Make 5 designs at once
designs = generator.generate_batch(
    batch_size=5,
    material=Material.SILVER,
    jewelry_type=JewelryType.RING,
    max_workers=3  # use 3 parallel workers
)

# Check out what we made
for design in designs:
    print(f"Design ID: {design.id}, Name: {design.display_name}")
``` 