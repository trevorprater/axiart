#!/usr/bin/env python3
"""Example: Abstract Character - Advanced Artistic Composition

This example demonstrates how to create intentional, artistic compositions
combining multiple pattern types with filled shapes and careful layering.
Inspired by the quality of claude-face.jpeg.
"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import (
    DendritePattern,
    SpiralPattern,
    GridPattern,
    FlowFieldPattern,
    NoisePattern
)
from axiart.composition import Composition
from axiart.shapes import Rectangle, Circle, Polygon, add_filled_shape


def main():
    """Create an abstract character with personality."""

    # Create composition
    comp = Composition(width=297, height=210, background="#FAFAFA")

    # Define layers (order matters for z-index)
    comp.add_layer("fills", color="none", stroke_width=0)  # Filled shapes
    comp.add_layer("grid_bg", color="#CCCCCC", stroke_width=0.3)
    comp.add_layer("dendrites", color="black", stroke_width=0.6)
    comp.add_layer("patterns", color="black", stroke_width=0.4)
    comp.add_layer("accent1", color="#FF6B6B", stroke_width=0.6)  # Red accent
    comp.add_layer("accent2", color="#4ECDC4", stroke_width=0.6)  # Teal accent
    comp.add_layer("details", color="black", stroke_width=0.5)

    canvas = comp.get_canvas()

    print("Creating abstract character composition...")
    print("(This combines filled shapes, patterns, and organic elements)")

    # 1. BACKGROUND GRID with slight distortion
    grid = GridPattern(width=297, height=210)
    grid.generate_square_grid(cell_size=12, jitter=0.3)
    grid.apply_radial_distortion(center=(148, 105), strength=0.05)
    comp.add_pattern(grid, "grid_bg")
    print("✓ Background grid")

    # 2. FILLED SHAPES - Body/head structure
    canvas.set_layer("fills")

    # Head (large circle with color fill)
    head_circle = Circle(center=(148, 100), radius=55)
    add_filled_shape(canvas, head_circle, fill_color="#FFE66D", stroke_color="black", stroke_width=1.0)

    # Body (trapezoid)
    body = Polygon([
        (120, 150),
        (176, 150),
        (190, 210),
        (106, 210),
        (120, 150)
    ])
    add_filled_shape(canvas, body, fill_color="#A8DADC", stroke_color="black", stroke_width=1.0)

    print("✓ Filled shapes (head & body)")

    # 3. EYES - Concentric spirals with teal accent
    # Left eye
    left_eye_bg = Circle(center=(125, 90), radius=18)
    add_filled_shape(canvas, left_eye_bg, fill_color="#E0F7FA", stroke_color="none")

    left_eye = SpiralPattern(width=297, height=210, center=(125, 90), num_revolutions=10)
    left_eye.generate_circular_waves(
        num_circles=12,
        start_radius=2,
        end_radius=16,
        wave_amplitude=0.3,
        wave_frequency=10
    )
    comp.add_pattern(left_eye, "accent2")

    # Right eye
    right_eye_bg = Circle(center=(171, 90), radius=18)
    add_filled_shape(canvas, right_eye_bg, fill_color="#E0F7FA", stroke_color="none")

    right_eye = SpiralPattern(width=297, height=210, center=(171, 90), num_revolutions=10)
    right_eye.generate_circular_waves(
        num_circles=12,
        start_radius=2,
        end_radius=16,
        wave_amplitude=0.3,
        wave_frequency=10
    )
    comp.add_pattern(right_eye, "accent2")

    print("✓ Eyes (spiral patterns)")

    # 4. MOUTH - Flow field creating organic texture
    # Background fill
    mouth_bg = Rectangle(x=110, y=120, width=76, height=25)
    add_filled_shape(canvas, mouth_bg, fill_color="#FFCCCB", stroke_color="none")

    # Flow field texture
    mouth_flow = FlowFieldPattern(width=297, height=210, field_type="waves", scale=15)
    mouth_starts = [(x, y) for x in range(112, 184, 2) for y in range(122, 143, 2)]
    mouth_flow.generate_streamlines(
        num_lines=len(mouth_starts),
        steps=30,
        step_size=0.6,
        start_positions=mouth_starts
    )
    comp.add_pattern(mouth_flow, "patterns")

    # Mouth outline
    canvas.set_layer("details")
    mouth_outline = Rectangle(x=110, y=120, width=76, height=25)
    canvas.add_polyline(mouth_outline.get_points(), "details")

    print("✓ Mouth (flow field texture)")

    # 5. NOSE - Simple geometric
    nose = Polygon([
        (148, 105),
        (143, 118),
        (153, 118),
        (148, 105)
    ], close=True)
    canvas.add_polyline(nose.get_points(), "details")

    # 6. DECORATIVE ELEMENTS - Dendrites growing from corners
    print("Generating organic dendrites...")

    # Top-left
    dendrite_tl = DendritePattern(
        width=297, height=210,
        num_particles=300,
        attraction_distance=3.5,
        branching_style="radial",
        seed_points=[(15, 15)]
    )
    dendrite_tl.generate(max_attempts=400)
    comp.add_pattern(dendrite_tl, "dendrites")

    # Top-right
    dendrite_tr = DendritePattern(
        width=297, height=210,
        num_particles=300,
        attraction_distance=3.5,
        branching_style="radial",
        seed_points=[(282, 15)]
    )
    dendrite_tr.generate(max_attempts=400)
    comp.add_pattern(dendrite_tr, "dendrites")

    # Bottom corners
    dendrite_bl = DendritePattern(
        width=297, height=210,
        num_particles=250,
        attraction_distance=3.5,
        branching_style="radial",
        seed_points=[(15, 195)]
    )
    dendrite_bl.generate(max_attempts=400)
    comp.add_pattern(dendrite_bl, "dendrites")

    dendrite_br = DendritePattern(
        width=297, height=210,
        num_particles=250,
        attraction_distance=3.5,
        branching_style="radial",
        seed_points=[(282, 195)]
    )
    dendrite_br.generate(max_attempts=400)
    comp.add_pattern(dendrite_br, "dendrites")

    print("✓ Corner dendrites")

    # 7. HAIR/ANTENNA - Flowing lines with red accent
    hair_flow = FlowFieldPattern(width=297, height=210, field_type="spiral", scale=40)
    hair_starts = [
        (148, 45), (140, 47), (156, 47),
        (132, 50), (164, 50)
    ]
    hair_flow.generate_streamlines(
        num_lines=len(hair_starts),
        steps=80,
        step_size=1.5,
        start_positions=hair_starts
    )
    comp.add_pattern(hair_flow, "accent1")
    print("✓ Hair/antenna (spiral flow)")

    # 8. TEXTURE DETAILS - Subtle stippling on body
    body_texture = NoisePattern(width=297, height=210, scale=25, seed=42)
    body_texture.generate_stippling(num_points=400, density_map=True, threshold=0.3)
    # Filter points to only show in body area
    filtered_points = [
        (x, y) for x, y in body_texture.get_points()
        if 106 < x < 190 and 150 < y < 210
    ]
    canvas.add_points(filtered_points, "patterns", radius=0.4)
    print("✓ Body texture")

    # Save
    comp.save("output_abstract_character.svg")
    print("\n✓ Saved abstract character to output_abstract_character.svg")
    print("  This demonstrates artistic composition combining:")
    print("  • Filled color shapes (head, body)")
    print("  • Pattern generators (spirals, flow fields)")
    print("  • Organic elements (dendrites)")
    print("  • Multiple color accents")


if __name__ == "__main__":
    main()
