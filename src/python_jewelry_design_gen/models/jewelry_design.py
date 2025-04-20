"""Jewelry design data models."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class Material(str, Enum):
    """Material types for jewelry designs."""

    GOLD = 'gold'
    SILVER = 'silver'
    STAINLESS_STEEL = 'stainless_steel'
    GOLD_PLATED = 'gold_plated'
    SILVER_PLATED = 'silver_plated'
    ROSE_GOLD = 'rose_gold'
    WHITE_GOLD = 'white_gold'
    PLATINUM = 'platinum'
    BRASS = 'brass'

    def __str__(self) -> str:
        return self.value


class JewelryType(str, Enum):
    """Types of jewelry that can be generated."""

    CHAIN = 'chain'
    RING = 'ring'
    BRACELET = 'bracelet'
    NECKLACE = 'necklace'
    EARRING = 'earring'
    PENDANT = 'pendant'

    def __str__(self) -> str:
        return self.value


class ChainStyle(str, Enum):
    """Chain styles for chain-based jewelry."""

    CUBAN = 'cuban'
    FIGARO = 'figaro'
    ROPE = 'rope'
    CABLE = 'cable'
    SNAKE = 'snake'
    BOX = 'box'
    HERRINGBONE = 'herringbone'
    WHEAT = 'wheat'
    BALL = 'ball'

    def __str__(self) -> str:
        return self.value


@dataclass
class JewelryDesign:
    """
    Represents a jewelry design with all its specifications.

    This class holds all the information needed to generate, display,
    and manufacture a piece of jewelry.
    """

    # Basic information
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ''
    description: str = ''

    # Design parameters
    jewelry_type: JewelryType = JewelryType.CHAIN
    material: Material = Material.GOLD
    chain_style: ChainStyle | None = None
    dimensions: dict[str, float] = field(default_factory=dict)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    batch_id: str | None = None
    tags: list[str] = field(default_factory=list)

    # Generated assets
    model_urls: dict[str, str] = field(default_factory=dict)
    thumbnail_url: str | None = None
    texture_urls: list[dict[str, str]] = field(default_factory=list)

    # Manufacturing info
    weight: float | None = None
    material_cost: float | None = None
    manufacturing_notes: str = ''

    def __post_init__(self):
        """Validate the design data after initialization."""
        if self.jewelry_type == JewelryType.CHAIN and not self.chain_style:
            self.chain_style = ChainStyle.CUBAN

    @property
    def display_name(self) -> str:
        """Get a formatted display name for the design."""
        if self.name:
            return self.name

        style = f'{self.chain_style} ' if self.chain_style else ''
        return f'{style}{self.material} {self.jewelry_type}'.title()

    def to_dict(self) -> dict[str, Any]:
        """Convert the design to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name or self.display_name,
            'description': self.description,
            'jewelry_type': str(self.jewelry_type),
            'material': str(self.material),
            'chain_style': str(self.chain_style) if self.chain_style else None,
            'dimensions': self.dimensions,
            'created_at': self.created_at.isoformat(),
            'batch_id': self.batch_id,
            'tags': self.tags,
            'model_urls': self.model_urls,
            'thumbnail_url': self.thumbnail_url,
            'texture_urls': self.texture_urls,
            'weight': self.weight,
            'material_cost': self.material_cost,
            'manufacturing_notes': self.manufacturing_notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JewelryDesign:
        """Create a design from a dictionary representation."""
        # Convert string enums back to their enum types
        if 'jewelry_type' in data and isinstance(data['jewelry_type'], str):
            data['jewelry_type'] = JewelryType(data['jewelry_type'])

        if 'material' in data and isinstance(data['material'], str):
            data['material'] = Material(data['material'])

        if 'chain_style' in data and isinstance(data['chain_style'], str):
            data['chain_style'] = ChainStyle(data['chain_style'])

        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])

        return cls(**data)

    def get_prompt(self) -> str:
        """
            Generate a detailed, realistic text prompt for AI model generation.
        """
        # Start with professional photography context
        photography_context = (
            'Professional jewelry studio photography of'
        )

        # Base description with material and type
        base_description = (
            f'a high-quality {self.material} {self.jewelry_type}'
        )

        # Add chain style details if applicable
        chain_details = ''
        if self.chain_style and self.jewelry_type in [
            JewelryType.CHAIN,
            JewelryType.NECKLACE,
            JewelryType.BRACELET,
        ]:
            chain_details = (
                f' with properly connected {self.chain_style} style links'
            )

        # Add technical specifications based on jewelry type
        technical_specs = ''
        if self.jewelry_type == JewelryType.RING:
            technical_specs = (
                ', precisely crafted round band with comfortable beveled '
                'inner edges, proper sizing proportions'
            )
        elif self.jewelry_type == JewelryType.PENDANT:
            technical_specs = (
                ', with securely attached bail for chain threading, '
                'balanced weight distribution for proper hanging'
            )
        elif self.jewelry_type == JewelryType.EARRING:
            technical_specs = (
                ', with secure ear wire mechanism, properly balanced '
                'for comfortable wear'
            )
        elif self.jewelry_type == JewelryType.NECKLACE:
            technical_specs = (
                ', featuring secure lobster clasp with jump ring, '
                'properly graduated links for comfortable draping'
            )
        elif self.jewelry_type == JewelryType.BRACELET:
            technical_specs = (
                ', with secure box clasp and safety chain, ergonomically '
                'designed for wrist comfort'
            )
        elif self.jewelry_type == JewelryType.CHAIN:
            technical_specs = (
                ', uniform link pattern throughout, featuring secure '
                'spring ring clasp'
            )

        # Craftsmanship details
        craftsmanship = (
            'professionally hand-polished to a mirror finish, '
            'showcasing refined craftsmanship with attention to detail'
        )

        # Material properties
        material_properties = self._get_material_properties()

        # Photography and presentation details
        presentation = (
            'displayed on neutral background with studio lighting '
            'highlighting fine details, proper depth of field, '
            'realistic reflections'
        )

        # Technical requirements to avoid AI issues
        technical_requirements = (
            'no floating disconnected elements, all components properly '
            'attached, physically accurate for manufacturing'
        )

        # Combine all elements
        prompt = (
            f'{photography_context} {base_description}'
            f'{chain_details}{technical_specs}, '
            f'{craftsmanship}, {material_properties}, '
            f'{presentation}, {technical_requirements}'
        )

        return prompt

    def _get_material_properties(self) -> str:
        """Generate specific material property descriptions."""
        if self.material == Material.GOLD:
            return (
                'warm yellow gold with accurate metallic luster '
                'and reflective properties'
            )
        elif self.material == Material.SILVER:
            return (
                'bright sterling silver with proper white metal sheen '
                'and subtle reflection'
            )
        elif self.material == Material.STAINLESS_STEEL:
            return (
                'durable stainless steel with cool gray tone '
                'and subtle brushed texture'
            )
        elif self.material == Material.GOLD_PLATED:
            return (
                'precision gold-plated surface with consistent coverage '
                'and warm golden hue'
            )
        elif self.material == Material.SILVER_PLATED:
            return (
                'precisely silver-plated with consistent layering '
                'and bright white metal appearance'
            )
        elif self.material == Material.ROSE_GOLD:
            return (
                'warm rose gold with distinctive pinkish hue '
                'and refined metallic shine'
            )
        elif self.material == Material.WHITE_GOLD:
            return (
                'bright white gold with rhodium-plated finish '
                'for brilliant white appearance'
            )
        elif self.material == Material.PLATINUM:
            return (
                'premium platinum with distinctive weight '
                'and cool white-gray metallic appearance'
            )
        elif self.material == Material.BRASS:
            return (
                'polished brass with warm golden-yellow tone '
                'and subtle antiqued detailing'
            )
        else:
            return (
                'with accurate metallic appearance '
                'and proper reflective properties'
            )
