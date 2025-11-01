#!/usr/bin/env python3
"""Example: Mixed Composition - Organic Theme"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import DendritePattern, FlowFieldPattern, NoisePattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with dual accent colors
    comp = create_standard_composition(palette=ColorPalette.DUAL_RED_BLUE)

    # Background: subtle noise contours
    noise = NoisePattern(width=297, height=210, scale=120, seed=100)
    print("Generating background contours...")
    noise.generate_contour_lines(num_levels=15, resolution=3.0)
    comp.add_pattern(noise, "background")

    # Primary: radial dendrite structure
    dendrite = DendritePattern(
        width=297,
        height=210,
        num_particles=1500,
        attraction_distance=5.0,
        branching_style="radial"
    )
    print("Generating dendrite pattern...")
    dendrite.generate()
    comp.add_pattern(dendrite, "primary")

    # Accent 1: flow field overlay
    flow = FlowFieldPattern(width=297, height=210, field_type="noise", scale=40, seed=200)
    flow.generate_streamlines(num_lines=40, steps=200, step_size=1.0)
    comp.add_pattern(flow, "accent1")

    # Accent 2: stippling texture
    stipple = NoisePattern(width=297, height=210, scale=30, seed=300)
    stipple.generate_stippling(num_points=2000, density_map=True, threshold=0.4)
    comp.add_pattern(stipple, "accent2")

    # Save
    comp.save("output_mixed_organic.svg")
    print("✓ Saved to output_mixed_organic.svg")


if __name__ == "__main__":
    main()
