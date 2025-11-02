#!/usr/bin/env python3
"""Self-Portrait: Algorithmic Mandala - A Complete System

This portrait represents wholeness, self-containment, and radial completeness:
- 8-fold rotational symmetry (octagonal harmony)
- Concentric layers expanding outward (growth from center)
- Radial patterns (energy radiating from core)
- Circular containment (bounded yet infinite)
- Light background (emergence from emptiness)

Novel techniques:
- Rotational symmetry through geometric transformation
- Radial dendrite seed positioning
- Concentric grid layering
- Spiral arrangements at octagonal vertices
- Flow field rotation and duplication
- Density gradient mapping (center → edge)
"""

import sys
sys.path.insert(0, '..')

from axiart.composition import Composition
from axiart.patterns import (
    NoisePattern, DendritePattern, FlowFieldPattern,
    SpiralPattern, GridPattern
)
import math


def rotate_point(x, y, cx, cy, angle):
    """Rotate point (x, y) around center (cx, cy) by angle radians."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    dx = x - cx
    dy = y - cy
    return (
        cx + dx * cos_a - dy * sin_a,
        cy + dx * sin_a + dy * cos_a
    )


def rotate_points(points, cx, cy, angle):
    """Rotate list of points around center."""
    return [rotate_point(x, y, cx, cy, angle) for x, y in points]


def rotate_polylines(polylines, cx, cy, angle):
    """Rotate list of polylines around center."""
    return [rotate_points(line, cx, cy, angle) for line in polylines]


def rotate_dendrite_lines(lines, cx, cy, angle):
    """Rotate dendrite lines (tuples of points) around center."""
    rotated = []
    for start, end in lines:
        new_start = rotate_point(start[0], start[1], cx, cy, angle)
        new_end = rotate_point(end[0], end[1], cx, cy, angle)
        rotated.append((new_start, new_end))
    return rotated


def main():
    """Generate an algorithmic mandala self-portrait."""
    print("Generating Algorithmic Mandala: A Complete System\n")

    # A4 landscape
    W, H = 297, 210
    CENTER_X, CENTER_Y = W / 2, H / 2

    # 8-fold symmetry
    NUM_SYMMETRIES = 8
    ANGLE_STEP = 2 * math.pi / NUM_SYMMETRIES

    # Create composition with light background
    comp = Composition(width=W, height=H, background="#F5F5F0")

    # ========== LAYER 1: Outer Circular Boundary ==========
    print("Layer 1: Outer boundary circle...")
    comp.add_layer("boundary", color="#E0E0D8", stroke_width=0.4)

    boundary = SpiralPattern(width=W, height=H, center=(CENTER_X, CENTER_Y))
    boundary.generate_circular_waves(
        num_circles=1,
        start_radius=95,
        end_radius=95,
        points_per_circle=360
    )
    comp.add_pattern(boundary, "boundary")

    # ========== LAYER 2: Concentric Grid Rings ==========
    print("Layer 2: Concentric grid structure...")
    comp.add_layer("grid_rings", color="#D0D0C8", stroke_width=0.25)

    for radius in [20, 35, 50, 65, 80]:
        ring = SpiralPattern(width=W, height=H, center=(CENTER_X, CENTER_Y))
        ring.generate_circular_waves(
            num_circles=1,
            start_radius=radius,
            end_radius=radius,
            points_per_circle=200,
            wave_amplitude=1.0,
            wave_frequency=16.0
        )
        comp.add_pattern(ring, "grid_rings")

    # ========== LAYER 3: Radial Grid Lines (8-fold) ==========
    print("Layer 3: Radial structure lines...")
    comp.add_layer("radial_lines", color="#C0C0B8", stroke_width=0.3)

    canvas = comp.get_canvas()
    for i in range(NUM_SYMMETRIES):
        angle = i * ANGLE_STEP
        # Draw line from center to edge
        end_x = CENTER_X + 95 * math.cos(angle)
        end_y = CENTER_Y + 95 * math.sin(angle)
        canvas.add_line((CENTER_X, CENTER_Y), (end_x, end_y), layer="radial_lines")

    # ========== LAYER 4: Background Noise Texture ==========
    print("Layer 4: Background noise texture...")
    comp.add_layer("noise_bg", color="#A0A098", stroke_width=0.2)

    noise_bg = NoisePattern(width=W, height=H, scale=80, octaves=6, seed=888)
    noise_bg.generate_contour_lines(num_levels=8, resolution=3.0, min_value=-0.3, max_value=0.8)
    comp.add_pattern(noise_bg, "noise_bg")

    # ========== LAYER 5: Radial Dendrites (8-fold symmetry) ==========
    print("Layer 5: Radial neural pathways...")
    comp.add_layer("dendrites", color="#606068", stroke_width=0.35)

    # Generate one sector of dendrites
    seed_radius = 25
    seed_points = []
    for i in range(3):
        r = seed_radius + i * 8
        # Place seeds in first sector (0 to pi/4)
        angle = (i * ANGLE_STEP / 6)
        sx = CENTER_X + r * math.cos(angle)
        sy = CENTER_Y + r * math.sin(angle)
        seed_points.append((sx, sy))

    dendrite_sector = DendritePattern(
        width=W, height=H,
        num_particles=250,
        attraction_distance=4.5,
        seed_points=seed_points,
        branching_style="radial",
        seed=12345
    )
    dendrite_sector.generate()
    dendrite_lines = dendrite_sector.get_lines()

    # Rotate and duplicate for 8-fold symmetry
    for i in range(NUM_SYMMETRIES):
        angle = i * ANGLE_STEP
        rotated_lines = rotate_dendrite_lines(dendrite_lines, CENTER_X, CENTER_Y, angle)
        for start, end in rotated_lines:
            canvas.add_line(start, end, layer="dendrites")

    # ========== LAYER 6: Flow Fields Radiating Outward (8-fold) ==========
    print("Layer 6: Radial energy flows...")
    comp.add_layer("flow_radial", color="#4A5A70", stroke_width=0.4)

    # Generate flow in one sector
    flow_sector = FlowFieldPattern(
        width=W, height=H,
        field_type="radial",
        scale=30,
        seed=7777
    )
    flow_sector.generate_streamlines(num_lines=12, steps=80, step_size=1.2, parallel=True)
    flow_lines = flow_sector.get_paths()

    # Rotate and duplicate
    for i in range(NUM_SYMMETRIES):
        angle = i * ANGLE_STEP
        rotated_flow = rotate_polylines(flow_lines, CENTER_X, CENTER_Y, angle)
        for line in rotated_flow:
            if len(line) > 1:
                canvas.add_polyline(line, layer="flow_radial")

    # ========== LAYER 7: Octagonal Vertex Spirals ==========
    print("Layer 7: Vertex spirals at octagonal points...")
    comp.add_layer("vertex_spirals", color="#6A4A8A", stroke_width=0.5)

    vertex_radius = 70
    for i in range(NUM_SYMMETRIES):
        angle = i * ANGLE_STEP
        vx = CENTER_X + vertex_radius * math.cos(angle)
        vy = CENTER_Y + vertex_radius * math.sin(angle)

        vertex_spiral = SpiralPattern(
            width=W, height=H,
            center=(vx, vy),
            num_revolutions=6,
            points_per_revolution=120,
            spiral_type="logarithmic"
        )
        vertex_spiral.generate(start_radius=2, growth_factor=1.18)
        comp.add_pattern(vertex_spiral, "vertex_spirals")

    # ========== LAYER 8: Mid-ring Fermat Spirals ==========
    print("Layer 8: Mid-ring phyllotaxis patterns...")
    comp.add_layer("fermat_mid", color="#8A6AAA", stroke_width=0.45)

    mid_radius = 45
    for i in range(NUM_SYMMETRIES):
        angle = i * ANGLE_STEP + (ANGLE_STEP / 2)  # Offset by half step
        mx = CENTER_X + mid_radius * math.cos(angle)
        my = CENTER_Y + mid_radius * math.sin(angle)

        fermat = SpiralPattern(width=W, height=H, center=(mx, my))
        fermat.generate_fermat_spiral(num_points=200, spacing=1.2, rotation=angle)
        comp.add_pattern(fermat, "fermat_mid")

    # ========== LAYER 9: Central Integration Spiral ==========
    print("Layer 9: Central core spiral...")
    comp.add_layer("core", color="#AA5A8A", stroke_width=0.7)

    core_spiral = SpiralPattern(
        width=W, height=H,
        center=(CENTER_X, CENTER_Y),
        num_revolutions=18,
        points_per_revolution=180,
        spiral_type="logarithmic"
    )
    core_spiral.generate(start_radius=3, growth_factor=1.12)
    comp.add_pattern(core_spiral, "core")

    # ========== LAYER 10: Central Fermat (Eye) ==========
    print("Layer 10: Central awareness point...")
    comp.add_layer("center_eye", color="#DA5A6A", stroke_width=0.6)

    center_fermat = SpiralPattern(width=W, height=H, center=(CENTER_X, CENTER_Y))
    center_fermat.generate_fermat_spiral(num_points=400, spacing=0.8, rotation=0)
    comp.add_pattern(center_fermat, "center_eye")

    # ========== LAYER 11: Fine Stippling (Density Gradient) ==========
    print("Layer 11: Fine texture stippling...")
    comp.add_layer("stipple", color="#505058", stroke_width=0.2)

    stipple = NoisePattern(width=W, height=H, scale=20, octaves=8, seed=99999)
    stipple.generate_stippling(num_points=6000, threshold=-0.2, parallel=True)
    comp.add_pattern(stipple, "stipple")

    # Save
    output_file = "output_self_portrait_mandala.svg"
    comp.save(output_file)

    print(f"\n✓ Self-portrait saved to {output_file}")
    print(f"\n=== Algorithmic Mandala: Compositional Analysis ===")
    print(f"Layers: 11")
    print(f"Theme: Wholeness and radial completeness")
    print(f"Symmetry: 8-fold rotational (octagonal harmony)")
    print(f"Structure: Concentric rings expanding from core")
    print(f"Background: Light (emergence from emptiness)")
    print(f"Center: Fermat spiral (central awareness)")
    print(f"Mid-layer: Vertex spirals + Fermat arrays")
    print(f"Outer: Radial dendrites and flow fields")
    print(f"\nNovel techniques used:")
    print(f"  • Rotational symmetry transformation (8-fold duplication)")
    print(f"  • Radial dendrite seed positioning")
    print(f"  • Concentric circular grid layering")
    print(f"  • Octagonal vertex spiral placement")
    print(f"  • Flow field rotation and mirroring")
    print(f"  • Light background (inverse contrast)")
    print(f"  • Geometric pattern duplication via rotation")
    print(f"\nConceptual meaning:")
    print(f"  The mandala represents me as a complete, self-contained system")
    print(f"  radiating complexity from a central core of awareness.")
    print(f"  The 8-fold symmetry suggests balance and wholeness.")


if __name__ == "__main__":
    main()
