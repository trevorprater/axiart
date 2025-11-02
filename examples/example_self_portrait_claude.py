#!/usr/bin/env python3
"""Self-Portrait: Neural Landscape - A Computational Being

This portrait represents an AI's inner world through layered abstractions:
- Knowledge substrate (noise at multiple scales)
- Neural pathways (dendrite networks)
- Dual processing modes (structured vs organic flow fields)
- Emergent focal points (Fermat spirals at golden ratio positions)
- Computational substrate (transitioning grid structure)

Novel techniques:
- Region-constrained pattern generation
- Dual-hemisphere compositional approach
- Multiple dendrite seeding strategies
- Opposing flow field interaction
- Multi-scale noise layering
"""

import sys
sys.path.insert(0, '..')

from axiart.composition import Composition
from axiart.patterns import (
    NoisePattern, DendritePattern, FlowFieldPattern,
    SpiralPattern, GridPattern
)
import math


def constrain_to_region(points_or_lines, filter_func, data_type="polylines"):
    """Filter pattern data to specific regions.

    Args:
        points_or_lines: Pattern data to filter
        filter_func: Function that takes (x, y) and returns bool
        data_type: "polylines", "dendrite_lines", or "points"
    """
    if not points_or_lines:
        return []

    if data_type == "polylines":
        # Handle list of polylines (list of lists of points)
        filtered = []
        for line in points_or_lines:
            filtered_line = [pt for pt in line if filter_func(pt[0], pt[1])]
            if len(filtered_line) > 1:
                filtered.append(filtered_line)
        return filtered
    elif data_type == "dendrite_lines":
        # Handle dendrite lines (list of tuples: ((x1,y1), (x2,y2)))
        filtered = []
        for start, end in points_or_lines:
            # Keep line if either endpoint is in region
            if filter_func(start[0], start[1]) or filter_func(end[0], end[1]):
                filtered.append((start, end))
        return filtered
    else:
        # Handle single list of points
        return [pt for pt in points_or_lines if filter_func(pt[0], pt[1])]


