"""Command-line interface for the jewelry design generator."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Optional

import click
from python_jewelry_design_gen.generators.meshy_generator import (
    MeshyJewelryGenerator,
)
from python_jewelry_design_gen.models.jewelry_design import ChainStyle
from python_jewelry_design_gen.models.jewelry_design import JewelryType
from python_jewelry_design_gen.models.jewelry_design import Material
from python_jewelry_design_gen.utils.config import load_config
from python_jewelry_design_gen.utils.file_utils import load_design_metadata
from python_jewelry_design_gen.utils.file_utils import open_in_browser
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Jewelry design generator using AI."""
    pass


@cli.command()
@click.option(
    '--material',
    type=click.Choice([m.value for m in Material]),
    help='Material for the jewelry design.',
)
@click.option(
    '--type',
    'jewelry_type',
    type=click.Choice([t.value for t in JewelryType]),
    help='Type of jewelry to generate.',
)
@click.option(
    '--chain-style',
    type=click.Choice([s.value for s in ChainStyle]),
    help='Style of chain (for chain-based jewelry).',
)
@click.option(
    '--prompt',
    type=str,
    help='Custom prompt for generation instead of auto-generated prompt.',
)
@click.option(
    '--texture-prompt', type=str, help='Custom prompt for texturing the model.',
)
@click.option(
    '--output-dir',
    type=click.Path(file_okay=False),
    help='Output directory for generated models.',
)
@click.option(
    '--formats',
    type=str,
    default='glb,fbx',
    help='Comma-separated list of output formats (glb,fbx,obj,usdz).',
)
@click.option(
    '--open-browser',
    is_flag=True,
    help='Open the generated model thumbnail in browser after completion.',
)
@click.option(
    '--mock',
    is_flag=True,
    help='Use mock mode without making actual API calls.',
)
def generate(
    material: str | None,
    jewelry_type: str | None,
    chain_style: str | None,
    prompt: str | None,
    texture_prompt: str | None,
    output_dir: str | None,
    formats: str,
    open_browser: bool,
    mock: bool,
):
    """Generate a single jewelry design."""
    try:
        # Load configuration
        config = load_config()

        # Parse material and type options
        material_enum = Material(material) if material else None
        type_enum = JewelryType(jewelry_type) if jewelry_type else None
        chain_style_enum = ChainStyle(chain_style) if chain_style else None

        # Parse formats
        format_list = formats.split(',') if formats else ['glb', 'fbx']

        # Create generator
        generator = MeshyJewelryGenerator(mock_mode=mock)

        # Progress bar setup
        progress_bar = tqdm(total=100, desc='Generating design')

        def update_progress(prog, status, stage):
            progress_bar.update(prog - progress_bar.n)
            progress_bar.set_description(
                f'Generating design ({stage}: {status})',
            )

        # Generate design
        design = generator.generate_design(
            material=material_enum,
            jewelry_type=type_enum,
            chain_style=chain_style_enum,
            custom_prompt=prompt,
            custom_texture_prompt=texture_prompt,
            output_dir=output_dir,
            formats=format_list,
            progress_callback=update_progress,
        )

        progress_bar.close()

        # Print results
        click.echo('\nDesign generated successfully!')
        click.echo(f'Design ID: {design.id}')
        click.echo(f'Name: {design.display_name}')

        if design.model_urls:
            click.echo('\nModel URLs:')
            for fmt, url in design.model_urls.items():
                click.echo(f'  {fmt.upper()}: {url}')

        output_path = Path(
            output_dir or config.get(
                'models_dir', 'output/models',
            ),
        )
        design_path = output_path / design.id

        click.echo(f'\nFiles saved to: {design_path}')

        # Open the thumbnail or model in browser if requested
        if open_browser:
            # First try to open the thumbnail
            thumbnail_path = design_path / 'thumbnail.png'
            if thumbnail_path.exists():
                click.echo('Opening thumbnail in browser...')
                open_in_browser(str(thumbnail_path))
            # If no thumbnail, try to open a GLB model with a viewer
            elif 'glb' in design.model_urls:
                click.echo('Opening GLB model in browser...')
                open_in_browser(design.model_urls['glb'])
            # If no GLB, try the first available model URL
            elif design.model_urls:
                first_format = next(iter(design.model_urls))
                click.echo(
                    f'Opening {first_format.upper()} model in browser...',
                )
                open_in_browser(design.model_urls[first_format])
            else:
                click.echo('No viewable files found to open in browser.')

        return 0

    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        logger.exception('Error generating design')
        return 1


