#!/usr/bin/env python3
"""Example: Simple Starter - Minimal Example"""

import sys
sys.path.insert(0, '..')

from axiart import SVGCanvas
from axiart.patterns import SpiralPattern


def main():
    """Simple starter example - just a spiral on a canvas."""

    # Create a canvas
    canvas = SVGCanvas(width=297, height=210, background="white")

    # Create a layer
    canvas.create_layer("main", color="black", stroke_width=0.5)
    canvas.set_layer("main")

    # Generate a simple spiral
    spiral = SpiralPattern(width=297, height=210)
    spiral.generate_fermat_spiral(num_points=800, spacing=3.0)

    # Draw it
    spiral.draw(canvas, "main", as_points=True)

    # Save
    canvas.save("output_simple.svg")
    print("✓ Saved simple spiral to output_simple.svg")


if __name__ == "__main__":
    main()
