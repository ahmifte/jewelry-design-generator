# Installation

## What You'll Need

- Python 3.10 or newer
- A Meshy API key (grab one at [meshy.ai](https://www.meshy.ai/api))

## Using uv (recommended)

[uv](https://github.com/astral-sh/uv) is a blazing-fast Python package manager and resolver written in Rust. It's up to 10-100x faster than pip or Poetry.

```bash
# Install uv if you don't have it yet
curl -fsSL https://astral.sh/uv/install.sh | bash

# Get the code
git clone https://github.com/ahmifte/python-jewelry-design-gen.git
cd python-jewelry-design-gen

# Install with uv (this is super fast!)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

## Using Poetry (alternative)

Poetry makes everything easier - here's how to use it:

```bash
# Get the code
git clone https://github.com/ahmifte/python-jewelry-design-gen.git
cd python-jewelry-design-gen

# Set up with Poetry
poetry install

# Jump into the poetry env
poetry shell
```

## Using pip (alternative)

If you're more comfortable with pip, that works too:

```bash
# Get the code
git clone https://github.com/ahmifte/python-jewelry-design-gen.git
cd python-jewelry-design-gen

# Install with pip
pip install -e .
```

## Test Your Setup

Let's make sure everything installed correctly:

```bash
# Try a quick test (don't worry, this won't make API calls)
python main.py generate --material silver --type ring --mock
```

If you don't see any errors, you're good to go!
