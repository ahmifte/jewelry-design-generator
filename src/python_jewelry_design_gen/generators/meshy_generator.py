"""Jewelry design generator using Meshy.ai API."""

import logging
import concurrent.futures
from typing import List, Optional, Callable
from pathlib import Path

from python_jewelry_design_gen.generators.meshy_api import (
    MeshyAPI,
    MeshyAPIError
)
from python_jewelry_design_gen.models.jewelry_design import (
    JewelryDesign,
    Material,
    JewelryType,
    ChainStyle,
)
from python_jewelry_design_gen.utils.config import load_config
from python_jewelry_design_gen.utils.file_utils import (
    save_design_metadata,
    generate_batch_id,
)

# Set up logging
logger = logging.getLogger(__name__)


class JewelryGenerationError(Exception):
    """Exception raised for errors in jewelry generation."""

    pass


class MeshyJewelryGenerator:
    """Generator for creating jewelry designs using Meshy API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_client: Optional[MeshyAPI] = None,
        mock_mode: bool = False
    ):
        """
        Initialize the jewelry generator.

        Args:
            api_key: Meshy API key.
                - If not provided, it will be loaded from config.
            api_client: Optional pre-configured MeshyAPI client.
            mock_mode: If True, use mock data instead of calling API.
        """
        self.config = load_config()
        self.mock_mode = mock_mode
        self.api = api_client if api_client else MeshyAPI(api_key=api_key)

    def generate_design(
        self,
        design: Optional[JewelryDesign] = None,
        material: Optional[Material] = None,
        jewelry_type: Optional[JewelryType] = None,
        chain_style: Optional[ChainStyle] = None,
        custom_prompt: Optional[str] = None,
        custom_texture_prompt: Optional[str] = None,
        output_dir: Optional[str] = None,
        formats: List[str] = None,
        wait_for_completion: bool = True,
        progress_callback: Optional[Callable[[int, str, str], None]] = None,
        timeout: Optional[float] = None,
    ) -> JewelryDesign:
        """
        Generate a single jewelry design.

        Args:
            design: Pre-configured JewelryDesign object. If provided,
                other design parameters will be ignored.
            material: Material to use for the design.
            jewelry_type: Type of jewelry to generate.
            chain_style: Style of chain (for chain-based jewelry).
            custom_prompt: Custom text prompt for generation.
            custom_texture_prompt: Custom prompt for texturing.
            output_dir: Directory to save model files.
            formats: List of model formats to download (glb, fbx, obj, usdz).
            wait_for_completion: Whether to wait for task completion.
            progress_callback: Callback for progress updates.
            timeout: Maximum time to wait for completion in seconds.

        Returns:
            The generated JewelryDesign object with model URLs.

        Raises:
            JewelryGenerationError: If generation fails.
        """
        # Get configuration values
        if formats is None:
            formats = ["glb", "fbx"]

        if output_dir is None:
            output_dir = self.config.get("models_dir", "output/models")

        # Create or use provided design
        if not design:
            design = JewelryDesign(
                material=material
                or Material(self.config.get("default_material", "gold")),
                jewelry_type=jewelry_type
                or JewelryType(
                    self.config.get("default_jewelry_type", "chain")
                ),
                chain_style=chain_style
                or (
                    ChainStyle(self.config.get("default_chain_style", "cuban"))
                    if jewelry_type
                    in [
                        JewelryType.CHAIN,
                        JewelryType.BRACELET,
                        JewelryType.NECKLACE
                    ] or not jewelry_type
                    else None
                ),
            )

        # If mock mode is enabled, return mock data without making API calls
        if self.mock_mode:
            logger.info(
                "Using mock mode - returning mock data without API calls")

            # Create output directory for consistency
            design_output_dir = Path(output_dir) / design.id
            design_output_dir.mkdir(parents=True, exist_ok=True)

            # Set mock model URLs
            design.model_urls = {
                fmt: f"https://mock.example.com/{design.id}.{fmt}"
                for fmt in formats
            }
            design.thumbnail_url = (
                f"https://mock.example.com/{design.id}_thumbnail.png"
            )
            design.texture_urls = [
                {
                    "base_color": (
                        f"https://mock.example.com/{design.id}_texture_0.png"
                    ),
                    "normal": (
                        f"https://mock.example.com/"
                        f"{design.id}_texture_0_normal.png"
                    )
                }
            ]

            # Save metadata
            save_design_metadata(
                design.id,
                design.to_dict(),
                self.config.get("metadata_dir", "output/metadata"),
            )

            # Trigger progress callback if provided
            if progress_callback:
                progress_callback(100, "MOCK_COMPLETED", "complete")

            logger.info(f"Mock design {design.id} generated successfully")
            return design

        # Create design-specific output directory
        design_output_dir = Path(output_dir) / design.id
        design_output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Generate text prompt if not provided
            prompt = custom_prompt or design.get_prompt()
            logger.info(f"Generating design with prompt: {prompt}")

            # Create preview task
            preview_task_id = self.api.create_text_to_3d_preview(
                prompt=prompt,
                art_style=self.config.get("art_style", "realistic"),
                should_remesh=self.config.get("should_remesh", True),
                topology=self.config.get("topology", "quad"),
                target_polycount=self.config.get("target_polycount", 100000),
                symmetry_mode=self.config.get("symmetry_mode", "on"),
                ai_model=self.config.get("ai_model", "meshy-4"),
            )

            logger.info(f"Preview task created: {preview_task_id}")

            if wait_for_completion:
                # Wait for preview to complete and get the task result
                def preview_progress_cb(progress, status):
                    if progress_callback:
                        progress_callback(
                            progress // 2,  # Preview is first half of progress
                            status,
                            "preview",
                        )

                self.api.wait_for_task_completion(
                    preview_task_id,
                    polling_interval=5.0,
                    timeout=timeout,
                    progress_callback=preview_progress_cb,
                )

                logger.info("Preview task completed, creating refine task")

                # Create refine task
                texture_prompt = custom_texture_prompt
                if not texture_prompt:
                    texture_prompt = (
                        f"{design.material} material, jewelry quality, "
                        f"detailed surface finish"
                    )

                refine_task_id = self.api.create_text_to_3d_refine(
                    preview_task_id=preview_task_id,
                    enable_pbr=self.config.get("enable_pbr", True),
                    texture_prompt=texture_prompt,
                )

                logger.info(f"Refine task created: {refine_task_id}")

                # Wait for refine to complete
                def refine_progress_cb(progress, status):
                    if progress_callback:
                        progress_callback(
                            # Refine is second half of progress
                            50 + progress // 2,
                            status,
                            "refine",
                        )

                refine_task = self.api.wait_for_task_completion(
                    refine_task_id,
                    polling_interval=5.0,
                    timeout=timeout,
                    progress_callback=refine_progress_cb,
                )

                # Download the model files and proceed
                logger.info(f"Downloading model files to {design_output_dir}")
                self.api.download_3d_model(
                    refine_task,
                    str(design_output_dir),
                    formats=formats,
                    download_textures=True,
                    show_progress=True,
                )

                # Update design with model information
                design.model_urls = refine_task.get("model_urls", {})
                design.texture_urls = refine_task.get("texture_urls", [])
                design.thumbnail_url = refine_task.get("thumbnail_url")

                # Save metadata
                save_design_metadata(
                    design.id,
                    design.to_dict(),
                    self.config.get("metadata_dir", "output/metadata"),
                )

                logger.info(
                    f"Design {design.id} generation completed successfully")

                if progress_callback:
                    progress_callback(100, "SUCCEEDED", "complete")
            else:
                # Just return the design with the task ID
                design.description = f"Preview task ID: {preview_task_id}"

            return design

        except (MeshyAPIError, Exception) as e:
            logger.error(f"Error generating design: {e}")
            raise JewelryGenerationError(
                f"Failed to generate design: {str(e)}") from e

    def generate_batch(
        self,
        batch_size: int = None,
        material: Optional[Material] = None,
        jewelry_type: Optional[JewelryType] = None,
        chain_style: Optional[ChainStyle] = None,
        output_dir: Optional[str] = None,
        formats: List[str] = None,
        max_workers: int = None,
        progress_callback: Optional[Callable[[
            int, str, JewelryDesign], None]] = None,
    ) -> List[JewelryDesign]:
        """
        Generate a batch of jewelry designs in parallel.

        Args:
            batch_size: Number of designs to generate.
            material: Material to use for the designs.
            jewelry_type: Type of jewelry to generate.
            chain_style: Style of chain for chain-based jewelry.
            output_dir: Directory to save model files.
            formats: List of model formats to download.
            max_workers: Maximum number of parallel generation tasks.
            progress_callback: Callback for progress updates.

        Returns:
            List of generated JewelryDesign objects.

        Raises:
            JewelryGenerationError: If batch generation fails.
        """
        # Use values from config if not specified
        if batch_size is None:
            batch_size = self.config.get("default_batch_size", 10)

        if max_workers is None:
            max_workers = self.config.get("max_workers", 3)

        batch_id = generate_batch_id()
        designs = []

        logger.info(
            f"Starting batch generation: {batch_id} with {batch_size} designs")

        # Create design objects
        for _ in range(batch_size):
            design = JewelryDesign(
                material=material
                or Material(self.config.get("default_material", "gold")),
                jewelry_type=jewelry_type
                or JewelryType(
                    self.config.get("default_jewelry_type", "chain")
                ),
                chain_style=chain_style
                or (
                    ChainStyle(self.config.get("default_chain_style", "cuban"))
                    if jewelry_type in [
                        JewelryType.CHAIN,
                        JewelryType.BRACELET,
                        JewelryType.NECKLACE
                    ] or not jewelry_type
                    else None
                ),
                batch_id=batch_id,
            )
            designs.append(design)

        completed_designs = []
        failed_designs = []

        def design_progress_callback(
            progress: int, status: str, stage: str, design: JewelryDesign
        ):
            if progress_callback:
                progress_callback(progress, status, design)

        # Generate designs in parallel
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:
            futures = {}

            for design in designs:
                future = executor.submit(
                    self.generate_design,
                    design=design,
                    output_dir=output_dir,
                    formats=formats,
                    wait_for_completion=True,
                    progress_callback=lambda p, s, st, d=design: (
                        design_progress_callback(p, s, st, d)
                    ),
                )
                futures[future] = design

            # Process results as they complete
            for future in concurrent.futures.as_completed(futures):
                design = futures[future]
                try:
                    completed_design = future.result()
                    completed_designs.append(completed_design)
                    logger.info(f"Design {design.id} completed successfully")
                except Exception as e:
                    logger.error(f"Design {design.id} failed: {e}")
                    failed_designs.append(design)

        if failed_designs:
            logger.warning(
                f"Batch {batch_id} completed with "
                f"{len(failed_designs)} failures"
            )
        else:
            logger.info(f"Batch {batch_id} completed successfully")

        return completed_designs