@cli.command()
@click.option(
    '--material',
    type=click.Choice([m.value for m in Material]),
    help='Material for the jewelry designs.',
)
@click.option(
    '--type',
    'jewelry_type',
    type=click.Choice([t.value for t in JewelryType]),
    help='Type of jewelry to generate.',
)
@click.option(
    '--chain-style',
    type=click.Choice([s.value for s in ChainStyle]),
    help='Style of chain (for chain-based jewelry).',
)
@click.option(
    '--batch-size',
    type=int,
    default=10,
    help='Number of designs to generate in the batch.',
)
@click.option(
    '--max-workers',
    type=int,
    default=3,
    help='Maximum number of parallel generation tasks.',
)
@click.option(
    '--output-dir',
    type=click.Path(file_okay=False),
    help='Output directory for generated models.',
)
@click.option(
    '--formats',
    type=str,
    default='glb,fbx',
    help='Comma-separated list of output formats (glb,fbx,obj,usdz).',
)
@click.option(
    '--open-browser',
    is_flag=True,
    help="Open the first completed design's thumbnail in browser.",
)
@click.option(
    '--mock',
    is_flag=True,
    help='Use mock mode without making actual API calls.',
)
def batch(
    material: str | None,
    jewelry_type: str | None,
    chain_style: str | None,
    batch_size: int,
    max_workers: int,
    output_dir: str | None,
    formats: str,
    open_browser: bool,
    mock: bool,
):
    """Generate a batch of jewelry designs in parallel."""
    try:
        # Load configuration
        config = load_config()

        # Parse material and type options
        material_enum = Material(material) if material else None
        type_enum = JewelryType(jewelry_type) if jewelry_type else None
        chain_style_enum = ChainStyle(chain_style) if chain_style else None

        # Parse formats
        format_list = formats.split(',') if formats else ['glb', 'fbx']

        # Create generator
        generator = MeshyJewelryGenerator(mock_mode=mock)

        # Track progress of each design
        design_progress = {}
        first_completed_design = None

        def update_progress(progress, status, design):
            design_id = design.id
            if design_id not in design_progress:
                design_progress[design_id] = {
                    'progress': 0, 'status': 'PENDING',
                }

            design_progress[design_id]['progress'] = progress
            design_progress[design_id]['status'] = status

            # Calculate overall progress
            total_progress = sum(
                d['progress']
                for d in design_progress.values()
            )
            avg_progress = total_progress / batch_size

            # Update display
            completed = sum(
                1 for d in design_progress.values()
                if d['progress'] == 100
            )
            click.echo(
                f'\rGenerating {batch_size} designs: '
                f'{avg_progress:.1f}% complete '
                f'({completed}/{batch_size} finished)',
                nl=False,
            )

            # Track the first completed design
            nonlocal first_completed_design
            if (
                progress == 100
                and status == 'SUCCEEDED'
                    and first_completed_design is None
            ):
                first_completed_design = design

        click.echo(f'Starting batch generation of {batch_size} designs...')

        # Generate designs
        designs = generator.generate_batch(
            batch_size=batch_size,
            material=material_enum,
            jewelry_type=type_enum,
            chain_style=chain_style_enum,
            output_dir=output_dir,
            formats=format_list,
            max_workers=max_workers,
            progress_callback=update_progress,
        )

        click.echo('\n\nBatch generation completed!')
        click.echo(f'Generated {len(designs)} designs')

        # Print summary
        for i, design in enumerate(designs):
            click.echo(
                f'\nDesign {i+1}: {design.display_name} (ID: {design.id})',
            )

        output_path = Path(
            output_dir or config.get(
                'models_dir', 'output/models',
            ),
        )
        click.echo(f'\nFiles saved to: {output_path}')

        # Open the first design in browser if requested
        if open_browser and designs:
            design_to_open = first_completed_design or designs[0]
            design_path = output_path / design_to_open.id
            thumbnail_path = design_path / 'thumbnail.png'

            if thumbnail_path.exists():
                click.echo(
                    f'Opening thumbnail for design '
                    f'{design_to_open.id} in browser...',
                )
                open_in_browser(str(thumbnail_path))
            elif 'glb' in design_to_open.model_urls:
                click.echo(
                    f'Opening GLB model for design '
                    f'{design_to_open.id} in browser...',
                )
                open_in_browser(design_to_open.model_urls['glb'])
            elif design_to_open.model_urls:
                first_format = next(iter(design_to_open.model_urls))
                click.echo(
                    f'Opening {first_format.upper()} model '
                    f'for design {design_to_open.id} in browser...',
                )
                open_in_browser(design_to_open.model_urls[first_format])
            else:
                click.echo('No viewable files found to open in browser.')

        return 0

    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        logger.exception('Error generating batch')
        return 1


