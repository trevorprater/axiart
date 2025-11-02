#!/usr/bin/env python3
"""Example: Warped Space - Showcase of Distortion Effects"""

import sys
sys.path.insert(0, '..')

from axiart.composition import Composition
from axiart.patterns import GridPattern, FlowFieldPattern, NoisePattern, SpiralPattern


def main():
    """
    Warped Space: Multiple layers of distortion creating a gravitational lens effect.

    Demonstrates:
    - Radial distortion at varying strengths
    - Grid jitter for texture
    - Noise contours for organic warping
    - Flow fields bending around center
    - Spiral as gravitational center
    """
    print("Generating Warped Space composition...")

    # Create composition with purple accent
    comp = Composition(width=297, height=210, background="#0A0A0F")

    # Layer 1: Outer distorted grid (heavy warping)
    comp.add_layer("outer_grid", color="#2D2D40", stroke_width=0.3)
    outer = GridPattern(width=297, height=210)
    outer.generate_square_grid(cell_size=25, jitter=0.0)
    outer.apply_radial_distortion(center=(148.5, 105), strength=0.9)
    comp.add_pattern(outer, "outer_grid")
    print("  ✓ Outer grid warped (strength: 0.9)")

    # Layer 2: Middle hexagonal grid (medium warping)
    comp.add_layer("hex_grid", color="#404060", stroke_width=0.4)
    middle = GridPattern(width=297, height=210)
    middle.generate_hexagonal_grid(cell_size=12)
    middle.apply_radial_distortion(center=(148.5, 105), strength=0.6)
    comp.add_pattern(middle, "hex_grid")
    print("  ✓ Hexagonal grid warped (strength: 0.6)")

    # Layer 3: Inner grid with jitter (light warping + randomness)
    comp.add_layer("inner_grid", color="#6060A0", stroke_width=0.35)
    inner = GridPattern(width=297, height=210)
    inner.generate_square_grid(cell_size=8, jitter=1.2)
    inner.apply_radial_distortion(center=(148.5, 105), strength=0.3)
    comp.add_pattern(inner, "inner_grid")
    print("  ✓ Inner jittered grid warped (strength: 0.3)")

    # Layer 4: Noise contours (organic warping lines)
    comp.add_layer("noise_field", color="#8080C0", stroke_width=0.3)
    noise = NoisePattern(width=297, height=210, scale=60, octaves=6, seed=42)
    noise.generate_contour_lines(num_levels=25, resolution=2.0)
    comp.add_pattern(noise, "noise_field")
    print("  ✓ Noise contours generated (25 levels)")

    # Layer 5: Flow field bending around center
    comp.add_layer("flow_lines", color="#A080FF", stroke_width=0.5)
    flow = FlowFieldPattern(width=297, height=210, field_type="radial", scale=40, seed=123)
    flow.generate_streamlines(num_lines=40, steps=150, step_size=1.2, parallel=True)
    comp.add_pattern(flow, "flow_lines")
    print("  ✓ Flow field generated (40 streamlines)")

    # Layer 6: Central spiral (gravitational singularity)
    comp.add_layer("singularity", color="#D080FF", stroke_width=0.8)
    center_spiral = SpiralPattern(
        width=297, height=210,
        center=(148.5, 105),
        num_revolutions=15,
        points_per_revolution=200,
        spiral_type="logarithmic"
    )
    center_spiral.generate(start_radius=5, growth_factor=1.2)
    comp.add_pattern(center_spiral, "singularity")
    print("  ✓ Central singularity spiral")

    # Layer 7: Outer ripples
    comp.add_layer("ripples", color="#9060C0", stroke_width=0.25)
    ripples = SpiralPattern(width=297, height=210, center=(148.5, 105))
    ripples.generate_circular_waves(
        num_circles=20,
        start_radius=20,
        end_radius=140,
        points_per_circle=300,
        wave_amplitude=3.0,
        wave_frequency=8.0
    )
    comp.add_pattern(ripples, "ripples")
    print("  ✓ Gravitational ripples")

    # Save
    comp.save("output_warped_space.svg")
    print("\n✓ Saved to output_warped_space.svg")
    print(f"  Layers: 7")
    print(f"  Theme: Warped spacetime with gravitational lens effect")
    print(f"  Distortion types: Radial (3 strengths), jitter, noise, flow field")


if __name__ == "__main__":
    main()
