import pytest
from datetime import datetime

from python_jewelry_design_gen.models.jewelry_design import (
    JewelryDesign,
    Material,
    JewelryType,
    ChainStyle,
)


class TestJewelryDesign:
    """Tests for the JewelryDesign class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        design = JewelryDesign()
        assert design.id is not None
        assert design.material == Material.GOLD
        assert design.jewelry_type == JewelryType.CHAIN
        assert design.chain_style == ChainStyle.CUBAN  # Set in __post_init__

    def test_custom_initialization(self):
        """Test initialization with custom values."""
        design = JewelryDesign(
            id="test-id",
            name="Test Design",
            material=Material.SILVER,
            jewelry_type=JewelryType.RING,
            chain_style=None,  # No chain style for rings
        )
        assert design.id == "test-id"
        assert design.name == "Test Design"
        assert design.material == Material.SILVER
        assert design.jewelry_type == JewelryType.RING
        assert design.chain_style is None

    def test_display_name(self):
        """Test the display_name property."""
        # With custom name
        design = JewelryDesign(name="Custom Name")
        assert design.display_name == "Custom Name"

        # Without custom name
        design = JewelryDesign(
            name="",
            material=Material.SILVER,
            jewelry_type=JewelryType.RING,
        )
        assert design.display_name == "Silver Ring"

        # With chain style
        design = JewelryDesign(
            name="",
            material=Material.GOLD,
            jewelry_type=JewelryType.CHAIN,
            chain_style=ChainStyle.CUBAN,
        )
        assert design.display_name == "Cuban Gold Chain"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        design = JewelryDesign(
            id="test-id",
            name="Test Design",
            material=Material.GOLD,
            jewelry_type=JewelryType.BRACELET,
            chain_style=ChainStyle.ROPE,
        )

        data = design.to_dict()
        assert data["id"] == "test-id"
        assert data["name"] == "Test Design"
        assert data["material"] == "gold"
        assert data["jewelry_type"] == "bracelet"
        assert data["chain_style"] == "rope"

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "id": "test-id",
            "name": "Test Design",
            "material": "silver",
            "jewelry_type": "ring",
            "chain_style": None,
            "created_at": datetime.now().isoformat(),
        }

        design = JewelryDesign.from_dict(data)
        assert design.id == "test-id"
        assert design.name == "Test Design"
        assert design.material == Material.SILVER
        assert design.jewelry_type == JewelryType.RING
        assert design.chain_style is None

    def test_get_prompt(self):
        """Test prompt generation."""
        # Test chain prompt
        chain = JewelryDesign(
            material=Material.GOLD,
            jewelry_type=JewelryType.CHAIN,
            chain_style=ChainStyle.CUBAN,
        )
        chain_prompt = chain.get_prompt()
        assert "gold chain" in chain_prompt.lower()
        assert "cuban style links" in chain_prompt.lower()

        # Test ring prompt
        ring = JewelryDesign(
            material=Material.SILVER,
            jewelry_type=JewelryType.RING,
        )
        ring_prompt = ring.get_prompt()
        assert "silver ring" in ring_prompt.lower()
        assert "round band" in ring_prompt.lower()

        # Test earring prompt
        earring = JewelryDesign(
            material=Material.PLATINUM,
            jewelry_type=JewelryType.EARRING,
        )
        earring_prompt = earring.get_prompt()
        assert "platinum earring" in earring_prompt.lower()
        assert "ear hook" in earring_prompt.lower()
