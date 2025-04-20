"""
Basic test file to verify module importing and test discovery.
"""
from __future__ import annotations

from pathlib import Path

import src.python_jewelry_design_gen
from src.python_jewelry_design_gen.models.jewelry_design import JewelryDesign
from src.python_jewelry_design_gen.models.jewelry_design import JewelryType
from src.python_jewelry_design_gen.models.jewelry_design import Material


def test_module_imports():
    """Test that the module can be imported successfully."""
    assert src.python_jewelry_design_gen is not None


def test_jewelry_design_creation():
    """Test basic jewelry design creation."""
    design = JewelryDesign(
        jewelry_type=JewelryType.RING,
        material=Material.GOLD,
    )
    assert design is not None
    assert design.jewelry_type == JewelryType.RING
    assert design.material == Material.GOLD
    assert design.display_name is not None


def test_project_structure():
    """Verify the project structure exists as expected."""
    src_dir = Path('src/python_jewelry_design_gen')
    assert src_dir.exists(), 'Source directory not found'
    assert (src_dir / '__init__.py').exists(), 'Package __init__.py not found'

    # Check for key subdirectories
    assert (src_dir / 'models').exists(), 'Models directory not found'
    assert (src_dir / 'generators').exists(), 'Generators directory not found'
    assert (src_dir / 'utils').exists(), 'Utils directory not found'
