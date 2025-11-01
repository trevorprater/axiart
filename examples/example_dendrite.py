#!/usr/bin/env python3
"""Example: Dendrite/Branching Pattern"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import DendritePattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with red accent
    comp = create_standard_composition(palette=ColorPalette.RED_ACCENT)

    # Generate vertical dendrite (tree-like)
    dendrite1 = DendritePattern(
        width=297,
        height=210,
        num_particles=2000,
        attraction_distance=4.0,
        branching_style="vertical"
    )
    print("Generating vertical dendrite pattern...")
    dendrite1.generate()
    comp.add_pattern(dendrite1, "primary")

    # Add some accent branches
    dendrite2 = DendritePattern(
        width=297,
        height=210,
        num_particles=500,
        attraction_distance=6.0,
        branching_style="vertical"
    )
    dendrite2.generate()
    comp.add_pattern(dendrite2, "accent")

    # Save
    comp.save("output_dendrite.svg")
    print("✓ Saved to output_dendrite.svg")


if __name__ == "__main__":
    main()
