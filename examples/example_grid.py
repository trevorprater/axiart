#!/usr/bin/env python3
"""Example: Grid Overlay Pattern"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import GridPattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with gold accent
    comp = create_standard_composition(palette=ColorPalette.GOLD_ACCENT)

    # Generate hexagonal grid
    grid1 = GridPattern(width=297, height=210, grid_type="hexagonal")
    grid1.generate_hexagonal_grid(cell_size=10, fill_cells=True)
    comp.add_pattern(grid1, "primary")

    # Generate distorted square grid as accent
    grid2 = GridPattern(width=297, height=210, grid_type="square")
    grid2.generate_square_grid(cell_size=15, jitter=1.5)
    grid2.apply_radial_distortion(strength=0.15)
    comp.add_pattern(grid2, "accent")

    # Save
    comp.save("output_grid.svg")
    print("✓ Saved to output_grid.svg")


if __name__ == "__main__":
    main()
