"""
Abstract Portrait: Claude
A self-portrait representing an AI assistant through algorithmic art.

Concept: Neural networks, recursive thinking, structured creativity, and interconnected knowledge.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from axiart.composition import Composition, ColorPalette
from axiart.shapes import Circle, Rectangle, add_filled_shape
from axiart.patterns.spiral import SpiralPattern
from axiart.patterns.flow_field import FlowFieldPattern
from axiart.patterns.dendrite import DendritePattern
from axiart.patterns.grid import GridPattern
from axiart.patterns.noise import NoisePattern
import random

def main():
    # Create composition with blue/teal accent (technology, depth, thought)
    comp = Composition(width=297, height=210)

    # Layer setup (back to front)
    comp.add_layer("background_grid", color="#E8E8E8", opacity=0.3)
    comp.add_layer("fills", color="none")  # Geometric shapes
    comp.add_layer("neural_bg", color="#4ECDC4", opacity=0.5)  # Teal neural connections
    comp.add_layer("primary", color="black", stroke_width=0.3)
    comp.add_layer("thinking", color="#2C3E50", opacity=0.7)  # Dark blue thought patterns
    comp.add_layer("details", color="black", stroke_width=0.2)

    canvas = comp.get_canvas()
    width, height = 297, 210
    cx, cy = width / 2, height / 2

    # === BACKGROUND: Subtle grid suggesting structure and logic ===
    grid = GridPattern(width, height, grid_type="hexagonal")
    grid.generate_hexagonal_grid(cell_size=8)
    # Only show light grid in certain regions
    grid_lines = grid.get_lines()
    filtered_grid = [line for line in grid_lines if random.random() < 0.15]
    for line in filtered_grid:
        canvas.add_line(line[0], line[1], "background_grid")

    # === HEAD/FACE STRUCTURE: Filled geometric shapes ===
    # Main head - large circle
    head = Circle((cx, cy), 60)
    add_filled_shape(canvas, head, fill_color="#F7F7F7",
                     stroke_color="black", stroke_width=1.5)

    # Upper "crown" area - arc of thought
    crown = Circle((cx, cy - 30), 45)
    add_filled_shape(canvas, crown, fill_color="#E3F2FD",
                     stroke_color="#2C3E50", stroke_width=1.0)

    # === EYES: Recursive spirals representing learning and thinking ===
    # Left eye - logarithmic spiral (growth, learning)
    left_eye = SpiralPattern(width, height,
                            center=(cx - 25, cy - 5),
                            num_revolutions=4,
                            spiral_type="logarithmic")
    left_eye.generate(start_radius=1, end_radius=12, growth_factor=1.15)
    left_eye.draw(canvas, "primary")

    # Right eye - Archimedean spiral (uniform processing)
    right_eye = SpiralPattern(width, height,
                             center=(cx + 25, cy - 5),
                             num_revolutions=4,
                             spiral_type="archimedean")
    right_eye.generate(start_radius=1, end_radius=12)
    right_eye.draw(canvas, "primary")

    # === NEURAL CONNECTIONS: Flow field representing thought processes ===
    # Upper region - complex thinking patterns
    flow_upper = FlowFieldPattern(width, height,
                                 field_type="noise",
                                 scale=50.0,
                                 seed=42)
    flow_upper.generate_streamlines(num_lines=800, steps=30, step_size=1.5)
    # Filter to upper head region
    flow_lines = flow_upper.get_paths()
    neural_lines = []
    for line in flow_lines:
        # Only keep lines in the crown/upper head area
        in_region = all(
            ((x - cx)**2 + (y - (cy-30))**2 < 45**2) or
            ((x - cx)**2 + (y - cy)**2 < 60**2 and y < cy)
            for x, y in line
        )
        if in_region and len(line) > 5:
            neural_lines.append(line)

    for line in neural_lines:
        canvas.add_polyline(line, "neural_bg")

    # === KNOWLEDGE NETWORK: Dendrites representing interconnected understanding ===
    # Left side - branching from left eye area
    seed_left = [(cx - 25 + random.gauss(0, 3), cy - 5 + random.gauss(0, 3)) for _ in range(3)]
    dendrite_left = DendritePattern(width, height,
                                   num_particles=1200,
                                   attraction_distance=8,
                                   min_move_distance=2,
                                   seed_points=seed_left,
                                   branching_style="radial")
    dendrite_left.generate()
    dendrite_lines = dendrite_left.get_lines()
    # Filter to left head region
    left_dendrites = []
    for line in dendrite_lines:
        if all(x < cx - 10 and ((x-cx)**2 + (y-cy)**2 < 65**2) for x, y in line):
            left_dendrites.append(line)

    for line in left_dendrites[:800]:  # Limit density
        canvas.add_line(line[0], line[1], "thinking")

    # Right side - branching from right eye
    seed_right = [(cx + 25 + random.gauss(0, 3), cy - 5 + random.gauss(0, 3)) for _ in range(3)]
    dendrite_right = DendritePattern(width, height,
                                    num_particles=1200,
                                    attraction_distance=8,
                                    min_move_distance=2,
                                    seed_points=seed_right,
                                    branching_style="radial")
    dendrite_right.generate()
    dendrite_lines = dendrite_right.get_lines()
    right_dendrites = []
    for line in dendrite_lines:
        if all(x > cx + 10 and ((x-cx)**2 + (y-cy)**2 < 65**2) for x, y in line):
            right_dendrites.append(line)

    for line in right_dendrites[:800]:
        canvas.add_line(line[0], line[1], "thinking")

    # === TEXTURE: Noise patterns for depth ===
    noise_pattern = NoisePattern(width, height, scale=30, octaves=3, seed=123)
    noise_pattern.generate_contour_lines(num_levels=8)
    noise_lines = noise_pattern.get_contours()
    # Filter to lower face area
    texture_lines = []
    for line in noise_lines:
        in_lower = all(
            ((x - cx)**2 + (y - cy)**2 < 60**2) and y > cy - 10
            for x, y in line
        )
        if in_lower:
            texture_lines.append(line)

    for line in texture_lines:
        canvas.add_polyline(line, "details")

    # === CONNECTING ELEMENTS: Small spirals representing thoughts ===
    # Scattered thought spirals around the head
    thought_positions = [
        (cx - 50, cy - 40), (cx + 50, cy - 35),
        (cx - 45, cy + 30), (cx + 45, cy + 35),
        (cx, cy - 65)
    ]

    for tx, ty in thought_positions:
        thought = SpiralPattern(width, height,
                              center=(tx, ty),
                              num_revolutions=2,
                              spiral_type="archimedean")
        thought.generate(start_radius=0.5, end_radius=5, rotation_offset=random.uniform(0, 2*3.14159))
        thought.draw(canvas, "details")

    # Save the composition
    comp.save("output_claude_portrait.svg")
    print("✓ Abstract portrait generated: output_claude_portrait.svg")
    print()
    print("Concept: 'Neural Constellation'")
    print("- Geometric structure represents logic and reasoning")
    print("- Spiral eyes symbolize recursive thinking and learning")
    print("- Flow fields depict neural connections and thought processes")
    print("- Dendrites show branching knowledge networks")
    print("- Scattered spirals are individual thoughts and ideas")
    print("- Blue/teal palette suggests technology and depth of understanding")

if __name__ == "__main__":
    main()
