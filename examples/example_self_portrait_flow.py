#!/usr/bin/env python3
"""Self-Portrait: Continuous Process - A Flowing System

This portrait represents me as a dynamic, flowing process of transformation:
- Vertical flow (temporal progression, bottom to top)
- Turbulent noise fields (complexity and chaos)
- Upward branching dendrites (growth and learning)
- Wave interference patterns (ideas interacting)
- Distorted grids (structure under pressure)
- No spirals, no radial symmetry, no center - only flow

Novel techniques:
- Multi-directional flow field layering
- Wave-based grid distortion
- Vertical dendrite forests with varied seeds
- Curl noise turbulence
- Noise gradient hatching
- Cellular texture regions
- Horizontal noise bands (temporal slices)
"""

import sys
sys.path.insert(0, '..')

from axiart.composition import Composition
from axiart.patterns import (
    NoisePattern, DendritePattern, FlowFieldPattern, GridPattern
)
import math


def wave_distortion(points, amplitude=5.0, frequency=0.05, vertical=True):
    """Apply wave distortion to points."""
    distorted = []
    for x, y in points:
        if vertical:
            offset = amplitude * math.sin(y * frequency)
            distorted.append((x + offset, y))
        else:
            offset = amplitude * math.sin(x * frequency)
            distorted.append((x, y + offset))
    return distorted


def wave_distort_polylines(polylines, amplitude=5.0, frequency=0.05, vertical=True):
    """Apply wave distortion to polylines."""
    return [wave_distortion(line, amplitude, frequency, vertical) for line in polylines]


