#!/usr/bin/env python3
"""Example: Truchet Tiles - Geometric Patterns"""

import sys
sys.path.insert(0, '..')

from axiart import SVGCanvas
from axiart.patterns import TruchetPattern


def main():
    """Demonstrate Truchet tile patterns."""

    # Create a canvas
    canvas = SVGCanvas(width=297, height=210, background="white")

    # Create layers
    canvas.create_layer("tiles", color="black", stroke_width=0.7)
    canvas.create_layer("accents", color="#FF6B6B", stroke_width=0.5)

    # Example 1: Diagonal tiles (top left, structured)
    diagonal = TruchetPattern(
        width=70,
        height=70,
        tile_type="diagonal",
        grid_size=15,
        randomness=0.0,  # Structured pattern
        seed=42
    )
    diagonal.generate()

    # Shift diagonals
    for (x1, y1), (x2, y2) in diagonal.get_lines():
        canvas.add_line((x1 + 10, y1 + 10), (x2 + 10, y2 + 10), layer="tiles")

    # Example 2: Arc tiles (top center, semi-random)
    arcs = TruchetPattern(
        width=70,
        height=70,
        tile_type="arc",
        grid_size=12,
        randomness=0.3,
        arc_segments=12,
        seed=42
    )
    arcs.generate()

    for curve in arcs.get_curves():
        shifted = [(x + 90, y + 10) for x, y in curve]
        canvas.add_polyline(shifted, layer="tiles")

    # Example 3: Double arc tiles (top right, random)
    double_arcs = TruchetPattern(
        width=70,
        height=70,
        tile_type="double_arc",
        grid_size=10,
        randomness=1.0,  # Fully random
        arc_segments=12,
        seed=123
    )
    double_arcs.generate()

    for curve in double_arcs.get_curves():
        shifted = [(x + 170, y + 10) for x, y in curve]
        canvas.add_polyline(shifted, layer="tiles")

    # Example 4: Triangle tiles (bottom left)
    triangles = TruchetPattern(
        width=70,
        height=70,
        tile_type="triangle",
        grid_size=12,
        randomness=0.5,
        seed=42
    )
    triangles.generate()

    for (x1, y1), (x2, y2) in triangles.get_lines():
        canvas.add_line((x1 + 10, y1 + 100), (x2 + 10, y2 + 100), layer="accents")

    # Example 5: Maze tiles (bottom center)
    maze = TruchetPattern(
        width=70,
        height=70,
        tile_type="maze",
        grid_size=15,
        randomness=1.0,
        seed=789
    )
    maze.generate()

    for (x1, y1), (x2, y2) in maze.get_lines():
        canvas.add_line((x1 + 90, y1 + 100), (x2 + 90, y2 + 100), layer="tiles")

    # Example 6: Large arc pattern (bottom right)
    large = TruchetPattern(
        width=70,
        height=70,
        tile_type="arc",
        grid_size=8,
        randomness=0.5,
        arc_segments=16,
        seed=456
    )
    large.generate()

    for curve in large.get_curves():
        shifted = [(x + 170, y + 100) for x, y in curve]
        canvas.add_polyline(shifted, layer="tiles")

    # Save
    canvas.save("output_truchet.svg")
    print("Saved Truchet tile patterns to output_truchet.svg")
    print(f"  Diagonal: {len(diagonal.get_lines())} lines")
    print(f"  Arcs: {len(arcs.get_curves())} curves")
    print(f"  Double Arcs: {len(double_arcs.get_curves())} curves")
    print(f"  Triangles: {len(triangles.get_lines())} lines")
    print(f"  Maze: {len(maze.get_lines())} lines")
    print(f"  Large: {len(large.get_curves())} curves")


if __name__ == "__main__":
    main()