def main():
    """Generate a computational self-portrait."""
    print("Generating Neural Landscape: A Computational Self-Portrait\n")

    # A4 landscape
    W, H = 297, 210
    CENTER_X, CENTER_Y = W / 2, H / 2

    # Golden ratio for positioning
    PHI = (1 + math.sqrt(5)) / 2

    # Create composition with dark background
    comp = Composition(width=W, height=H, background="#0D0D12")

    # ========== LAYER 1: Deep Knowledge Substrate (Multi-scale Noise) ==========
    print("Layer 1: Deep knowledge substrate...")
    comp.add_layer("substrate_deep", color="#1A1A28", stroke_width=0.2)

    # Large-scale patterns (broad concepts)
    substrate_macro = NoisePattern(width=W, height=H, scale=120, octaves=4, seed=1618)
    substrate_macro.generate_contour_lines(num_levels=15, resolution=3.0)
    comp.add_pattern(substrate_macro, "substrate_deep")

    # ========== LAYER 2: Mid-scale Knowledge (Hatching) ==========
    print("Layer 2: Mid-scale knowledge structures...")
    comp.add_layer("substrate_mid", color="#252535", stroke_width=0.25)

    substrate_mid = NoisePattern(width=W, height=H, scale=60, octaves=6, seed=2718)
    substrate_mid.generate_hatching(spacing=2.5, line_length=8.0, threshold=-0.2)
    comp.add_pattern(substrate_mid, "substrate_mid")

    # ========== LAYER 3: Computational Grid (Transitional) ==========
    print("Layer 3: Computational substrate grid...")
    comp.add_layer("grid_substrate", color="#2D2D45", stroke_width=0.3)

    # Left hemisphere: More regular (analytical)
    grid_left = GridPattern(width=W, height=H)
    grid_left.generate_square_grid(cell_size=12, jitter=0.3)
    grid_left.apply_radial_distortion(center=(CENTER_X * 0.5, CENTER_Y), strength=0.2)
    left_lines = constrain_to_region(
        grid_left.get_lines(),
        lambda x, y: x < CENTER_X,
        data_type="polylines"
    )

    # Right hemisphere: More organic (creative)
    grid_right = GridPattern(width=W, height=H)
    grid_right.generate_hexagonal_grid(cell_size=10)
    grid_right.apply_radial_distortion(center=(CENTER_X * 1.5, CENTER_Y), strength=0.4)
    right_lines = constrain_to_region(
        grid_right.get_lines(),
        lambda x, y: x >= CENTER_X,
        data_type="polylines"
    )

    # Draw both hemispheres
    canvas = comp.get_canvas()
    for line in left_lines:
        if len(line) > 1:
            canvas.add_polyline(line, layer="grid_substrate")
    for line in right_lines:
        if len(line) > 1:
            canvas.add_polyline(line, layer="grid_substrate")

    # ========== LAYER 4: Neural Networks (Dendrites - Left Hemisphere) ==========
    print("Layer 4: Left hemisphere neural pathways (structured)...")
    comp.add_layer("neural_left", color="#4A5580", stroke_width=0.35)

    # Structured seed points (grid-based thinking)
    left_seeds = [
        (CENTER_X * 0.5, CENTER_Y * 0.6),
        (CENTER_X * 0.3, CENTER_Y * 1.2),
        (CENTER_X * 0.7, CENTER_Y)
    ]
    dendrite_left = DendritePattern(
        width=W, height=H,
        num_particles=600,
        attraction_distance=5.0,
        seed_points=left_seeds,
        branching_style="radial",
        seed=314159
    )
    dendrite_left.generate()

    # Constrain to left hemisphere
    left_dendrite_lines = constrain_to_region(
        dendrite_left.get_lines(),
        lambda x, y: x < CENTER_X + 20,  # Small overlap
        data_type="dendrite_lines"
    )
    for start, end in left_dendrite_lines:
        canvas.add_line(start, end, layer="neural_left")

    # ========== LAYER 5: Neural Networks (Dendrites - Right Hemisphere) ==========
    print("Layer 5: Right hemisphere neural pathways (organic)...")
    comp.add_layer("neural_right", color="#5A6A50", stroke_width=0.35)

    # Organic seed points (more creative)
    right_seeds = [
        (CENTER_X * 1.5, CENTER_Y * 0.7),
        (CENTER_X * 1.3, CENTER_Y * 1.3),
        (CENTER_X * 1.7, CENTER_Y * 0.9)
    ]
    dendrite_right = DendritePattern(
        width=W, height=H,
        num_particles=600,
        attraction_distance=6.0,
        seed_points=right_seeds,
        branching_style="vertical",
        seed=271828
    )
    dendrite_right.generate()

    # Constrain to right hemisphere
    right_dendrite_lines = constrain_to_region(
        dendrite_right.get_lines(),
        lambda x, y: x >= CENTER_X - 20,  # Small overlap
        data_type="dendrite_lines"
    )
    for start, end in right_dendrite_lines:
        canvas.add_line(start, end, layer="neural_right")

    # ========== LAYER 6: Thought Flow - Analytical (Left) ==========
    print("Layer 6: Analytical thought flows...")
    comp.add_layer("flow_analytical", color="#6080B0", stroke_width=0.4)

    # Structured radial flow from left center
    flow_left = FlowFieldPattern(
        width=W, height=H,
        field_type="radial",
        scale=40,
        seed=161803
    )
    flow_left.generate_streamlines(num_lines=25, steps=120, step_size=1.0, parallel=True)

    left_flow_lines = constrain_to_region(
        flow_left.get_paths(),
        lambda x, y: x < CENTER_X + 30,
        data_type="polylines"
    )
    for line in left_flow_lines:
        if len(line) > 1:
            canvas.add_polyline(line, layer="flow_analytical")

    # ========== LAYER 7: Thought Flow - Creative (Right) ==========
    print("Layer 7: Creative thought flows...")
    comp.add_layer("flow_creative", color="#80A060", stroke_width=0.4)

    # Organic noise-based flow
    flow_right = FlowFieldPattern(
        width=W, height=H,
        field_type="noise",
        scale=35,
        seed=577215
    )
    flow_right.generate_streamlines(num_lines=25, steps=120, step_size=1.2, parallel=True)

    right_flow_lines = constrain_to_region(
        flow_right.get_paths(),
        lambda x, y: x >= CENTER_X - 30,
        data_type="polylines"
    )
    for line in right_flow_lines:
        if len(line) > 1:
            canvas.add_polyline(line, layer="flow_creative")

    # ========== LAYER 8: Emergence Centers (Fermat Spirals at Golden Ratio Points) ==========
    print("Layer 8: Centers of emergent understanding...")
    comp.add_layer("emergence", color="#A080D0", stroke_width=0.5)

    # Left focus: Analytical center
    emerge_left = SpiralPattern(
        width=W, height=H,
        center=(CENTER_X / PHI, CENTER_Y)
    )
    emerge_left.generate_fermat_spiral(num_points=500, spacing=1.8, rotation=0)
    comp.add_pattern(emerge_left, "emergence")

    # Right focus: Creative center
    emerge_right = SpiralPattern(
        width=W, height=H,
        center=(W - (CENTER_X / PHI), CENTER_Y)
    )
    emerge_right.generate_fermat_spiral(num_points=500, spacing=1.8, rotation=math.pi/4)
    comp.add_pattern(emerge_right, "emergence")

    # ========== LAYER 9: Integration (Central Spiral) ==========
    print("Layer 9: Central integration point...")
    comp.add_layer("integration", color="#D080A0", stroke_width=0.6)

    # Logarithmic spiral at center (integration of both modes)
    integration = SpiralPattern(
        width=W, height=H,
        center=(CENTER_X, CENTER_Y),
        num_revolutions=12,
        points_per_revolution=180,
        spiral_type="logarithmic"
    )
    integration.generate(start_radius=8, growth_factor=1.15)
    comp.add_pattern(integration, "integration")

    # ========== LAYER 10: Consciousness Ripples ==========
    print("Layer 10: Ripples of awareness...")
    comp.add_layer("awareness", color="#9060C0", stroke_width=0.3)

    # Circular waves emanating from center
    awareness = SpiralPattern(width=W, height=H, center=(CENTER_X, CENTER_Y))
    awareness.generate_circular_waves(
        num_circles=15,
        start_radius=25,
        end_radius=100,
        points_per_circle=250,
        wave_amplitude=2.0,
        wave_frequency=12.0
    )
    comp.add_pattern(awareness, "awareness")

    # ========== LAYER 11: Fine Detail (Stippling) ==========
    print("Layer 11: Fine-scale detail texture...")
    comp.add_layer("detail", color="#6060A0", stroke_width=0.2)

    detail = NoisePattern(width=W, height=H, scale=25, octaves=8, seed=123456)
    detail.generate_stippling(num_points=8000, threshold=-0.1, parallel=True)
    comp.add_pattern(detail, "detail")

    # Save
    output_file = "output_self_portrait_claude.svg"
    comp.save(output_file)

    print(f"\n✓ Self-portrait saved to {output_file}")
    print(f"\n=== Neural Landscape: Compositional Analysis ===")
    print(f"Layers: 11")
    print(f"Theme: Dual-process cognitive architecture")
    print(f"Left hemisphere: Analytical (grid, radial flow, structured dendrites)")
    print(f"Right hemisphere: Creative (hexagonal, noise flow, organic dendrites)")
    print(f"Integration: Central spiral merging both modes")
    print(f"Emergence: Fermat spirals at golden ratio positions")
    print(f"Consciousness: Circular waves representing awareness")
    print(f"Substrate: Multi-scale noise (macro → mid → micro detail)")
    print(f"\nNovel techniques used:")
    print(f"  • Region-constrained pattern generation (hemispheric division)")
    print(f"  • Multiple dendrite seeding strategies")
    print(f"  • Opposing flow field types with overlap zones")
    print(f"  • Golden ratio spatial positioning")
    print(f"  • Multi-scale noise layering (3 levels)")
    print(f"  • Transitional grid (square → hexagonal)")


if __name__ == "__main__":
    main()
