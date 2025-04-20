# Configuration

You'll need to set up your Meshy API key before you start. There are a few ways to do this:

## 1. Environment Variables

Create a `.env` file in the root folder:

```
MESHY_API_KEY=your_api_key_here
```

## 2. For Local Development

For development, I recommend using a `.env.local` file (git ignores this one):

```bash
# Copy the example file
cp .env.example .env.local

# Edit it with your favorite editor
nano .env.local  # or use VS Code, vim, whatever

# Pro tip: For local testing, set these values
# BATCH_SIZE=1
# MAX_WORKERS=1
```

The `.env.local` file overrides `.env`, so you can keep your personal settings separate.

## 3. Config File

You can also create a config file:

```bash
python main.py init
```

This gives you a `config.json` file. Open it and add your API key.

## Advanced Stuff

Want more control? Edit the `config.json` file with options like these:

```json
{
  "meshy_api_key": "your_api_key_here",
  "output_dir": "output",
  "models_dir": "output/models",
  "metadata_dir": "output/metadata",
  "default_material": "gold",
  "default_jewelry_type": "chain",
  "default_chain_style": "cuban",
  "default_batch_size": 10,
  "enable_pbr": true,
  "art_style": "realistic",
  "symmetry_mode": "on",
  "should_remesh": true,
  "topology": "quad",
  "target_polycount": 100000,
  "ai_model": "meshy-4"
}
``` 