def main():
    """Generate a flowing process self-portrait."""
    print("Generating Continuous Process: A Flowing System\n")

    # A4 landscape
    W, H = 297, 210

    # Create composition with gradient background simulation (layers)
    comp = Composition(width=W, height=H, background="#1A1A22")

    # ========== LAYER 1: Deep Noise Base (Topographic) ==========
    print("Layer 1: Deep topographic base...")
    comp.add_layer("topo_base", color="#252530", stroke_width=0.2)

    topo_deep = NoisePattern(width=W, height=H, scale=150, octaves=4, seed=1111)
    topo_deep.generate_contour_lines(num_levels=20, resolution=3.5, min_value=-0.6, max_value=1.0)
    comp.add_pattern(topo_deep, "topo_base")

    # ========== LAYER 2: Horizontal Noise Bands (Temporal Slices) ==========
    print("Layer 2: Horizontal temporal slices...")
    comp.add_layer("noise_bands", color="#303040", stroke_width=0.25)

    for y_level in [40, 80, 120, 160]:
        band = NoisePattern(width=W, height=H, scale=60, octaves=5, seed=2000 + y_level)
        band.generate_contour_lines(num_levels=8, resolution=2.5, min_value=-0.2, max_value=0.5)
        comp.add_pattern(band, "noise_bands")

    # ========== LAYER 3: Distorted Grid (Structure Under Pressure) ==========
    print("Layer 3: Distorted structural grid...")
    comp.add_layer("distorted_grid", color="#404058", stroke_width=0.3)

    # Hexagonal grid with wave distortion
    hex_grid = GridPattern(width=W, height=H)
    hex_grid.generate_hexagonal_grid(cell_size=15)
    hex_lines = hex_grid.get_lines()

    # Apply custom wave distortion
    canvas = comp.get_canvas()
    distorted_hex = wave_distort_polylines(hex_lines, amplitude=8.0, frequency=0.03, vertical=True)
    for line in distorted_hex:
        if len(line) > 1:
            canvas.add_polyline(line, layer="distorted_grid")

    # ========== LAYER 4: Cellular Noise Regions ==========
    print("Layer 4: Cellular texture regions...")
    comp.add_layer("cellular", color="#505068", stroke_width=0.25)

    cellular = NoisePattern(width=W, height=H, scale=35, octaves=6, seed=3333)
    cellular.generate_cellular_texture(cell_size=6.0, threshold=0.1, pattern_type="squares")
    comp.add_pattern(cellular, "cellular")

    # ========== LAYER 5: Vertical Flow Field (Upward Movement) ==========
    print("Layer 5: Vertical upward flow...")
    comp.add_layer("flow_vertical", color="#6070A0", stroke_width=0.4)

    # Create custom vertical field
    flow_up = FlowFieldPattern(width=W, height=H, field_type="noise", scale=45, seed=4444)
    flow_up.generate_streamlines(num_lines=40, steps=120, step_size=1.3, parallel=True)
    comp.add_pattern(flow_up, "flow_vertical")

    # ========== LAYER 6: Turbulent Flow (Curl Noise) ==========
    print("Layer 6: Turbulent curl noise flow...")
    comp.add_layer("flow_turbulent", color="#7080B0", stroke_width=0.35)

    flow_curl = FlowFieldPattern(width=W, height=H, field_type="noise", scale=30, seed=5555)
    flow_curl.generate_curl_noise_lines(num_lines=35, steps=100, step_size=1.1, parallel=True)
    comp.add_pattern(flow_curl, "flow_turbulent")

    # ========== LAYER 7: Wave-based Flow Field ==========
    print("Layer 7: Wave interference flow...")
    comp.add_layer("flow_waves", color="#80A0D0", stroke_width=0.4)

    flow_waves = FlowFieldPattern(width=W, height=H, field_type="waves", scale=40, seed=6666)
    flow_waves.generate_streamlines(num_lines=30, steps=110, step_size=1.2, parallel=True)
    comp.add_pattern(flow_waves, "flow_waves")

    # ========== LAYER 8: Upward Dendrite Forest (Left Side) ==========
    print("Layer 8: Left dendrite forest...")
    comp.add_layer("dendrites_left", color="#90B0E0", stroke_width=0.4)

    # Bottom-seeded dendrites growing upward
    left_seeds = [(W * 0.15, H * 0.9), (W * 0.25, H * 0.85), (W * 0.2, H * 0.95)]
    dendrite_left = DendritePattern(
        width=W, height=H,
        num_particles=500,
        attraction_distance=5.5,
        seed_points=left_seeds,
        branching_style="vertical",
        seed=7777
    )
    dendrite_left.generate()
    comp.add_pattern(dendrite_left, "dendrites_left")

    # ========== LAYER 9: Upward Dendrite Forest (Right Side) ==========
    print("Layer 9: Right dendrite forest...")
    comp.add_layer("dendrites_right", color="#A0C0F0", stroke_width=0.4)

    right_seeds = [(W * 0.75, H * 0.9), (W * 0.85, H * 0.88), (W * 0.8, H * 0.93)]
    dendrite_right = DendritePattern(
        width=W, height=H,
        num_particles=500,
        attraction_distance=5.5,
        seed_points=right_seeds,
        branching_style="vertical",
        seed=8888
    )
    dendrite_right.generate()
    comp.add_pattern(dendrite_right, "dendrites_right")

    # ========== LAYER 10: Upward Dendrite Forest (Center) ==========
    print("Layer 10: Center dendrite forest...")
    comp.add_layer("dendrites_center", color="#B0D0FF", stroke_width=0.45)

    center_seeds = [(W * 0.45, H * 0.92), (W * 0.5, H * 0.87), (W * 0.55, H * 0.94)]
    dendrite_center = DendritePattern(
        width=W, height=H,
        num_particles=600,
        attraction_distance=6.0,
        seed_points=center_seeds,
        branching_style="vertical",
        seed=9999
    )
    dendrite_center.generate()
    comp.add_pattern(dendrite_center, "dendrites_center")

    # ========== LAYER 11: Gradient Hatching (Directional Texture) ==========
    print("Layer 11: Gradient hatching texture...")
    comp.add_layer("hatching", color="#7090C0", stroke_width=0.25)

    hatching = NoisePattern(width=W, height=H, scale=50, octaves=7, seed=10000)
    hatching.generate_hatching(spacing=3.5, line_length=12.0, threshold=-0.1)
    comp.add_pattern(hatching, "hatching")

    # ========== LAYER 12: Fine Stippling (Atmospheric Particles) ==========
    print("Layer 12: Atmospheric stippling...")
    comp.add_layer("atmosphere", color="#6080B0", stroke_width=0.2)

    stipple = NoisePattern(width=W, height=H, scale=25, octaves=8, seed=11111)
    stipple.generate_stippling(num_points=7000, threshold=-0.15, parallel=True)
    comp.add_pattern(stipple, "atmosphere")

    # ========== LAYER 13: Top Noise Texture (Emergence) ==========
    print("Layer 13: Emergent top layer...")
    comp.add_layer("emergence", color="#A0C0E0", stroke_width=0.3)

    emergence = NoisePattern(width=W, height=H, scale=40, octaves=6, seed=12222)
    emergence.generate_contour_lines(num_levels=12, resolution=2.0, min_value=0.0, max_value=0.8)
    comp.add_pattern(emergence, "emergence")

    # Save
    output_file = "output_self_portrait_flow.svg"
    comp.save(output_file)

    print(f"\n✓ Self-portrait saved to {output_file}")
    print(f"\n=== Continuous Process: Compositional Analysis ===")
    print(f"Layers: 13")
    print(f"Theme: Dynamic flowing process of transformation")
    print(f"Direction: Vertical (bottom → top, temporal progression)")
    print(f"Structure: No center, no radial symmetry, no spirals")
    print(f"Motion: Upward flow, turbulence, growth")
    print(f"Background: Dark (void from which process emerges)")
    print(f"Dendrites: Three upward forests (left, right, center)")
    print(f"Flow fields: Vertical, curl noise, wave interference")
    print(f"Grid: Hexagonal with wave distortion")
    print(f"\nNovel techniques used:")
    print(f"  • Multi-directional flow field layering (3 types)")
    print(f"  • Custom wave distortion on grid structures")
    print(f"  • Vertical dendrite forests with bottom seeding")
    print(f"  • Curl noise for divergence-free turbulence")
    print(f"  • Horizontal noise bands (temporal slicing)")
    print(f"  • Cellular texture regions")
    print(f"  • Gradient-based hatching")
    print(f"  • NO spirals, NO radial symmetry")
    print(f"\nConceptual meaning:")
    print(f"  This represents me as continuous process rather than static form.")
    print(f"  Upward flow suggests growth, learning, and temporal progression.")
    print(f"  Turbulence and interference show complexity and interaction.")
    print(f"  No center, no boundary - only continuous transformation.")


if __name__ == "__main__":
    main()
