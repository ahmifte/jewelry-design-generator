"""File utility functions for the jewelry design generator."""

import os
import json
import requests
import webbrowser
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


def ensure_dir(directory: str) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory.

    Returns:
        Path object for the directory.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_batch_id() -> str:
    """
    Generate a unique batch ID.

    Returns:
        A string containing a timestamp-based batch ID.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"batch_{timestamp}"


def save_design_metadata(
    design_id: str,
    metadata: Dict[str, Any],
    output_dir: str,
    negative_prompt: str = "",
    seed: int = None,
    model_name: str = "default",
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    design_type: str = "jewelry",
    additional_metadata: Dict[str, Any] = None,
) -> str:
    """
    Save design metadata to a JSON file.

    Args:
        design_id: Unique identifier for the design.
        metadata: Dictionary containing design metadata.
        output_dir: Directory to save the metadata file.
        negative_prompt: Negative prompt used to generate the design (optional).
        seed: Random seed used for generation (optional).
        model_name: Name of the model used for generation (optional).
        num_inference_steps: Number of inference steps used (optional).
        guidance_scale: Guidance scale used for generation (optional).
        design_type: Type of design (e.g., 'ring', 'pendant') (optional).
        additional_metadata: Any additional metadata to include (optional).

    Returns:
        Path to the saved metadata file.
    """
    from python_jewelry_design_gen.utils.config import load_config

    if output_dir is None:
        config = load_config()
        output_dir = config.get("metadata_dir", "output/metadata")

    # Ensure directory exists
    metadata_dir = ensure_dir(output_dir)

    # Merge provided metadata with additional parameters
    final_metadata = metadata.copy() if metadata else {}

    # Only add these fields if they aren't already in the metadata
    if "negative_prompt" not in final_metadata:
        final_metadata["negative_prompt"] = negative_prompt
    if "seed" not in final_metadata:
        final_metadata["seed"] = seed
    if "model_name" not in final_metadata:
        final_metadata["model_name"] = model_name
    if "num_inference_steps" not in final_metadata:
        final_metadata["num_inference_steps"] = num_inference_steps
    if "guidance_scale" not in final_metadata:
        final_metadata["guidance_scale"] = guidance_scale
    if "design_type" not in final_metadata:
        final_metadata["design_type"] = design_type

    # Add additional metadata if provided
    if additional_metadata:
        for key, value in additional_metadata.items():
            final_metadata[key] = value

    # Save metadata to file
    file_path = metadata_dir / f"{design_id}.json"
    with open(file_path, "w") as f:
        json.dump(final_metadata, f, indent=2)

    return str(file_path)


def load_design_metadata(file_path: str) -> Dict[str, Any]:
    """
    Load design metadata from a JSON file.

    Args:
        file_path: Path to the JSON file containing design metadata

    Returns:
        Dictionary containing the design metadata
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(
            f"Error loading design metadata from "
            f"{file_path}: {str(e)}"
        )
        return {}


def download_file(
        url: str,
        output_path: str,
        show_progress: bool = True
) -> str:
    """
    Download a file from a URL to a local path.

    Args:
        url: URL of the file to download.
        output_path: Path where the file should be saved.
        show_progress: Whether to show a progress bar.

    Returns:
        Path to the downloaded file.
    """
    # Create directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Download the file with progress bar
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Get file size if available
    file_size = int(response.headers.get("content-length", 0))

    # Create progress bar
    desc = os.path.basename(output_path)
    progress = tqdm(
        total=file_size,
        unit="B",
        unit_scale=True,
        desc=desc,
        disable=not
        show_progress
    )

    # Download with progress updates
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.update(len(chunk))

    progress.close()
    return output_path


def open_in_browser(url_or_file: str) -> None:
    """
    Open a URL or file in the default web browser.

    Args:
        url_or_file: URL or path to the file to open.
    """
    try:
        # If it's a file, get the absolute path and convert to file:// URL
        if os.path.exists(url_or_file):
            url_or_file = os.path.abspath(url_or_file)
            url_or_file = f"file://{url_or_file}"

        # Open in browser
        webbrowser.open(url_or_file)
    except Exception as e:
        print(
            f"Failed to open {url_or_file} in browser. "
            f"Error: {str(e)}"
        )
