"""Configuration utilities for the jewelry design generator."""

import os
import json
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables and config files.

    Priority order:
    1. .env.local file (for local development)
    2. .env file (for general use)
    3. config.json file
    4. Default values

    Returns:
        Dict containing configuration values.
    """
    # First, check for .env.local and load if exists
    env_local = Path(".env.local")
    env_file = Path(".env")

    if env_local.exists():
        load_dotenv(dotenv_path=env_local)
    elif env_file.exists():
        load_dotenv(dotenv_path=env_file)

    # For local testing, use the BATCH_SIZE from .env.local if available
    batch_size = int(
        os.getenv("BATCH_SIZE", os.getenv("DEFAULT_BATCH_SIZE", "10")))
    max_workers = int(os.getenv("MAX_WORKERS", "3"))

    config = {
        # Meshy API configuration
        "meshy_api_key": os.getenv("MESHY_API_KEY", ""),
        "meshy_api_base_url": os.getenv(
            "MESHY_API_BASE_URL",
            "https://api.meshy.ai"
        ),

        # File paths
        "output_dir": os.getenv("OUTPUT_DIR", "output"),
        "models_dir": os.getenv("MODELS_DIR", "output/models"),
        "metadata_dir": os.getenv("METADATA_DIR", "output/metadata"),

        # Generation settings
        "default_material": os.getenv("DEFAULT_MATERIAL", "gold"),
        "default_jewelry_type": os.getenv("DEFAULT_JEWELRY_TYPE", "chain"),
        "default_chain_style": os.getenv("DEFAULT_CHAIN_STYLE", "cuban"),
        "default_batch_size": batch_size,
        "max_workers": max_workers,
        "enable_pbr": os.getenv("ENABLE_PBR", "true").lower() == "true",
        "art_style": os.getenv("ART_STYLE", "realistic"),

        # Advanced settings
        "symmetry_mode": os.getenv("SYMMETRY_MODE", "on"),
        "should_remesh": os.getenv("SHOULD_REMESH", "true").lower() == "true",
        "topology": os.getenv("TOPOLOGY", "quad"),
        "target_polycount": int(os.getenv("TARGET_POLYCOUNT", "100000")),
        "ai_model": os.getenv("AI_MODEL", "meshy-4"),
    }

    # Load config from JSON file if it exists
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, "r") as f:
            file_config = json.load(f)
            # Update config with values from file
            config.update(file_config)

    return config


def get_meshy_api_key() -> str:
    """
    Get the Meshy API key from config.

    Returns:
        The API key as a string.

    Raises:
        ValueError: If the API key is not set.
    """
    config = load_config()
    api_key = config.get("meshy_api_key")

    if not api_key:
        raise ValueError(
            "Meshy API key not found. "
            "Please set it in the MESHY_API_KEY environment variable "
            "or in the config.json file."
        )

    return api_key


def get_model_output_path(design_id: str) -> Path:
    """
    Get the output path for a model file.

    Args:
        design_id: The ID of the design.

    Returns:
        Path to the output directory for the design.
    """
    config = load_config()
    models_dir = Path(config["models_dir"])

    # Create path with design ID as subdirectory
    output_path = models_dir / design_id
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path
