#!/usr/bin/env python3
"""
visualize_v3.py - Next-gen code diagram with rich visual encoding
Uses axiart's full pattern library to show multiple data dimensions
"""

import json
import math
import random
from axiart.composition import Composition
from axiart.shapes import Circle
from axiart.patterns.grid import GridPattern
from axiart.patterns.noise import NoisePattern
from axiart.patterns.flow_field import FlowFieldPattern
from axiart.patterns.voronoi import VoronoiPattern

# Load analysis
with open('analysis.json', 'r') as f:
    data = json.load(f)

# Canvas setup
width, height = 297, 210
comp = Composition(width, height)

# Layers (bottom to top)
comp.add_layer("background", color="#F8F8F8", stroke_width=0.1)
comp.add_layer("complexity_heat", color="#FF9999", stroke_width=0.15)
comp.add_layer("territories", color="#DDDDDD", stroke_width=0.3)
comp.add_layer("flow", color="#BBBBBB", stroke_width=0.12)
comp.add_layer("files", color="black", stroke_width=0.4)
comp.add_layer("api_surface", color="#4A90E2", stroke_width=0.25)
comp.add_layer("hotspots", color="#FF4444", stroke_width=0.5)
comp.add_layer("annotations", color="#333333", stroke_width=0.3)

canvas = comp.get_canvas()

print("Generating next-gen code diagram...")

# 1. Background: Subtle grid
print("  Adding coordinate grid...")
grid = GridPattern(width, height)
grid.generate_square_grid(cell_size=40, jitter=0)
grid.draw(canvas, "background")

# 2. Complexity heat map using noise contours
print("  Generating complexity heat map...")
noise = NoisePattern(width, height, scale=30, octaves=3)
noise.generate_contour_lines(num_levels=3, resolution=3.0)
noise.draw(canvas, "complexity_heat")

# 3. Module territories using Voronoi
print("  Creating module territories...")
voronoi = VoronoiPattern(width, height, num_sites=6, relaxation_iterations=2, seed=42)
voronoi.generate()
voronoi.draw(canvas, "territories")

# 4. Information flow using flow field
print("  Adding information flow...")
flow = FlowFieldPattern(width, height, field_type="radial", scale=40)
flow.generate_streamlines(num_lines=15, steps=80, step_size=2)
flow.draw(canvas, "flow")

# 5. Position files strategically
print("  Positioning files...")

# Manually position key files for clarity
file_positions = {
    # Core infrastructure (left)
    'svg_exporter.py': (50, 80, 'core'),
    'composition.py': (50, 130, 'core'),
    'shapes.py': (50, 180, 'core'),
    '__init__.py': (30, 105, 'core'),

    # Patterns (center-right, arranged in arc)
    'patterns/__init__.py': (120, 105, 'pattern'),
    'dendrite.py': (100, 50, 'pattern'),
    'spiral.py': (140, 40, 'pattern'),
    'grid.py': (170, 50, 'pattern'),
    'flow_field.py': (100, 160, 'pattern'),
    'noise.py': (140, 170, 'pattern'),
    'voronoi.py': (170, 160, 'pattern'),
    'lsystem.py': (200, 105, 'pattern'),
    'truchet.py': (230, 105, 'pattern'),
    'dendrite_rust.py': (85, 100, 'pattern'),
}

# Get file data by name
files_by_name = {f['name']: f for f in data['files']}

# 6. Draw files with multi-dimensional encoding
print("  Drawing files with rich encoding...")

