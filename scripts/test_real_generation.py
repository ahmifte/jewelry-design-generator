#!/usr/bin/env python
"""
Generates jewelry designs with enhanced prompts and opens in browser.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Optional

from python_jewelry_design_gen.generators.meshy_generator import (
    MeshyJewelryGenerator,
)
from python_jewelry_design_gen.models.jewelry_design import ChainStyle
from python_jewelry_design_gen.models.jewelry_design import JewelryType
from python_jewelry_design_gen.models.jewelry_design import Material
from python_jewelry_design_gen.utils.config import load_config
from python_jewelry_design_gen.utils.file_utils import open_in_browser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def generate_and_open(
    material: Material,
    jewelry_type: JewelryType,
    chain_style: ChainStyle | None = None,
    custom_prompt: str | None = None,
    formats: list = None,
):
    """Generate a jewelry design and open it in the browser."""
    if formats is None:
        formats = ['glb', 'fbx']

    config = load_config()
    output_dir = config.get('models_dir', 'output/models')

    logger.info(f'Generating {material} {jewelry_type}...')
    generator = MeshyJewelryGenerator(mock_mode=False)

    def update_progress(progress, status, stage):
        logger.info(f'Progress: {progress}% - {stage}: {status}')

    design = generator.generate_design(
        material=material,
        jewelry_type=jewelry_type,
        chain_style=chain_style,
        custom_prompt=custom_prompt,
        output_dir=output_dir,
        formats=formats,
        progress_callback=update_progress,
    )
    logger.info(f'Design generated: {design.id} - {design.display_name}')
    logger.info('Enhanced prompt used:')
    logger.info(design.get_prompt())
    time.sleep(2)

    output_path = Path(output_dir)
    design_path = output_path / design.id
    thumbnail_path = design_path / 'thumbnail.png'

    if thumbnail_path.exists():
        logger.info(f'Opening thumbnail in browser: {thumbnail_path}')
        open_in_browser(str(thumbnail_path))
    elif 'glb' in design.model_urls:
        logger.info(
            f"Opening GLB model in browser: {design.model_urls['glb']}",
        )
        open_in_browser(design.model_urls['glb'])
    elif design.model_urls:
        first_format = next(iter(design.model_urls))
        url = design.model_urls[first_format]
        logger.info(f'Opening {first_format.upper()} model in browser: {url}')
        open_in_browser(url)
    else:
        logger.warning('No viewable files found to open in browser.')

    return design


def main():
    """Run tests generating several different jewelry designs."""
    config = load_config()
    if not config.get('meshy_api_key'):
        logger.error(
            'Meshy API key not found. Set the MESHY_API_KEY '
            'environment variable or add it to config.json.',
        )
        return 1

    test_cases = [
        # A ring
        {
            'material': Material.PLATINUM,
            'jewelry_type': JewelryType.RING,
        },
        # A chain with specific style
        {
            'material': Material.GOLD,
            'jewelry_type': JewelryType.CHAIN,
            'chain_style': ChainStyle.CUBAN,
        },
        # A pendant
        {
            'material': Material.SILVER,
            'jewelry_type': JewelryType.PENDANT,
        },
    ]

    generated_designs = []
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f'\nGenerating test case {i}/{len(test_cases)}:')
        for key, value in test_case.items():
            logger.info(f'  {key}: {value}')

        try:
            design = generate_and_open(**test_case)
            generated_designs.append(design)
            if i < len(test_cases):
                logger.info('Waiting 5 seconds before next generation...')
                time.sleep(5)
        except Exception as e:
            logger.error(f'Error generating design: {e}')

    for i, design in enumerate(generated_designs, 1):
        logger.info(f'{i}. {design.display_name} (ID: {design.id})')
        if design.model_urls:
            for fmt, url in design.model_urls.items():
                logger.info(f'   {fmt.upper()}: {url}')

    return 0


if __name__ == '__main__':
    main()
