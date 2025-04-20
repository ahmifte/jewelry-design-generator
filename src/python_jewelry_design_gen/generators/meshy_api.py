"""Client for the Meshy.ai API."""

import requests
import time
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
import json

from python_jewelry_design_gen.utils.config import (
    get_meshy_api_key,
    load_config
)
from python_jewelry_design_gen.utils.file_utils import download_file

# Set up logging
logger = logging.getLogger(__name__)


class MeshyAPIError(Exception):
    """Exception raised for errors in the Meshy API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class MeshyAPI:
    """Client for the Meshy.ai API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize the Meshy API client.
        Args:
            api_key: Meshy API key. If not provided, it will be loaded from
                config.
            base_url: Base URL for the Meshy API. If not provided, it will be
                loaded from config.
        """
        config = load_config()

        self.api_key = api_key or get_meshy_api_key()
        self.base_url = base_url or config.get(
            "meshy_api_base_url", "https://api.meshy.ai"
        )

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_text_to_3d_preview(
        self,
        prompt: str,
        art_style: str = "realistic",
        should_remesh: bool = True,
        topology: str = "quad",
        target_polycount: int = 100000,
        symmetry_mode: str = "on",
        seed: Optional[int] = None,
        ai_model: str = "meshy-4",
    ) -> str:
        """
        Create a Text to 3D Preview task.

        Args:
            prompt: Text description of what to generate.
            art_style: Art style to use (realistic, sculpture).
            should_remesh: Whether to enable the remesh phase.
            topology: Topology of the generated model (quad, triangle).
            target_polycount: Target number of polygons.
            symmetry_mode: Symmetry behavior (off, auto, on).
            seed: Random seed for generation.
            ai_model: AI model to use.

        Returns:
            Task ID of the preview task.

        Raises:
            MeshyAPIError: If the API request fails.
        """
        endpoint = f"{self.base_url}/openapi/v2/text-to-3d"

        payload = {
            "mode": "preview",
            "prompt": prompt,
            "art_style": art_style,
            "should_remesh": should_remesh,
            "topology": topology,
            "target_polycount": target_polycount,
            "symmetry_mode": symmetry_mode,
            "ai_model": ai_model,
        }

        # Add optional fields if provided
        if seed is not None:
            payload["seed"] = seed

        try:
            response = requests.post(
                endpoint, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json().get("result")
            if not result:
                raise MeshyAPIError(
                    "No task ID returned in response", response=response.json()
                )

            return result

        except requests.RequestException as e:
            status_code = e.response.status_code if hasattr(
                e, "response") else None
            response_data = None

            if hasattr(e, "response") and e.response is not None:
                try:
                    response_data = e.response.json()
                except (ValueError, json.JSONDecodeError):
                    response_data = {"raw": e.response.text}

            raise MeshyAPIError(
                f"Error creating preview task: {str(e)}",
                status_code=status_code,
                response=response_data,
            ) from e

    def create_text_to_3d_refine(
        self,
        preview_task_id: str,
        enable_pbr: bool = True,
        texture_prompt: Optional[str] = None,
    ) -> str:
        """
        Create a Text to 3D Refine task.

        Args:
            preview_task_id: ID of the preview task.
            enable_pbr: Whether to generate PBR maps.
            texture_prompt: Additional prompt for texturing.

        Returns:
            Task ID of the refine task.

        Raises:
            MeshyAPIError: If the API request fails.
        """
        endpoint = f"{self.base_url}/openapi/v2/text-to-3d"

        payload = {
            "mode": "refine",
            "preview_task_id": preview_task_id,
            "enable_pbr": enable_pbr,
        }

        # Add optional fields if provided
        if texture_prompt:
            payload["texture_prompt"] = texture_prompt

        try:
            response = requests.post(
                endpoint, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json().get("result")
            if not result:
                raise MeshyAPIError(
                    "No task ID returned in response", response=response.json()
                )

            return result

        except requests.RequestException as e:
            status_code = e.response.status_code if hasattr(
                e, "response") else None
            response_data = None

            if hasattr(e, "response") and e.response is not None:
                try:
                    response_data = e.response.json()
                except (ValueError, json.JSONDecodeError):
                    response_data = {"raw": e.response.text}

            raise MeshyAPIError(
                f"Error creating refine task: {str(e)}",
                status_code=status_code,
                response=response_data,
            ) from e

    def get_text_to_3d_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get details of a Text to 3D task.

        Args:
            task_id: ID of the task.

        Returns:
            Task details.

        Raises:
            MeshyAPIError: If the API request fails.
        """
        endpoint = f"{self.base_url}/openapi/v2/text-to-3d/{task_id}"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            status_code = e.response.status_code if hasattr(
                e, "response") else None
            response_data = None

            if hasattr(e, "response") and e.response is not None:
                try:
                    response_data = e.response.json()
                except (ValueError, json.JSONDecodeError):
                    response_data = {"raw": e.response.text}

            raise MeshyAPIError(
                f"Error getting task details: {str(e)}",
                status_code=status_code,
                response=response_data,
            ) from e

    def wait_for_task_completion(
        self,
        task_id: str,
        polling_interval: float = 5.0,
        timeout: Optional[float] = None,
        progress_callback=None,
    ) -> Dict[str, Any]:
        """
        Wait for a task to complete.

        Args:
            task_id: ID of the task.
            polling_interval: How often to check task status in seconds.
            timeout: Maximum time to wait in seconds. None for no timeout.
            progress_callback: Optional callback function for progress updates.

        Returns:
            Completed task details.

        Raises:
            MeshyAPIError: If the task fails or times out.
        """
        start_time = time.time()
        last_progress = -1

        while True:
            task = self.get_text_to_3d_task(task_id)
            status = task.get("status")
            progress = task.get("progress", 0)

            # Call progress callback if provided and progress has changed
            if progress_callback and progress != last_progress:
                progress_callback(progress, status)
                last_progress = progress

            # Check if task is complete
            if status == "SUCCEEDED":
                return task
            elif status == "FAILED" or status == "CANCELED":
                error_msg = "Task failed"
                task_error = task.get("task_error", {})
                if task_error and task_error.get("message"):
                    error_msg = task_error.get("message")

                raise MeshyAPIError(
                    f"Task failed with status {status}: {error_msg}",
                    response=task
                )

            # Check for timeout
            if timeout and (time.time() - start_time) > timeout:
                raise MeshyAPIError(
                    f"Task timed out after {timeout} seconds", response=task
                )

            # Wait before polling again
            time.sleep(polling_interval)

    def download_3d_model(
        self,
        task: Dict[str, Any],
        output_dir: str,
        formats: List[str] = ["glb"],
        download_textures: bool = True,
        show_progress: bool = True,
    ) -> Dict[str, str]:
        """
        Download 3D models and textures from a completed task.

        Args:
            task: Task details dictionary.
            output_dir: Directory to save downloaded files.
            formats: List of formats to download (glb, fbx, obj, usdz).
            download_textures: Whether to download texture files.
            show_progress: Whether to show download progress.

        Returns:
            Dictionary mapping format/texture to local file paths.

        Raises:
            MeshyAPIError: If downloads fail.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        downloaded_files = {}

        # Download model files
        if "model_urls" in task:
            for fmt in formats:
                if fmt in task["model_urls"]:
                    url = task["model_urls"][fmt]
                    filename = f"model.{fmt}"

                    if fmt == "obj" and "mtl" in task["model_urls"]:
                        # Also download MTL file for OBJ
                        mtl_url = task["model_urls"]["mtl"]
                        mtl_path = output_path / "model.mtl"
                        download_file(
                            mtl_url, str(mtl_path), show_progress=show_progress
                        )
                        downloaded_files["mtl"] = str(mtl_path)

                    output_file = output_path / filename
                    download_file(url, str(output_file),
                                  show_progress=show_progress)
                    downloaded_files[fmt] = str(output_file)

        # Download thumbnail if available
        if "thumbnail_url" in task and task["thumbnail_url"]:
            thumb_path = output_path / "thumbnail.png"
            download_file(task["thumbnail_url"], str(thumb_path),
                          show_progress=show_progress)
            downloaded_files["thumbnail"] = str(thumb_path)
        # Download textures if requested
        if (
            download_textures
            and "texture_urls" in task
            and task["texture_urls"]
        ):
            textures_dir = output_path / "textures"
            textures_dir.mkdir(exist_ok=True)

            for i, texture_set in enumerate(task["texture_urls"]):
                for tex_type, tex_url in texture_set.items():
                    filename = f"texture_{i}_{tex_type}.png"
                    if tex_type == "base_color":
                        # Base texture has simpler name
                        filename = f"texture_{i}.png"

                    tex_path = textures_dir / filename
                    download_file(tex_url, str(tex_path),
                                  show_progress=show_progress)
                    downloaded_files[f"texture_{i}_{tex_type}"] = str(tex_path)

        return downloaded_files
