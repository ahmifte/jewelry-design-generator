# Using uv for Development

This project uses [uv](https://github.com/astral-sh/uv), an extremely fast Python package manager and environment manager built in Rust.

## Why uv?

- **Speed**: uv is 10-100x faster than pip or Poetry
- **Reliability**: Built in Rust with a focus on deterministic builds
- **Compatibility**: Works with existing project formats (pyproject.toml, requirements.txt)
- **Modern features**: Dependency resolution, virtual environments, locking

## Development Workflow

Here's how to work with this project using uv:

### First-Time Setup

```bash
# First, ensure you have uv installed
curl -fsSL https://astral.sh/uv/install.sh | bash

# Alternative for Windows PowerShell:
# iwr -useb https://astral.sh/uv/install.ps1 | iex

# Clone the repo
git clone https://github.com/ahmifte/python-jewelry-design-gen.git
cd python-jewelry-design-gen

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"  # Install with development dependencies

# Set up pre-commit hooks
pre-commit install

# Copy the environment template
cp .env.example .env
# Edit .env to add your Meshy API key
```

### Alternatively, use our setup script

```bash
# For Unix/Linux/Mac
mkdir -p scripts
chmod +x scripts/setup_uv.sh  # Make executable
./scripts/setup_uv.sh
```

### Day-to-Day Development

```bash
# Activate the environment (if not already active)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Running the tool
python main.py generate --material silver --type ring

# Running tests
pytest

# Adding new dependencies
uv pip install some-package
# Then update pyproject.toml manually to include it

# Manual pre-commit check (runs automatically on git commit)
pre-commit run --all-files
```

## Code Quality and Pre-commit

This project uses [pre-commit](https://pre-commit.com/) to maintain code quality. Pre-commit hooks automatically run before each commit to catch issues early:

- Trailing whitespace removal
- File ending fixes
- Code formatting with autopep8
- Import ordering
- Flake8 linting
- And more...

The hooks are configured in `.pre-commit-config.yaml` and run automatically after you install pre-commit with `pre-commit install`.

## Speed Comparison

Tasks that took minutes with pip or Poetry now take seconds with uv:

| Task | pip | Poetry | uv |
|------|-----|--------|-----|
| Initial environment setup | 45-90 sec | 30-60 sec | 3-8 sec |
| Installing all dependencies | 30-60 sec | 20-40 sec | 2-5 sec |
| Adding a single package | 10-20 sec | 8-15 sec | <1 sec |

## CI/CD Integration

Our GitHub Actions workflows now use uv for faster builds and more reliable testing:

- `.github/workflows/python-tests.yml` - Runs tests with pytest
- `.github/workflows/pre-commit.yml` - Runs pre-commit checks

Both use uv for dependency installation, making the CI pipeline much faster.