for name, (x, y, category) in file_positions.items():
    if name not in files_by_name:
        continue

    file_data = files_by_name[name]
    loc = file_data['loc']
    complexity = file_data['max_complexity']
    api_surface = file_data['api_surface']

    # Radius based on LOC
    radius = 2 + math.sqrt(loc / 50) * 2.5

    # Determine layer based on complexity
    if complexity > 5:
        layer = "hotspots"
    else:
        layer = "files"

    # Draw main circle
    circle = Circle((x, y), radius)
    canvas.add_polyline(circle.get_points(), layer)

    # Add concentric rings for API surface (public interface size)
    if api_surface > 3:
        rings = min(3, api_surface // 2)
        for i in range(1, rings + 1):
            ring = Circle((x, y), radius + i * 1.0)
            canvas.add_polyline(ring.get_points(), "api_surface")

# 7. Add stippling for high-LOC files
print("  Adding complexity stippling...")
high_loc_files = []
for name, (x, y, cat) in file_positions.items():
    if name in files_by_name:
        high_loc_files.append((name, (x, y, cat), files_by_name[name]))

high_loc_files = sorted(high_loc_files, key=lambda x: x[2]['loc'], reverse=True)[:3]

for name, (x, y, cat), file_data in high_loc_files:
    # Add subtle stippling inside circle
    radius = 2 + math.sqrt(file_data['loc'] / 50) * 2.5
    num_points = min(80, file_data['loc'] // 3)

    stipple_points = []
    for _ in range(num_points):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, radius * 0.7)
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        stipple_points.append((px, py))

    canvas.add_points(stipple_points, "files")

# 8. Annotations
print("  Adding annotations...")

# Key files
key_annotations = [
    ('svg_exporter.py', 50, 80, 'CANVAS'),
    ('composition.py', 50, 130, 'COMPOSER'),
    ('shapes.py', 50, 180, 'SHAPES'),
    ('patterns/__init__.py', 120, 105, 'PATTERNS'),
]

for name, x, y, label in key_annotations:
    if name in files_by_name:
        file_data = files_by_name[name]
        canvas.dwg.add(canvas.dwg.text(
            label,
            insert=(x - 3, y - 10),
            fill='#333333',
            font_size='5pt',
            font_family='monospace',
            font_weight='bold'
        ))

        # Add LOC count
        canvas.dwg.add(canvas.dwg.text(
            f"{file_data['loc']} LOC",
            insert=(x - 3, y + 15),
            fill='#666666',
            font_size='4pt',
            font_family='monospace'
        ))

# Coordinate markers
canvas.dwg.add(canvas.dwg.text(
    '0,0', insert=(10, 10),
    fill='#AAAAAA', font_size='5pt', font_family='monospace'
))

# Legend
legend_y = 25
legend_items = [
    ('Circle size = LOC', 20),
    ('Concentric rings = API surface', 35),
    ('Stippling = Code density', 50),
    ('Red = High complexity', 65),
]

canvas.dwg.add(canvas.dwg.text(
    'ENCODING:', insert=(width - 80, legend_y),
    fill='#333333', font_size='5pt', font_family='monospace', font_weight='bold'
))

for text, offset in legend_items:
    canvas.dwg.add(canvas.dwg.text(
        text, insert=(width - 80, legend_y + offset),
        fill='#666666', font_size='4pt', font_family='monospace'
    ))

# Save
comp.save('code_diagram_v3.svg')
print("\n✓ Generated: code_diagram_v3.svg")

# Export PNG
try:
    import cairosvg
    cairosvg.svg2png(url='code_diagram_v3.svg', write_to='code_diagram_v3.png', output_width=3000)
    print("✓ Generated: code_diagram_v3.png")
except ImportError:
    print("  (Install cairosvg for PNG: pip install cairosvg)")

# Statistics
print("\n" + "="*50)
print("AXIART CODE DIAGRAM v3.0")
print("="*50)
print(f"Files visualized: {len(file_positions)}")
print(f"Total LOC: {data['total_loc']:,}")
print(f"Avg complexity: {data['avg_complexity']:.2f} (very low = well-designed)")
print(f"Max complexity: {data['max_complexity']} (threshold: 10)")

# Find insights
high_api = [f for f in data['files'] if f['api_surface'] > 5]
if high_api:
    print(f"\n🎯 Large API surface ({len(high_api)} files):")
    for f in sorted(high_api, key=lambda x: x['api_surface'], reverse=True)[:3]:
        print(f"  {f['name']}: {f['api_surface']} public exports")

large_files = sorted(data['files'], key=lambda x: x['loc'], reverse=True)[:3]
print(f"\n📊 Largest files:")
for f in large_files:
    print(f"  {f['name']}: {f['loc']} LOC")

print(f"\n🎨 Visualization:")
print(f"  - Noise contours = Complexity heat map")
print(f"  - Voronoi cells = Module territories")
print(f"  - Flow field = Information flow")
print(f"  - Concentric rings = API surface size")
print(f"  - Stippling = Code density")
print("="*50)