@cli.command()
@click.argument('design_id', required=True)
@click.option(
    '--metadata-dir',
    type=click.Path(file_okay=False),
    help='Directory containing design metadata files.',
)
@click.option(
    '--open-browser',
    is_flag=True,
    help='Open the design thumbnail or model in browser.',
)
def info(design_id: str, metadata_dir: str | None, open_browser: bool):
    """Display information about a generated design."""
    try:
        # Load configuration
        config = load_config()

        # Determine metadata directory
        if metadata_dir is None:
            metadata_dir = config.get('metadata_dir', 'output/metadata')

        # Load metadata
        metadata_path = Path(metadata_dir) / f'{design_id}.json'
        if not metadata_path.exists():
            click.echo(f'Error: Design {design_id} not found', err=True)
            return 1

        metadata = load_design_metadata(str(metadata_path))

        # Display metadata
        click.echo(f"Design ID: {metadata.get('id')}")
        click.echo(f"Name: {metadata.get('name')}")
        click.echo(f"Type: {metadata.get('jewelry_type')}")
        click.echo(f"Material: {metadata.get('material')}")

        if metadata.get('chain_style'):
            click.echo(f"Chain Style: {metadata.get('chain_style')}")

        click.echo(f"Created: {metadata.get('created_at')}")

        if metadata.get('batch_id'):
            click.echo(f"Batch ID: {metadata.get('batch_id')}")

        if metadata.get('model_urls'):
            click.echo('\nModel URLs:')
            for fmt, url in metadata.get('model_urls', {}).items():
                click.echo(f'  {fmt.upper()}: {url}')

        if metadata.get('dimensions'):
            click.echo('\nDimensions:')
            for dim, value in metadata.get('dimensions', {}).items():
                click.echo(f'  {dim}: {value}')

        # Open in browser if requested
        if open_browser:
            models_dir = config.get('models_dir', 'output/models')
            design_path = Path(models_dir) / design_id
            thumbnail_path = design_path / 'thumbnail.png'

            if thumbnail_path.exists():
                click.echo('Opening thumbnail in browser...')
                open_in_browser(str(thumbnail_path))
            elif metadata.get('model_urls', {}).get('glb'):
                click.echo('Opening GLB model in browser...')
                open_in_browser(metadata.get('model_urls').get('glb'))
            elif metadata.get('model_urls'):
                first_format = next(iter(metadata.get('model_urls')))
                click.echo(
                    f'Opening {first_format.upper()} model in browser...',
                )
                open_in_browser(metadata.get('model_urls').get(first_format))
            else:
                click.echo('No viewable files found to open in browser.')

        return 0

    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        logger.exception('Error displaying design info')
        return 1


@cli.command()
@click.option(
    '--output',
    type=click.Path(dir_okay=False),
    help='Output file to write the example config (defaults to config.json).',
)
def init(output: str | None):
    """Initialize a config file with default settings."""
    try:
        # Load default configuration
        config = load_config()

        # Add default settings that might not be in environment
        config.update(
            {
                'meshy_api_key': 'YOUR_MESHY_API_KEY_HERE',
                'meshy_api_base_url': 'https://api.meshy.ai',
                'output_dir': 'output',
                'models_dir': 'output/models',
                'metadata_dir': 'output/metadata',
                'default_material': 'gold',
                'default_jewelry_type': 'chain',
                'default_chain_style': 'cuban',
                'default_batch_size': 10,
                'enable_pbr': True,
                'art_style': 'realistic',
                'symmetry_mode': 'on',
                'should_remesh': True,
                'topology': 'quad',
                'target_polycount': 100000,
                'ai_model': 'meshy-4',
            },
        )

        # Write to file
        output_path = output or 'config.json'
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)

        click.echo(f'Configuration saved to {output_path}')
        click.echo('Remember to update the API key in the configuration file.')

        # Create example .env file if it doesn't exist
        env_example_path = Path('.env.example')
        env_path = Path('.env')

        if env_example_path.exists() and not env_path.exists():
            click.echo('Creating .env file from .env.example...')
            with (
                open(env_example_path) as src,
                open(env_path, 'w') as dst,
            ):
                dst.write(src.read())
            click.echo(
                'Created .env file. Remember to update it with your API key.',
            )

        return 0

    except Exception as e:
        click.echo(f'Error: {e}', err=True)
        logger.exception('Error initializing config')
        return 1


if __name__ == '__main__':
    sys.exit(cli())
