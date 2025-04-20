# Usage Guide

## Command Line

Here's how to use the tool from the command line:

### Creating a Single Design

```bash
# Create a gold ring
python main.py generate --material gold --type ring

# Make a silver cuban chain
python main.py generate --material silver --type chain --chain-style cuban

# Customize with your own prompt and formats
python main.py generate --prompt "Gold bracelet with intricate Celtic patterns" --formats glb,fbx,obj

# Generate and view in your browser
python main.py generate --material gold --type pendant --open-browser

# Testing? Try mock mode (no API calls)
python main.py generate --material gold --type ring --mock
```

### Batch Generation

```bash
# Create 10 gold chains with different styles
python main.py batch --material gold --type chain --batch-size 10

# Make 5 silver rings faster with workers
python main.py batch --material silver --type ring --batch-size 5 --max-workers 2

# Generate multiple designs and view the first one
python main.py batch --material silver --type earrings --batch-size 3 --open-browser

# Test batch mode without API calls
python main.py batch --material gold --type chain --batch-size 5 --mock
```

### Viewing Designs

```bash
# Get info about a design
python main.py info abc123def456

# View a design in your browser
python main.py info abc123def456 --open-browser
```

## Using in Python Code

You can use the library directly in your code:

```python
from python_jewelry_design_gen.models.jewelry_design import Material, JewelryType, ChainStyle
from python_jewelry_design_gen.generators.meshy_generator import MeshyJewelryGenerator

# Set up the generator
generator = MeshyJewelryGenerator(api_key="your_api_key_here")

# Create a gold cuban chain
design = generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.CHAIN,
    chain_style=ChainStyle.CUBAN,
    formats=["glb", "fbx"],
    wait_for_completion=True
)

# Check out what you made
print(f"Created: {design.display_name}")
print(f"Model URLs: {design.model_urls}")

# For testing without API calls
mock_generator = MeshyJewelryGenerator(mock_mode=True)
mock_design = mock_generator.generate_design(
    material=Material.GOLD,
    jewelry_type=JewelryType.RING
)

# Create 5 designs at once
designs = generator.generate_batch(
    batch_size=5,
    material=Material.SILVER,
    jewelry_type=JewelryType.RING,
    max_workers=3  # use 3 parallel workers
)

# See what you've created
for design in designs:
    print(f"Design ID: {design.id}, Name: {design.display_name}")
```
