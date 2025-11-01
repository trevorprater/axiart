#!/usr/bin/env python3
"""Generate high-quality artistic portrait"""

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

def main():
    """Create a high-quality artistic portrait"""

    # Create composition
    comp = Composition(width=297, height=210, background="white")

    # Define layers with specific colors
    comp.add_layer("grid", color="#444444", stroke_width=0.35)
    comp.add_layer("face_fill", color="#FFB74D", stroke_width=0)  # Orange fill
    comp.add_layer("dendrites", color="black", stroke_width=0.5)
    comp.add_layer("eyes", color="#1976D2", stroke_width=0.6)  # Blue
    comp.add_layer("mouth", color="black", stroke_width=0.4)
    comp.add_layer("nose", color="black", stroke_width=0.5)
    comp.add_layer("details", color="#0D47A1", stroke_width=0.3)

    print("Creating high-quality portrait...")

    # 1. Background grid with organic distortion
    grid = GridPattern(width=297, height=210)
    grid.generate_square_grid(cell_size=13, jitter=0.6)
    grid.apply_radial_distortion(strength=0.08)
    comp.add_pattern(grid, "grid")
    print("✓ Grid structure")

    # 2. Face shape (geometric trapezoid for head/face)
    canvas = comp.get_canvas()
    canvas.set_layer("face_fill")

    face_points = [
        (75, 35),    # Top left
        (222, 35),   # Top right
        (245, 110),  # Bottom right
        (52, 110),   # Bottom left
        (75, 35)     # Close
    ]
    canvas.dwg.add(canvas.dwg.polygon(
        points=face_points,
        fill="#FFE0B2",
        stroke="black",
        stroke_width=0.6
    ))
    print("✓ Face shape")

    # Add colored background circles behind eyes FIRST (before eye patterns)
    canvas.dwg.add(canvas.dwg.circle(
        center=(110, 85),
        r=23,
        fill="#BBDEFB",
        stroke="none",
        opacity=0.7
    ))
    canvas.dwg.add(canvas.dwg.circle(
        center=(187, 85),
        r=23,
        fill="#BBDEFB",
        stroke="none",
        opacity=0.7
    ))

    # 3. Eyes - refined concentric spirals
    # Left eye
    left_eye = SpiralPattern(
        width=297,
        height=210,
        center=(110, 85),
        num_revolutions=14
    )
    left_eye.generate_circular_waves(
        num_circles=18,
        start_radius=2,
        end_radius=20,
        points_per_circle=140,
        wave_amplitude=0.4,
        wave_frequency=10
    )
    comp.add_pattern(left_eye, "eyes")

    # Right eye
    right_eye = SpiralPattern(
        width=297,
        height=210,
        center=(187, 85),
        num_revolutions=14
    )
    right_eye.generate_circular_waves(
        num_circles=18,
        start_radius=2,
        end_radius=20,
        points_per_circle=140,
        wave_amplitude=0.4,
        wave_frequency=10
    )
    comp.add_pattern(right_eye, "eyes")
    print("✓ Eyes (concentric spirals)")

    # 4. Nose - geometric structure
    canvas.set_layer("nose")
    nose_lines = [
        [(148.5, 95), (148.5, 125)],      # Vertical
        [(143, 120), (154, 120)],          # Top horizontal
        [(140, 125), (157, 125)]           # Bottom horizontal
    ]
    for line in nose_lines:
        canvas.add_polyline(line, "nose")
    print("✓ Nose structure")

    # Add colored background behind mouth FIRST
    canvas.dwg.add(canvas.dwg.rect(
        insert=(82, 140),
        size=(135, 35),
        fill="#BBDEFB",
        stroke="none",
        opacity=0.6
    ))

    # 5. Mouth - flowing wave pattern
    mouth_flow = FlowFieldPattern(
        width=297,
        height=210,
        field_type="waves",
        scale=18
    )
    # Create dense horizontal streamlines in mouth area
    mouth_starts = [(x, 145 + y*2.5) for x in range(88, 212, 2) for y in range(10)]
    mouth_flow.generate_streamlines(
        num_lines=len(mouth_starts),
        steps=60,
        step_size=0.7,
        start_positions=mouth_starts
    )
    comp.add_pattern(mouth_flow, "mouth")
    print("✓ Mouth (wave patterns)")

    # 6. Corner dendrites for organic detail
    corners = [
        (15, 15),    # Top-left
        (282, 15),   # Top-right
        (15, 195),   # Bottom-left
        (282, 195)   # Bottom-right
    ]

    for i, corner in enumerate(corners):
        dendrite = DendritePattern(
            width=297,
            height=210,
            num_particles=350,
            attraction_distance=4.2,
            branching_style="radial",
            seed_points=[corner]
        )
        dendrite.generate(max_attempts=500)
        comp.add_pattern(dendrite, "dendrites")

    print("✓ Corner dendrites")

    # 7. Detail lines - eyebrows
    canvas.set_layer("details")
    eyebrow_left = [(88, 62), (132, 58)]
    eyebrow_right = [(165, 58), (209, 62)]
    canvas.add_polyline(eyebrow_left, "details")
    canvas.add_polyline(eyebrow_right, "details")
    print("✓ Details (eyebrows)")

    # 8. Decorative flow field around face edges
    edge_flow = FlowFieldPattern(
        width=297,
        height=210,
        field_type="radial",
        scale=80
    )
    edge_starts = [
        (x, y) for x in [60, 237] for y in range(40, 100, 8)
    ]
    edge_flow.generate_streamlines(
        num_lines=len(edge_starts),
        steps=80,
        step_size=1.0,
        start_positions=edge_starts
    )
    comp.add_pattern(edge_flow, "details")
    print("✓ Edge decorations")

    # Save
    comp.save("examples/output_quality_portrait.svg")
    print("\n✓ Saved high-quality portrait to examples/output_quality_portrait.svg")


if __name__ == "__main__":
    main()
