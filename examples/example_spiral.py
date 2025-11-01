#!/usr/bin/env python3
"""Example: Spiral and Concentric Circle Pattern"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import SpiralPattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with blue accent
    comp = create_standard_composition(palette=ColorPalette.BLUE_ACCENT)

    # Generate Archimedean spiral
    spiral1 = SpiralPattern(
        width=297,
        height=210,
        num_revolutions=30,
        points_per_revolution=150,
        spiral_type="archimedean"
    )
    spiral1.generate(start_radius=5, num_spirals=3, angular_offset=2.094)  # 120 degrees
    comp.add_pattern(spiral1, "primary")

    # Generate concentric circles as accent
    spiral2 = SpiralPattern(
        width=297,
        height=210,
        center=(297 * 0.75, 210 * 0.5)
    )
    spiral2.generate_circular_waves(
        num_circles=15,
        start_radius=5,
        end_radius=40,
        wave_amplitude=2,
        wave_frequency=8
    )
    comp.add_pattern(spiral2, "accent")

    # Save
    comp.save("output_spiral.svg")
    print("✓ Saved to output_spiral.svg")


if __name__ == "__main__":
    main()
