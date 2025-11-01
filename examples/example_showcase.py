#!/usr/bin/env python3
"""Example: Comprehensive Showcase - All Patterns Combined"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import (
    DendritePattern,
    SpiralPattern,
    GridPattern,
    NoisePattern,
    FlowFieldPattern
)
from axiart.composition import Composition, ColorPalette


def main():
    # Create a large composition showcasing all patterns
    comp = Composition(width=297, height=210, background="white")

    # Create layers with custom colors
    comp.add_layer("grid", color="#CCCCCC", stroke_width=0.3)
    comp.add_layer("noise", color="black", stroke_width=0.4)
    comp.add_layer("flow", color="#1976D2", stroke_width=0.5)
    comp.add_layer("dendrite", color="#D32F2F", stroke_width=0.6)
    comp.add_layer("spiral", color="#F9A825", stroke_width=0.5)

    print("Generating showcase composition with all pattern types...")

    # Layer 1: Hexagonal grid background
    grid = GridPattern(width=297, height=210)
    grid.generate_hexagonal_grid(cell_size=15, fill_cells=True)
    comp.add_pattern(grid, "grid")
    print("✓ Grid layer")

    # Layer 2: Noise contours (left half)
    noise = NoisePattern(width=150, height=210, scale=60, seed=42)
    noise.generate_contour_lines(num_levels=20, resolution=2.0)
    comp.add_pattern(noise, "noise")
    print("✓ Noise layer")

    # Layer 3: Flow field (right half)
    flow = FlowFieldPattern(width=297, height=210, field_type="noise", scale=50, seed=100)
    # Start positions on right side
    start_positions = [(297 * 0.7, y) for y in range(0, 210, 15)]
    flow.generate_streamlines(
        num_lines=len(start_positions),
        steps=200,
        step_size=1.0,
        start_positions=start_positions
    )
    comp.add_pattern(flow, "flow")
    print("✓ Flow field layer")

    # Layer 4: Dendrite (center)
    dendrite = DendritePattern(
        width=297,
        height=210,
        num_particles=1000,
        attraction_distance=5.0,
        branching_style="radial",
        seed_points=[(148.5, 105)]
    )
    dendrite.generate(max_attempts=500)
    comp.add_pattern(dendrite, "dendrite")
    print("✓ Dendrite layer")

    # Layer 5: Spirals (corners)
    spiral_tl = SpiralPattern(width=297, height=210, center=(40, 40), num_revolutions=10)
    spiral_tl.generate(start_radius=2, end_radius=30)
    comp.add_pattern(spiral_tl, "spiral")

    spiral_br = SpiralPattern(width=297, height=210, center=(257, 170), num_revolutions=10)
    spiral_br.generate(start_radius=2, end_radius=30)
    comp.add_pattern(spiral_br, "spiral")
    print("✓ Spiral layers")

    # Save
    comp.save("output_showcase.svg")
    print("\n✓ Saved comprehensive showcase to output_showcase.svg")


if __name__ == "__main__":
    main()
