#!/usr/bin/env python3
"""Portrait: Trevor - Algorithmic Portrait from Photo

This portrait captures key features through algorithmic patterns:
- Round glasses (geometric circles)
- Curly beard (dendrite branching from chin)
- Curly side hair (dendrite clusters)
- Facial structure (filled shapes + contour shading)
- Hoodie (filled base shape)
- Atmospheric background (flow fields + noise)

Techniques:
- Filled shapes for solid forms (face, glasses, hoodie)
- Dendrite generation for organic textures (hair, beard)
- Noise contours for facial shading
- Stippling for skin texture
- Flow field background atmosphere
- Hatching for clothing texture
"""

import sys
sys.path.insert(0, '..')

from axiart.composition import Composition
from axiart.patterns import (
    NoisePattern, DendritePattern, FlowFieldPattern, SpiralPattern
)
from axiart.shapes import Circle, add_filled_shape
import math


def main():
    """Generate an algorithmic portrait of Trevor."""
    print("Generating Algorithmic Portrait: Trevor\n")

    # Portrait orientation (swap W and H)
    W, H = 210, 297
    CENTER_X = W / 2

    # Key vertical positions
    HEAD_CENTER_Y = H * 0.35
    CHIN_Y = HEAD_CENTER_Y + 55
    GLASSES_Y = HEAD_CENTER_Y - 5

    # Create composition
    comp = Composition(width=W, height=H, background="#E8E8E0")

    # ========== LAYER 1: Background Flow Field ==========
    print("Layer 1: Background atmosphere...")
    comp.add_layer("bg_flow", color="#C8C8C0", stroke_width=0.3)

    bg_flow = FlowFieldPattern(width=W, height=H, field_type="noise", scale=60, seed=7001)
    bg_flow.generate_streamlines(num_lines=30, steps=100, step_size=1.5, parallel=True)
    comp.add_pattern(bg_flow, "bg_flow")

    # ========== LAYER 2: Background Noise Texture ==========
    print("Layer 2: Background texture...")
    comp.add_layer("bg_noise", color="#D0D0C8", stroke_width=0.2)

    bg_noise = NoisePattern(width=W, height=H, scale=100, octaves=4, seed=7002)
    bg_noise.generate_contour_lines(num_levels=10, resolution=4.0, min_value=-0.5, max_value=0.5)
    comp.add_pattern(bg_noise, "bg_noise")

    # ========== LAYER 3: Hoodie Base (Filled Shape) ==========
    print("Layer 3: Hoodie base...")
    comp.add_layer("hoodie_fill", color="#1A1A1A", stroke_width=0)
    comp.add_layer("hoodie_outline", color="#0A0A0A", stroke_width=0.6)

    canvas = comp.get_canvas()

    # Hoodie shape (shoulders and neck area)
    hoodie_points = [
        (0, H),  # bottom left
        (0, H * 0.65),  # left shoulder
        (CENTER_X - 45, H * 0.55),  # left neck
        (CENTER_X - 35, H * 0.5),  # left neck curve
        (CENTER_X, H * 0.48),  # center neck
        (CENTER_X + 35, H * 0.5),  # right neck curve
        (CENTER_X + 45, H * 0.55),  # right neck
        (W, H * 0.65),  # right shoulder
        (W, H),  # bottom right
    ]
    canvas.dwg.add(canvas.dwg.polygon(
        points=hoodie_points,
        fill="#1A1A1A",
        stroke="#0A0A0A",
        stroke_width=0.6
    ))

    # ========== LAYER 4: Head/Face Base (Filled Ellipse) ==========
    print("Layer 4: Face base...")
    comp.add_layer("face_fill", color="#F4D4B0", stroke_width=0)
    comp.add_layer("face_outline", color="#E0C0A0", stroke_width=0.5)

    # Face ellipse
    face_ellipse = canvas.dwg.ellipse(
        center=(CENTER_X, HEAD_CENTER_Y),
        r=(42, 55),
        fill="#F4D4B0",
        stroke="#E0C0A0",
        stroke_width=0.5
    )
    canvas.dwg.add(face_ellipse)

    # ========== LAYER 5: Facial Shading (Noise Contours) ==========
    print("Layer 5: Facial shading contours...")
    comp.add_layer("face_shading", color="#D0B090", stroke_width=0.25)

    face_shade = NoisePattern(width=W, height=H, scale=40, octaves=6, seed=7003)
    face_shade.generate_contour_lines(num_levels=8, resolution=2.0, min_value=-0.2, max_value=0.6)
    comp.add_pattern(face_shade, "face_shading")

    # ========== LAYER 6: Skin Texture (Stippling) ==========
    print("Layer 6: Skin texture...")
    comp.add_layer("skin_texture", color="#E0C0A0", stroke_width=0.15)

    skin_stipple = NoisePattern(width=W, height=H, scale=25, octaves=7, seed=7004)
    skin_stipple.generate_stippling(num_points=3000, threshold=0.0, parallel=True)
    comp.add_pattern(skin_stipple, "skin_texture")

    # ========== LAYER 7: Glasses Frames (Filled Circles) ==========
    print("Layer 7: Glasses...")
    comp.add_layer("glasses_fill", color="none", stroke_width=0)
    comp.add_layer("glasses_frame", color="#2A2A2A", stroke_width=1.2)

    # Left lens
    left_glass = canvas.dwg.circle(
        center=(CENTER_X - 20, GLASSES_Y),
        r=15,
        fill="none",
        stroke="#2A2A2A",
        stroke_width=1.2
    )
    canvas.dwg.add(left_glass)

    # Right lens
    right_glass = canvas.dwg.circle(
        center=(CENTER_X + 20, GLASSES_Y),
        r=15,
        fill="none",
        stroke="#2A2A2A",
        stroke_width=1.2
    )
    canvas.dwg.add(right_glass)

    # Bridge
    canvas.add_line(
        (CENTER_X - 5, GLASSES_Y),
        (CENTER_X + 5, GLASSES_Y),
        layer="glasses_frame"
    )

    # ========== LAYER 8: Curly Side Hair - Left (Dendrites) ==========
    print("Layer 8: Left side hair...")
    comp.add_layer("hair_left", color="#3A2A1A", stroke_width=0.4)

    left_hair_seeds = [
        (CENTER_X - 45, HEAD_CENTER_Y - 20),
        (CENTER_X - 50, HEAD_CENTER_Y),
        (CENTER_X - 48, HEAD_CENTER_Y + 20),
        (CENTER_X - 42, HEAD_CENTER_Y - 35)
    ]
    hair_left = DendritePattern(
        width=W, height=H,
        num_particles=400,
        attraction_distance=4.0,
        seed_points=left_hair_seeds,
        branching_style="radial",
        seed=7005
    )
    hair_left.generate()
    comp.add_pattern(hair_left, "hair_left")

    # ========== LAYER 9: Curly Side Hair - Right (Dendrites) ==========
    print("Layer 9: Right side hair...")
    comp.add_layer("hair_right", color="#3A2A1A", stroke_width=0.4)

    right_hair_seeds = [
        (CENTER_X + 45, HEAD_CENTER_Y - 20),
        (CENTER_X + 50, HEAD_CENTER_Y),
        (CENTER_X + 48, HEAD_CENTER_Y + 20),
        (CENTER_X + 42, HEAD_CENTER_Y - 35)
    ]
    hair_right = DendritePattern(
        width=W, height=H,
        num_particles=400,
        attraction_distance=4.0,
        seed_points=right_hair_seeds,
        branching_style="radial",
        seed=7006
    )
    hair_right.generate()
    comp.add_pattern(hair_right, "hair_right")

    # ========== LAYER 10: Beard (Dendrites Growing from Chin) ==========
    print("Layer 10: Beard...")
    comp.add_layer("beard", color="#2A1A0A", stroke_width=0.35)

    beard_seeds = [
        (CENTER_X, CHIN_Y),
        (CENTER_X - 15, CHIN_Y - 5),
        (CENTER_X + 15, CHIN_Y - 5),
        (CENTER_X - 25, CHIN_Y - 10),
        (CENTER_X + 25, CHIN_Y - 10),
        (CENTER_X - 10, CHIN_Y + 3),
        (CENTER_X + 10, CHIN_Y + 3),
    ]
    beard = DendritePattern(
        width=W, height=H,
        num_particles=600,
        attraction_distance=4.5,
        seed_points=beard_seeds,
        branching_style="radial",
        seed=7007
    )
    beard.generate()
    comp.add_pattern(beard, "beard")

    # ========== LAYER 11: Mustache Area (Smaller Dendrites) ==========
    print("Layer 11: Mustache...")
    comp.add_layer("mustache", color="#2A1A0A", stroke_width=0.3)

    mustache_seeds = [
        (CENTER_X - 12, HEAD_CENTER_Y + 18),
        (CENTER_X + 12, HEAD_CENTER_Y + 18),
        (CENTER_X - 6, HEAD_CENTER_Y + 20),
        (CENTER_X + 6, HEAD_CENTER_Y + 20),
    ]
    mustache = DendritePattern(
        width=W, height=H,
        num_particles=250,
        attraction_distance=3.5,
        seed_points=mustache_seeds,
        branching_style="horizontal",
        seed=7008
    )
    mustache.generate()
    comp.add_pattern(mustache, "mustache")

    # ========== LAYER 12: Hoodie Texture (Hatching) ==========
    print("Layer 12: Hoodie texture...")
    comp.add_layer("hoodie_texture", color="#0A0A0A", stroke_width=0.2)

    hoodie_texture = NoisePattern(width=W, height=H, scale=45, octaves=5, seed=7009)
    hoodie_texture.generate_hatching(spacing=4.0, line_length=10.0, threshold=-0.3)
    comp.add_pattern(hoodie_texture, "hoodie_texture")

    # ========== LAYER 13: Fine Details (Eye Accent Dots) ==========
    print("Layer 13: Eye details...")
    comp.add_layer("eyes", color="#1A1A1A", stroke_width=2.0)

    # Simple eye dots behind glasses
    canvas.add_points([(CENTER_X - 20, GLASSES_Y + 2)], layer="eyes")
    canvas.add_points([(CENTER_X + 20, GLASSES_Y + 2)], layer="eyes")

    # Save
    output_file = "output_portrait_trevor.svg"
    comp.save(output_file)

    print(f"\n✓ Portrait saved to {output_file}")
    print(f"\n=== Algorithmic Portrait Analysis ===")
    print(f"Subject: Trevor")
    print(f"Layers: 13")
    print(f"Techniques:")
    print(f"  • Filled shapes for solid forms (face, hoodie, glasses)")
    print(f"  • Dendrite branching for organic textures (beard, hair)")
    print(f"  • Noise contours for shading and depth")
    print(f"  • Stippling for skin texture (3000 points)")
    print(f"  • Flow field atmospheric background")
    print(f"  • Hatching for fabric texture")
    print(f"\nKey features captured:")
    print(f"  ✓ Round glasses (geometric circles)")
    print(f"  ✓ Curly beard (600 dendrite particles)")
    print(f"  ✓ Curly side hair (800 dendrite particles)")
    print(f"  ✓ Balding top (minimal hair in upper region)")
    print(f"  ✓ Black hoodie (filled polygon + hatching)")
    print(f"  ✓ Facial structure (ellipse + shading)")


if __name__ == "__main__":
    main()
