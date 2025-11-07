#!/usr/bin/env python3
"""
Code Infographic: What IS axiart?

Shows capabilities, patterns, architecture - not abstract circles.
"""

from axiart.composition import Composition
from axiart.shapes import Circle, Rectangle
from axiart.patterns.dendrite import DendritePattern
from axiart.patterns.spiral import SpiralPattern
from axiart.patterns.grid import GridPattern
from axiart.patterns.noise import NoisePattern
from axiart.patterns.flow_field import FlowFieldPattern
from axiart.patterns.voronoi import VoronoiPattern
from axiart.patterns.lsystem import LSystemPattern
from axiart.patterns.truchet import TruchetPattern

# Large canvas for detailed infographic
width, height = 297, 210
comp = Composition(width, height)

# Layers
comp.add_layer("background", color="#F8F8F8", stroke_width=0.1)
comp.add_layer("structure", color="#DDDDDD", stroke_width=0.3)
comp.add_layer("patterns", color="black", stroke_width=0.3)
comp.add_layer("highlights", color="#4A90E2", stroke_width=0.4)
comp.add_layer("annotations", color="#333333", stroke_width=0.3)

canvas = comp.get_canvas()

print("Generating axiart infographic...")

# Title
canvas.dwg.add(canvas.dwg.text(
    'AXIART', insert=(10, 15),
    fill='black', font_size='16pt', font_family='monospace', font_weight='bold'
))

canvas.dwg.add(canvas.dwg.text(
    'Algorithmic Art for Pen Plotters', insert=(10, 25),
    fill='#666666', font_size='7pt', font_family='monospace'
))

# Architecture section (top left)
canvas.dwg.add(canvas.dwg.text(
    'ARCHITECTURE', insert=(10, 45),
    fill='black', font_size='8pt', font_family='monospace', font_weight='bold'
))

# Python → Rust boxes
py_box = Rectangle(10, 50, 50, 20)
canvas.add_polyline(py_box.get_points(), "structure")
canvas.dwg.add(canvas.dwg.text(
    'Python API', insert=(17, 63),
    fill='black', font_size='6pt', font_family='monospace'
))

rust_box = Rectangle(70, 50, 50, 20)
canvas.add_polyline(rust_box.get_points(), "structure")
canvas.dwg.add(canvas.dwg.text(
    'Rust Core', insert=(80, 63),
    fill='black', font_size='6pt', font_family='monospace'
))

# Arrow
canvas.add_line((60, 60), (70, 60), "patterns")
canvas.dwg.add(canvas.dwg.text(
    '→', insert=(62, 63),
    fill='black', font_size='10pt', font_family='monospace'
))

canvas.dwg.add(canvas.dwg.text(
    '100-300x faster', insert=(12, 80),
    fill='#4A90E2', font_size='5pt', font_family='monospace', font_weight='bold'
))

# Pattern catalog (center - THE MAIN CONTENT)
canvas.dwg.add(canvas.dwg.text(
    '8 PATTERN GENERATORS', insert=(10, 100),
    fill='black', font_size='8pt', font_family='monospace', font_weight='bold'
))

print("  Generating pattern samples...")

# Grid of pattern samples (2 rows x 4 columns)
pattern_samples = [
    ('DENDRITE', 15, 110, DendritePattern, {}),
    ('SPIRAL', 50, 110, SpiralPattern, {}),
    ('GRID', 85, 110, GridPattern, {}),
    ('NOISE', 120, 110, NoisePattern, {}),
    ('FLOW', 15, 150, FlowFieldPattern, {}),
    ('VORONOI', 50, 150, VoronoiPattern, {}),
    ('L-SYSTEM', 85, 150, LSystemPattern, {}),
    ('TRUCHET', 120, 150, TruchetPattern, {}),
]

