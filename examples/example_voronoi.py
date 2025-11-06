#!/usr/bin/env python3
"""Example: Voronoi Diagrams - Cellular Patterns"""

import sys
sys.path.insert(0, '..')

from axiart import SVGCanvas
from axiart.patterns import VoronoiPattern


def main():
    """Demonstrate Voronoi diagram patterns."""

    # Create a canvas
    canvas = SVGCanvas(width=297, height=210, background="white")

    # Create layers
    canvas.create_layer("voronoi", color="black", stroke_width=0.5)
    canvas.create_layer("sites", color="#FF6B6B", stroke_width=2.0)

    # Example 1: Random Voronoi (left side)
    voronoi1 = VoronoiPattern(
        width=140,
        height=210,
        num_sites=50,
        relaxation_iterations=0,  # Pure random
        seed=42
    )
    voronoi1.generate()
    voronoi1.draw(canvas, "voronoi", draw_sites=False)

    # Example 2: Relaxed Voronoi with Lloyd's algorithm (right side)
    voronoi2 = VoronoiPattern(
        width=140,
        height=210,
        num_sites=50,
        relaxation_iterations=3,  # More uniform cells
        seed=42
    )
    voronoi2.generate()

    # Shift to right side
    shifted_edges = []
    for (x1, y1), (x2, y2) in voronoi2.get_edges():
        shifted_edges.append(((x1 + 157, y1), (x2 + 157, y2)))

    for start, end in shifted_edges:
        canvas.add_line(start, end, layer="voronoi")

    # Draw sites for both
    canvas.add_points(voronoi1.get_sites(), layer="sites", radius=1.0)

    shifted_sites = [(x + 157, y) for x, y in voronoi2.get_sites()]
    canvas.add_points(shifted_sites, layer="sites", radius=1.0)

    # Save
    canvas.save("output_voronoi.svg")
    print("Saved Voronoi diagram to output_voronoi.svg")
    print(f"  Left: Random ({len(voronoi1.get_sites())} sites, {len(voronoi1.get_edges())} edges)")
    print(f"  Right: Relaxed ({len(voronoi2.get_sites())} sites, {len(voronoi2.get_edges())} edges)")


if __name__ == "__main__":
    main()
