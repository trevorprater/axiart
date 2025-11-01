#!/usr/bin/env python3
"""Example: Mixed Composition - Landscape Theme"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import NoisePattern, DendritePattern, SpiralPattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with dual gold/teal palette
    comp = create_standard_composition(palette=ColorPalette.DUAL_GOLD_TEAL)

    # Background: topographic contours (mountains)
    topo = NoisePattern(width=297, height=210, scale=100, octaves=8, seed=500)
    print("Generating topographic landscape...")
    topo.generate_contour_lines(num_levels=40, resolution=2.0, min_value=-0.5, max_value=1.0)
    comp.add_pattern(topo, "background")

    # Primary: hatching for shading
    hatching = NoisePattern(width=297, height=210, scale=60, seed=600)
    hatching.generate_hatching(line_spacing=3.0, angle=45, density_modulation=True)
    comp.add_pattern(hatching, "primary")

    # Accent 1: tree-like dendrites
    trees = DendritePattern(
        width=297,
        height=210,
        num_particles=800,
        attraction_distance=4.0,
        branching_style="vertical"
    )
    print("Generating trees...")
    trees.generate()
    comp.add_pattern(trees, "accent1")

    # Accent 2: sun/moon with concentric circles
    sun = SpiralPattern(width=297, height=210, center=(250, 40))
    sun.generate_circular_waves(num_circles=8, start_radius=5, end_radius=25)
    comp.add_pattern(sun, "accent2")

    # Save
    comp.save("output_mixed_landscape.svg")
    print("✓ Saved to output_mixed_landscape.svg")


if __name__ == "__main__":
    main()
