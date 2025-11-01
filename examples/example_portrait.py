#!/usr/bin/env python3
"""Example: Abstract Portrait - Artistic Composition"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import (
    DendritePattern,
    SpiralPattern,
    GridPattern,
    FlowFieldPattern
)
from axiart.composition import Composition
from axiart import SVGCanvas


def main():
    """Create an artistic abstract portrait similar to claude-face.jpeg"""

    # Create composition with custom color scheme
    comp = Composition(width=297, height=210, background="white")

    # Define layers with specific colors
    comp.add_layer("grid", color="#333333", stroke_width=0.4)
    comp.add_layer("hair_fill", color="#F9A825", stroke_width=0)  # Gold fill
    comp.add_layer("dendrites", color="black", stroke_width=0.5)
    comp.add_layer("eyes", color="#9C27B0", stroke_width=0.6)  # Purple
    comp.add_layer("mouth", color="black", stroke_width=0.4)
    comp.add_layer("nose", color="black", stroke_width=0.5)
    comp.add_layer("details", color="#7B1FA2", stroke_width=0.3)

    print("Creating artistic portrait composition...")

    # 1. Background grid
    grid = GridPattern(width=297, height=210)
    grid.generate_square_grid(cell_size=15, jitter=0.5)
    comp.add_pattern(grid, "grid")
    print("✓ Grid structure")

    # 2. Hair (filled geometric shape - using canvas directly for fills)
    canvas = comp.get_canvas()
    canvas.set_layer("hair_fill")

    # Create hair shape (trapezoid at top)
    hair_points = [
        (80, 30),
        (217, 30),
        (240, 100),
        (57, 100),
        (80, 30)
    ]
    canvas.dwg.add(canvas.dwg.polygon(
        points=hair_points,
        fill="#F9A825",
        stroke="black",
        stroke_width=0.5
    ))
    print("✓ Hair shape")

    # 3. Eyes - concentric spirals
    # Left eye
    left_eye = SpiralPattern(
        width=297,
        height=210,
        center=(110, 100),
        num_revolutions=12
    )
    left_eye.generate_circular_waves(
        num_circles=15,
        start_radius=3,
        end_radius=22,
        points_per_circle=120,
        wave_amplitude=0.5,
        wave_frequency=8
    )
    comp.add_pattern(left_eye, "eyes")

    # Add purple fill circle behind left eye
    canvas.dwg.add(canvas.dwg.circle(
        center=(110, 100),
        r=25,
        fill="#E1BEE7",
        stroke="none",
        opacity=0.6
    ))

    # Right eye
    right_eye = SpiralPattern(
        width=297,
        height=210,
        center=(187, 100),
        num_revolutions=12
    )
    right_eye.generate_circular_waves(
        num_circles=15,
        start_radius=3,
        end_radius=22,
        points_per_circle=120,
        wave_amplitude=0.5,
        wave_frequency=8
    )
    comp.add_pattern(right_eye, "eyes")

    # Add purple fill circle behind right eye
    canvas.dwg.add(canvas.dwg.circle(
        center=(187, 100),
        r=25,
        fill="#E1BEE7",
        stroke="none",
        opacity=0.6
    ))
    print("✓ Eyes (concentric spirals)")

    # 4. Nose - simple geometric structure
    canvas.set_layer("nose")
    nose_lines = [
        [(148.5, 110), (148.5, 140)],
        [(143, 135), (154, 135)],
        [(143, 140), (154, 140)]
    ]
    for line in nose_lines:
        canvas.add_polyline(line, "nose")
    print("✓ Nose structure")

    # 5. Mouth - wavy flow field
    mouth_flow = FlowFieldPattern(
        width=297,
        height=210,
        field_type="waves",
        scale=20
    )
    # Generate horizontal streamlines in mouth area
    mouth_starts = [(x, 160 + y*3) for x in range(90, 207, 3) for y in range(8)]
    mouth_flow.generate_streamlines(
        num_lines=len(mouth_starts),
        steps=50,
        step_size=0.8,
        start_positions=mouth_starts
    )
    comp.add_pattern(mouth_flow, "mouth")

    # Add purple fill behind mouth
    canvas.dwg.add(canvas.dwg.rect(
        insert=(85, 155),
        size=(127, 30),
        fill="#E1BEE7",
        stroke="none",
        opacity=0.5
    ))
    print("✓ Mouth (wave patterns)")

    # 6. Dendrite branches from corners
    # Top-left corner
    dendrite_tl = DendritePattern(
        width=297,
        height=210,
        num_particles=400,
        attraction_distance=4.0,
        branching_style="radial",
        seed_points=[(20, 20)]
    )
    dendrite_tl.generate(max_attempts=500)
    comp.add_pattern(dendrite_tl, "dendrites")

    # Top-right corner
    dendrite_tr = DendritePattern(
        width=297,
        height=210,
        num_particles=400,
        attraction_distance=4.0,
        branching_style="radial",
        seed_points=[(277, 20)]
    )
    dendrite_tr.generate(max_attempts=500)
    comp.add_pattern(dendrite_tr, "dendrites")

    # Bottom-left corner
    dendrite_bl = DendritePattern(
        width=297,
        height=210,
        num_particles=400,
        attraction_distance=4.0,
        branching_style="radial",
        seed_points=[(20, 190)]
    )
    dendrite_bl.generate(max_attempts=500)
    comp.add_pattern(dendrite_bl, "dendrites")

    # Bottom-right corner
    dendrite_br = DendritePattern(
        width=297,
        height=210,
        num_particles=400,
        attraction_distance=4.0,
        branching_style="radial",
        seed_points=[(277, 190)]
    )
    dendrite_br.generate(max_attempts=500)
    comp.add_pattern(dendrite_br, "dendrites")

    print("✓ Corner dendrites")

    # 7. Add some detail lines around eyes
    canvas.set_layer("details")
    # Eyebrow-like marks
    eyebrow_left = [(90, 75), (130, 72)]
    eyebrow_right = [(167, 72), (207, 75)]
    canvas.add_polyline(eyebrow_left, "details")
    canvas.add_polyline(eyebrow_right, "details")

    # Save
    comp.save("output_portrait.svg")
    print("\n✓ Saved artistic portrait to output_portrait.svg")


if __name__ == "__main__":
    main()
