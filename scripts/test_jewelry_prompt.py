#!/usr/bin/env python
"""
Demonstrates jewelry design prompts across materials and types.
"""
from __future__ import annotations

from python_jewelry_design_gen.models.jewelry_design import ChainStyle
from python_jewelry_design_gen.models.jewelry_design import JewelryDesign
from python_jewelry_design_gen.models.jewelry_design import JewelryType
from python_jewelry_design_gen.models.jewelry_design import Material


def main():
    jewelry_types = [
        JewelryType.CHAIN,
        JewelryType.RING,
        JewelryType.BRACELET,
        JewelryType.NECKLACE,
        JewelryType.EARRING,
        JewelryType.PENDANT,
    ]

    materials = [
        Material.GOLD,
        Material.SILVER,
        Material.PLATINUM,
        Material.ROSE_GOLD,
    ]

    for jewelry_type in jewelry_types:
        for material in materials:
            chain_style = None
            chain_types = [
                JewelryType.CHAIN,
                JewelryType.BRACELET,
                JewelryType.NECKLACE,
            ]

            if jewelry_type in chain_types:
                is_chain = jewelry_type == JewelryType.CHAIN
                chain_style = ChainStyle.CUBAN if is_chain else ChainStyle.ROPE

            design = JewelryDesign(
                jewelry_type=jewelry_type,
                material=material,
                chain_style=chain_style,
            )

            print(f"\n{'='*80}\n")
            print(f'DESIGN: {design.display_name}')
            print(f'\nPROMPT:\n{design.get_prompt()}')
            print(f"\n{'='*80}\n")

    print('\nPrompt testing complete!')


if __name__ == '__main__':
    main()
