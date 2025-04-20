# Jewelry Design Workflow

Here's how to use this tool from start to finish:

## Step 1: Set Up Your API Key

First, grab your Meshy API key:

```bash
# Create a file with your key
echo "MESHY_API_KEY=your_api_key_here" > .env
```

## Step 2: Generate Designs

### One at a Time

```bash
# Create a simple gold ring
python main.py generate --material gold --type ring

# Get creative with options
python main.py generate --material silver --type necklace --custom-prompt "Minimalist silver necklace with geometric pendant"
```

### Batch Mode

```bash
# Make 3 gold pendants
python main.py batch --material gold --type pendant --batch-size 3

# Speed up with parallel processing
python main.py batch --material silver --type earrings --batch-size 5 --max-workers 3
```

## Step 3: View Your Designs

You'll find your generated files here:
- `output/models/<design_id>/` - 3D models
- `output/metadata/<design_id>.json` - Metadata

```bash
# Check info about your design
python main.py info <design_id>
```

## Using the Browser Viewer

Want to see your models? Use the browser integration:

```bash
# Create and view right away
python main.py generate --material gold --type ring --open-browser

# Make a batch and see the first one
python main.py batch --material silver --type chain --batch-size 2 --open-browser

# View an existing design
python main.py info <design_id> --open-browser
```

When you use `--open-browser`:
1. Your browser opens automatically after generation
2. You'll see a thumbnail or 3D model viewer
3. GLB files get an interactive 3D viewer
4. Other formats open as direct links

Works best with:
- Chrome
- Firefox
- Safari
- Edge

Make sure WebGL is on for the best experience.

## Tips for Developers

If you're working on the code:

1. Create a `.env.local` file with faster settings:
```
MESHY_API_KEY=your_api_key_here
BATCH_SIZE=1
MAX_WORKERS=1
```

2. Test with a quick generation:
```bash
python main.py generate --material gold --type ring
```

3. View your creation:
```bash
python main.py info <design_id> --open-browser
```

This lets you test changes quickly without waiting for large batches.
