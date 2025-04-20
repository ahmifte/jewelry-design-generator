# Jewelry Design Workflow

Here's how to use this tool from start to finish:

## Step 1: Set Up Your API Key

First, you need your Meshy API key:

```bash
# Just create this file with your key
echo "MESHY_API_KEY=your_api_key_here" > .env
```

## Step 2: Generate Some Designs

### One at a Time

```bash
# Simple gold ring
python main.py generate --material gold --type ring

# Get fancy with options
python main.py generate --material silver --type necklace --custom-prompt "Minimalist silver necklace with geometric pendant"
```

### Batch Mode

```bash
# Make 3 different gold pendants
python main.py batch --material gold --type pendant --batch-size 3

# Speed things up with parallel processing
python main.py batch --material silver --type earrings --batch-size 5 --max-workers 3
```

## Step 3: Check Out Your Designs

Your generated files end up here:
- `output/models/<design_id>/` - For the 3D models
- `output/metadata/<design_id>.json` - For the metadata

```bash
# See info about a design
python main.py info <design_id>
```

## Using the Browser Viewer

Want to actually see your models? Use the browser integration:

```bash
# Make a design and open it right away
python main.py generate --material gold --type ring --open-browser

# Make a batch and see the first one
python main.py batch --material silver --type chain --batch-size 2 --open-browser

# View an existing design
python main.py info <design_id> --open-browser
```

What happens when you use `--open-browser`:
1. Your design gets generated
2. When it's done, your browser opens automatically
3. You'll see either a thumbnail or 3D model viewer
4. For GLB files, you get an interactive 3D viewer

It'll show:
- PNG thumbnails directly
- GLB models in a 3D viewer
- Other model URLs in your browser

### Browser Support

Works best with:
- Chrome (recommended)
- Firefox 
- Safari (mostly works)
- Edge

Make sure WebGL is enabled for the best experience.

## Dev Workflow Tips

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

3. View what you made:
```bash
python main.py info <design_id> --open-browser
```

This lets you test changes quickly without waiting forever for big batches. 