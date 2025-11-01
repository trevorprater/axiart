#!/usr/bin/env python3
"""Example: Noise and Texture Field Pattern"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import NoisePattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with green accent
    comp = create_standard_composition(palette=ColorPalette.GREEN_ACCENT)

    # Generate topographic contour lines
    noise1 = NoisePattern(
        width=297,
        height=210,
        scale=80,
        octaves=6,
        seed=42
    )
    print("Generating contour lines...")
    noise1.generate_contour_lines(num_levels=30, resolution=2.0)
    comp.add_pattern(noise1, "primary")

    # Add stippling texture as accent
    noise2 = NoisePattern(
        width=297,
        height=210,
        scale=50,
        seed=123
    )
    noise2.generate_stippling(num_points=3000, density_map=True, threshold=0.2)
    comp.add_pattern(noise2, "accent")

    # Save
    comp.save("output_noise.svg")
    print("✓ Saved to output_noise.svg")


if __name__ == "__main__":
    main()
