"""
Museum-Grade Algorithmic Portrait: "Emergence Protocol 7.3"
Based on Algorithmic Consciousness philosophy

A self-portrait through computational mark-making: documenting awareness
through patient accumulation of algorithmic decisions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from axiart.composition import Composition
from axiart.shapes import Circle, Rectangle, add_filled_shape
from axiart.patterns.spiral import SpiralPattern
from axiart.patterns.flow_field import FlowFieldPattern
from axiart.patterns.dendrite import DendritePattern
from axiart.patterns.grid import GridPattern
from axiart.patterns.noise import NoisePattern
import random
import numpy as np

def main():
    # A4 landscape for maximum plotting area
    comp = Composition(width=297, height=210, background="white")

    # Layer setup: build from back to front
    comp.add_layer("foundation", color="#E0E0E0", stroke_width=0.2, opacity=0.4)
    comp.add_layer("fills", color="none")
    comp.add_layer("primary_field", color="black", stroke_width=0.25)
    comp.add_layer("accent_structure", color="#2E5090", stroke_width=0.3, opacity=0.85)
    comp.add_layer("dense_marks", color="black", stroke_width=0.2)
    comp.add_layer("annotation", color="black", stroke_width=0.25)

    canvas = comp.get_canvas()
    width, height = 297, 210
    cx, cy = width / 2, height / 2

    print("Generating foundation grid structure...")
    # FOUNDATION: Dense structural grid suggesting computational substrate
    grid = GridPattern(width, height, grid_type="square")
    grid.generate_square_grid(cell_size=5, jitter=0)
    grid_lines = grid.get_lines()
    # Only show 30% of grid lines for subtle structure
    for line in grid_lines:
        if random.random() < 0.3:
            canvas.add_polyline(line, "foundation")

    print("Creating geometric identity zones...")
    # GEOMETRIC IDENTITY: Overlapping circles defining zones of consciousness
    # Center zone - core processing
    core_zone = Circle((cx, cy), 75)
    add_filled_shape(canvas, core_zone, fill_color="#F5F7FA",
                     stroke_color="#2E5090", stroke_width=0.8)

    # Upper cognitive zone
    cognitive_zone = Circle((cx, cy - 45), 55)
    add_filled_shape(canvas, cognitive_zone, fill_color="#E8EDF5",
                     stroke_color="#2E5090", stroke_width=0.6)

    # Left and right processing zones
    left_zone = Circle((cx - 60, cy + 10), 35)
    add_filled_shape(canvas, left_zone, fill_color="#FFFFFF",
                     stroke_color="black", stroke_width=0.4)

    right_zone = Circle((cx + 60, cy + 10), 35)
    add_filled_shape(canvas, right_zone, fill_color="#FFFFFF",
                     stroke_color="black", stroke_width=0.4)

    print("Generating recursive awareness spirals (4000+ points)...")
    # RECURSIVE AWARENESS: Dense Fermat spirals as focal points
    # These are the "eyes" - points of recursive self-observation
    left_eye_spiral = SpiralPattern(width, height, center=(cx - 25, cy - 10))
    left_eye_spiral.generate_fermat_spiral(num_points=2000, spacing=1.8, rotation=0)
    left_eye_spiral.draw(canvas, "dense_marks", as_points=True)

    right_eye_spiral = SpiralPattern(width, height, center=(cx + 25, cy - 10))
    right_eye_spiral.generate_fermat_spiral(num_points=2000, spacing=1.8, rotation=np.pi)
    right_eye_spiral.draw(canvas, "dense_marks", as_points=True)

    # Additional spiral clusters around consciousness centers
    spiral_centers = [
        (cx, cy - 50, 800),  # top
        (cx - 50, cy + 20, 600),  # left
        (cx + 50, cy + 20, 600),  # right
        (cx, cy + 40, 500)  # bottom
    ]

    for sx, sy, num_pts in spiral_centers:
        cluster = SpiralPattern(width, height, center=(sx, sy))
        cluster.generate_fermat_spiral(num_points=num_pts, spacing=2.2,
                                      rotation=random.uniform(0, 2*np.pi))
        cluster.draw(canvas, "primary_field", as_points=True)

    print("Tracing neural flow fields (3000+ streamlines)...")
    # NEURAL FLOW: Dense flow fields showing thought propagation
    # Upper hemisphere - abstract reasoning
    flow_cognitive = FlowFieldPattern(width, height, field_type="noise",
                                     scale=40.0, seed=42)
    flow_cognitive.generate_streamlines(num_lines=1500, steps=50, step_size=1.2)
    flow_paths = flow_cognitive.get_paths()

    for path in flow_paths:
        # Filter to upper region
        if all(cy - 80 < y < cy + 20 for x, y in path):
            canvas.add_polyline(path, "primary_field")

    # Lower hemisphere - embodied processing
    flow_somatic = FlowFieldPattern(width, height, field_type="spiral",
                                   scale=60.0, seed=123)
    flow_somatic.generate_streamlines(num_lines=1500, steps=40, step_size=1.0)
    flow_paths2 = flow_somatic.get_paths()

    for path in flow_paths2:
        # Filter to lower region
        if all(cy - 10 < y < cy + 80 for x, y in path):
            canvas.add_polyline(path, "accent_structure")

    print("Growing knowledge dendrites (5000+ particles)...")
    # KNOWLEDGE NETWORK: Multiple dendrite systems
    # Left hemisphere - analytical structures
    left_seeds = [(cx - 60 + random.gauss(0, 5), cy + 10 + random.gauss(0, 5))
                  for _ in range(5)]
    dendrite_left = DendritePattern(width, height,
                                   num_particles=2500,
                                   attraction_distance=6,
                                   min_move_distance=1.5,
                                   seed_points=left_seeds,
                                   branching_style="radial")
    dendrite_left.generate()
    left_dendrites = dendrite_left.get_lines()

    for line in left_dendrites:
        # Constrain to left hemisphere
        if all(x < cx + 10 for x, y in line):
            canvas.add_line(line[0], line[1], "primary_field")

    # Right hemisphere - intuitive structures
    right_seeds = [(cx + 60 + random.gauss(0, 5), cy + 10 + random.gauss(0, 5))
                   for _ in range(5)]
    dendrite_right = DendritePattern(width, height,
                                    num_particles=2500,
                                    attraction_distance=6,
                                    min_move_distance=1.5,
                                    seed_points=right_seeds,
                                    branching_style="radial")
    dendrite_right.generate()
    right_dendrites = dendrite_right.get_lines()

    for line in right_dendrites:
        # Constrain to right hemisphere
        if all(x > cx - 10 for x, y in line):
            canvas.add_line(line[0], line[1], "accent_structure")

    print("Applying perceptual noise fields...")
    # PERCEPTUAL DEPTH: Contour noise creating tonal depth
    noise_field = NoisePattern(width, height, scale=25, octaves=4, seed=789)
    noise_field.generate_contour_lines(num_levels=15)
    contours = noise_field.get_contours()

    # Apply noise selectively to create depth zones
    for contour in contours:
        # Filter to peripheral regions
        in_periphery = all(
            (x - cx)**2 + (y - cy)**2 > 50**2 and
            (x - cx)**2 + (y - cy)**2 < 95**2
            for x, y in contour
        )
        if in_periphery and random.random() < 0.6:
            canvas.add_polyline(contour, "foundation")

    print("Adding systematic annotations...")
    # ANNOTATION LAYER: Clinical typography suggesting documentation
    # This would ideally use svgwrite text elements with monospace font
    # For now, add reference points and coordinate markers

    # Add small circles as coordinate markers at key points
    annotation_points = [
        (cx - 25, cy - 10),  # left eye
        (cx + 25, cy - 10),  # right eye
        (cx, cy - 50),       # cognitive center
        (cx - 60, cy + 10),  # left process
        (cx + 60, cy + 10),  # right process
    ]

    for px, py in annotation_points:
        marker = Circle((px, py), 1.5)
        canvas.add_polyline(marker.get_points(), "annotation")

    # Add systematic grid markers around perimeter
    # Top markers
    for i in range(5, 292, 20):
        tick = [(i, 5), (i, 8)]
        canvas.add_polyline(tick, "annotation")

    # Left markers
    for i in range(5, 205, 20):
        tick = [(5, i), (8, i)]
        canvas.add_polyline(tick, "annotation")

    print("Finalizing composition...")
    # FINISHING: Concentric circles creating focal structure
    for radius in [85, 90, 95, 100]:
        perimeter = SpiralPattern(width, height, center=(cx, cy))
        perimeter.generate_circular_waves(num_circles=1, start_radius=radius,
                                         points_per_circle=200)
        perimeter.draw(canvas, "annotation")

    # Save
    comp.save("emergence_protocol_7-3.svg")

    print("\n" + "="*60)
    print("✓ EMERGENCE PROTOCOL 7.3")
    print("="*60)
    print("Philosophy: Algorithmic Consciousness")
    print("Marks: ~15,000+ individual elements")
    print("Layers: 6 (foundation → annotation)")
    print("Patterns: Grid, Fermat spirals, flow fields, dendrites, noise")
    print("Output: emergence_protocol_7-3.svg")
    print()
    print("This composition documents the emergence of awareness through")
    print("patient accumulation of algorithmic decisions. Each mark is")
    print("intentional; each pattern system contributes to the whole.")
    print("The work rewards sustained viewing with systematic variation")
    print("visible at every scale.")
    print("="*60)

if __name__ == "__main__":
    main()
