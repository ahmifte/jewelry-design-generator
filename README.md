# Jewelry Design Generator

Create awesome 3D jewelry designs with AI. This tool lets you build detailed models of rings, chains, bracelets and more in different materials like gold, silver, and stainless steel.

![Silver Ring](examples/ring_example.png)

## Tech Stack

I've built this using:

- **Python 3.10+**: As the main language
- **[Meshy AI](https://docs.meshy.ai)**: For the 3D model generation (their API is amazing for jewelry)
- **Poetry**: Handles dependencies way better than pip alone
- **Asyncio**: Makes batch generation much faster with concurrent API calls
- **Logging**: Keeps track of what's happening during generation

## Features

- Make 3D models of rings, chains, bracelets, necklaces, earrings, and pendants
- Choose from gold, silver, stainless steel, or plated metals 
- Create different chain styles (cuban, figaro, rope, etc.) with smooth edges
- Generate multiple designs at once for production runs
- Download in GLB, FBX, OBJ or USDZ formats
- Get PBR textures for realistic renders

## Example Outputs

Check out these silver jewelry designs the tool created:

### Classic Silver Ring
![Silver Ring](examples/ring_example.png)

### Silver Pendant
![Silver Pendant](examples/pendant_example.png)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/ahmifte/python-jewelry-design-gen.git
cd python-jewelry-design-gen

# Install with Poetry
poetry install

# Add your Meshy API key
echo "MESHY_API_KEY=your_api_key_here" > .env

# Make your first design!
python main.py generate --material silver --type ring
```

## Documentation

Want more details? Check out:

- [How to install](docs/installation.md)
- [Configuration options](docs/configuration.md)
- [Usage guide](docs/usage.md)
- [Workflow examples](docs/workflow.md)
- [Example output images](docs/examples.md)
- [Testing the code](docs/testing.md)

## Meshy Integration

The tool uses [Meshy AI](https://docs.meshy.ai) for text-to-3D generation. I've optimized the prompts specifically for jewelry, and you'll get:

- Great 3D models from text descriptions
- Multiple export formats
- PBR materials that look like real metals
- Lots of customization options

## License

MIT