for name, x, y, PatternClass, params in pattern_samples:
    # Draw sample area box
    sample_box = Rectangle(x, y, 30, 30)
    canvas.add_polyline(sample_box.get_points(), "structure")

    # Label
    canvas.dwg.add(canvas.dwg.text(
        name, insert=(x + 2, y - 2),
        fill='#666666', font_size='4pt', font_family='monospace'
    ))

    # Generate tiny sample
    try:
        if PatternClass == DendritePattern:
            pattern = DendritePattern(30, 30, num_particles=50, seed_points=[(15, 15)])
            pattern.generate()
        elif PatternClass == SpiralPattern:
            pattern = SpiralPattern(30, 30, center=(15, 15), num_revolutions=4)
            pattern.generate()
        elif PatternClass == GridPattern:
            pattern = GridPattern(30, 30)
            pattern.generate_square_grid(cell_size=5)
        elif PatternClass == NoisePattern:
            pattern = NoisePattern(30, 30, scale=8, octaves=2)
            pattern.generate_contour_lines(num_levels=3, resolution=2.0)
        elif PatternClass == FlowFieldPattern:
            pattern = FlowFieldPattern(30, 30, field_type='noise', scale=10)
            pattern.generate_streamlines(num_lines=8, steps=30, step_size=1)
        elif PatternClass == VoronoiPattern:
            pattern = VoronoiPattern(30, 30, num_sites=15, seed=42)
            pattern.generate()
        elif PatternClass == LSystemPattern:
            pattern = LSystemPattern(30, 30, preset='plant1', start_x=15, start_y=25, start_angle=-90, step_length=2, iterations=3)
            pattern.generate()
        elif PatternClass == TruchetPattern:
            pattern = TruchetPattern(30, 30, grid_size=5, tile_type='arc')
            pattern.generate()

        # Draw pattern offset to sample area
        if hasattr(pattern, 'lines'):
            for line in pattern.lines[:50]:  # Limit for performance
                if len(line) > 1:
                    offset_line = [(px + x, py + y) for px, py in line]
                    canvas.add_polyline(offset_line, "patterns")

        if hasattr(pattern, 'points'):
            for px, py in pattern.points[:100]:  # Limit
                canvas.add_points([(px + x, py + y)], "patterns")

    except Exception as e:
        print(f"    Warning: Could not generate {name}: {e}")
        # Draw X to indicate error
        canvas.add_line((x + 5, y + 5), (x + 25, y + 25), "patterns")
        canvas.add_line((x + 25, y + 5), (x + 5, y + 25), "patterns")

# Use cases (right side)
canvas.dwg.add(canvas.dwg.text(
    'WHAT YOU CAN BUILD', insert=(160, 45),
    fill='black', font_size='8pt', font_family='monospace', font_weight='bold'
))

use_cases = [
    'Portraits (realistic)',
    'Abstract compositions',
    'Landscapes',
    'Organic textures',
    'Geometric patterns',
    'Scientific visualizations',
]

for i, use_case in enumerate(use_cases):
    canvas.dwg.add(canvas.dwg.text(
        f'• {use_case}', insert=(162, 55 + i * 8),
        fill='#333333', font_size='5pt', font_family='monospace'
    ))

# Performance metrics (right bottom)
canvas.dwg.add(canvas.dwg.text(
    'PERFORMANCE', insert=(160, 110),
    fill='black', font_size='8pt', font_family='monospace', font_weight='bold'
))

metrics = [
    ('Dendrite', '920 particles/sec'),
    ('Spiral', '12M points/sec'),
    ('Grid', '8M points/sec'),
    ('Noise', '1.67M segments/sec'),
    ('Flow Field', '12.5M points/sec'),
]

for i, (pattern, speed) in enumerate(metrics):
    canvas.dwg.add(canvas.dwg.text(
        f'{pattern}:', insert=(162, 120 + i * 7),
        fill='#333333', font_size='5pt', font_family='monospace'
    ))
    canvas.dwg.add(canvas.dwg.text(
        speed, insert=(210, 120 + i * 7),
        fill='#4A90E2', font_size='5pt', font_family='monospace', font_weight='bold'
    ))

# Core modules (bottom)
canvas.dwg.add(canvas.dwg.text(
    'CORE MODULES', insert=(160, 160),
    fill='black', font_size='8pt', font_family='monospace', font_weight='bold'
))

modules = [
    'SVGCanvas - Drawing primitives',
    'Composition - Layer system',
    'Shapes - Geometric forms',
    'Patterns - 8 generators',
]

for i, module in enumerate(modules):
    canvas.dwg.add(canvas.dwg.text(
        f'• {module}', insert=(162, 170 + i * 7),
        fill='#333333', font_size='5pt', font_family='monospace'
    ))

# Footer
canvas.dwg.add(canvas.dwg.text(
    'Rust-accelerated • Pen plotter optimized • 1,646 LOC Python + 2,632 LOC Rust',
    insert=(10, 205),
    fill='#999999', font_size='4pt', font_family='monospace'
))

comp.save('axiart_infographic.svg')
print("\n✓ Generated: axiart_infographic.svg")

try:
    import cairosvg
    cairosvg.svg2png(url='axiart_infographic.svg', write_to='axiart_infographic.png', output_width=3000)
    print("✓ Generated: axiart_infographic.png")
except ImportError:
    print("  (Install cairosvg for PNG)")

print("\n" + "="*50)
print("AXIART INFOGRAPHIC")
print("="*50)
print("Shows:")
print("  - Architecture (Python → Rust)")
print("  - 8 pattern generators with visual samples")
print("  - Use cases (what you can build)")
print("  - Performance metrics")
print("  - Core modules")
print("\nActually informative, not abstract circles.")
print("="*50)
