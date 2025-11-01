#!/usr/bin/env python3
"""Example: Mixed Composition - Geometric Theme"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import GridPattern, SpiralPattern, FlowFieldPattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with orange accent
    comp = create_standard_composition(palette=ColorPalette.ORANGE_ACCENT)

    # Background: distorted grid
    grid = GridPattern(width=297, height=210)
    grid.generate_square_grid(cell_size=20, draw_horizontal=True, draw_vertical=True)
    grid.apply_radial_distortion(strength=0.2)
    comp.add_pattern(grid, "background")

    # Primary: multiple spirals
    spiral = SpiralPattern(width=297, height=210, num_revolutions=25, spiral_type="logarithmic")
    spiral.generate(start_radius=3, num_spirals=5, angular_offset=1.256)  # 72 degrees
    comp.add_pattern(spiral, "primary")

    # Accent: flow field with radial pattern
    flow = FlowFieldPattern(width=297, height=210, field_type="radial")
    flow.generate_streamlines(num_lines=30, steps=100, step_size=1.5)
    comp.add_pattern(flow, "accent")

    # Save
    comp.save("output_mixed_geometric.svg")
    print("✓ Saved to output_mixed_geometric.svg")


if __name__ == "__main__":
    main()
