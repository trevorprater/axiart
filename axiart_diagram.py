#!/usr/bin/env python3
"""
Custom diagram for axiart codebase
Generated: 2025-11-06
Strategy: Dual-zone layout (Python ↔ Rust architecture)

Visualization reveals:
- Two-layer architecture (Python wrappers, Rust acceleration)
- SVGCanvas as central hub (all patterns depend on it)
- 8 pattern modules with corresponding Rust implementations
- Size indicates complexity (radius ∝ √LOC)
"""

from axiart.composition import Composition
from axiart.shapes import Circle, Rectangle
from axiart.patterns.grid import GridPattern

# Canvas setup (A4 landscape)
width, height = 297, 210
comp = Composition(width, height)

# Define layers (bottom to top)
comp.add_layer("grid", color="#DDDDDD", stroke_width=0.1)
comp.add_layer("zones", color="#F5F5F5", stroke_width=0.3)
comp.add_layer("dependencies", color="#AAAAAA", stroke_width=0.2)
comp.add_layer("files", color="black", stroke_width=0.4)
comp.add_layer("accent", color="black", stroke_width=0.2)
comp.add_layer("highlights", color="#4A90E2", stroke_width=0.5)
comp.add_layer("annotations", color="#333333", stroke_width=0.3)

canvas = comp.get_canvas()

# 1. Add sparse grid
grid = GridPattern(width, height)
grid.generate_square_grid(cell_size=30)
grid.draw(canvas, "grid")

# 2. Add zone boundaries
# Python zone (left half)
python_zone = Rectangle(15, 15, 125, 180)
canvas.add_polyline(python_zone.get_points(), "zones")

# Rust zone (right half)
rust_zone = Rectangle(157, 15, 125, 180)
canvas.add_polyline(rust_zone.get_points(), "zones")

# 3. Define file positions and metadata
# Python files (left zone, positioned manually for clarity)
python_files = {
    # Core infrastructure (central column)
    'svg_exporter.py': {'x': 77, 'y': 105, 'loc': 266, 'is_hub': True},
    'composition.py': {'x': 77, 'y': 55, 'loc': 210, 'is_hub': False},
    'shapes.py': {'x': 77, 'y': 155, 'loc': 289, 'is_hub': False},

    # Pattern wrappers (arc around svg_exporter)
    'patterns/dendrite.py': {'x': 35, 'y': 70, 'loc': 101, 'is_hub': False, 'rust': 'dendrite.rs'},
    'patterns/spiral.py': {'x': 35, 'y': 105, 'loc': 165, 'is_hub': False, 'rust': 'spiral.rs'},
    'patterns/grid.py': {'x': 35, 'y': 140, 'loc': 120, 'is_hub': False, 'rust': 'grid.rs'},
    'patterns/flow_field.py': {'x': 119, 'y': 70, 'loc': 140, 'is_hub': False, 'rust': 'flow_field.rs'},
    'patterns/noise.py': {'x': 119, 'y': 105, 'loc': 185, 'is_hub': False, 'rust': 'noise_pattern.rs'},
    'patterns/voronoi.py': {'x': 119, 'y': 140, 'loc': 104, 'is_hub': False, 'rust': 'voronoi.rs'},
    'patterns/lsystem.py': {'x': 77, 'y': 175, 'loc': 166, 'is_hub': False, 'rust': 'lsystem.rs'},
    'patterns/truchet.py': {'x': 35, 'y': 175, 'loc': 110, 'is_hub': False, 'rust': 'truchet.rs'},
}

# Rust files (right zone, positioned to mirror Python patterns)
rust_files = {
    # PyO3 bindings (central)
    'lib.rs': {'x': 220, 'y': 105, 'loc': 44, 'is_hub': True},

    # Pattern implementations (mirroring Python layout)
    'dendrite.rs': {'x': 178, 'y': 70, 'loc': 337, 'is_hub': False},
    'spiral.rs': {'x': 178, 'y': 105, 'loc': 237, 'is_hub': False},
    'grid.rs': {'x': 178, 'y': 140, 'loc': 148, 'is_hub': False},
    'flow_field.rs': {'x': 262, 'y': 70, 'loc': 356, 'is_hub': False},
    'noise_pattern.rs': {'x': 262, 'y': 105, 'loc': 356, 'is_hub': False},
    'noise_core.rs': {'x': 262, 'y': 140, 'loc': 140, 'is_hub': False},
    'voronoi.rs': {'x': 220, 'y': 140, 'loc': 273, 'is_hub': False},
    'lsystem.rs': {'x': 220, 'y': 35, 'loc': 410, 'is_hub': False},
    'truchet.rs': {'x': 178, 'y': 35, 'loc': 334, 'is_hub': False},
}

# 4. Draw Python→Rust connections (pattern wrappers to implementations)
pattern_links = [
    ('patterns/dendrite.py', 'dendrite.rs'),
    ('patterns/spiral.py', 'spiral.rs'),
    ('patterns/grid.py', 'grid.rs'),
    ('patterns/flow_field.py', 'flow_field.rs'),
    ('patterns/noise.py', 'noise_pattern.rs'),
    ('patterns/voronoi.py', 'voronoi.rs'),
    ('patterns/lsystem.py', 'lsystem.rs'),
    ('patterns/truchet.py', 'truchet.rs'),
]

for py_file, rs_file in pattern_links:
    py_data = python_files[py_file]
    rs_data = rust_files[rs_file]
    canvas.add_line((py_data['x'], py_data['y']), (rs_data['x'], rs_data['y']), "dependencies")

# 5. Draw Python file circles
for filename, data in python_files.items():
    x, y, loc = data['x'], data['y'], data['loc']
    radius = 2 + (loc / 100) ** 0.5 * 2.5

    layer = "highlights" if data['is_hub'] else "files"
    circle = Circle((x, y), radius)
    canvas.add_polyline(circle.get_points(), layer)

# 6. Draw Rust file circles
for filename, data in rust_files.items():
    x, y, loc = data['x'], data['y'], data['loc']
    radius = 2 + (loc / 100) ** 0.5 * 2.5

    layer = "highlights" if data['is_hub'] else "files"
    circle = Circle((x, y), radius)
    canvas.add_polyline(circle.get_points(), layer)

# 7. Add subtle concentric accent on 3 largest Rust files
large_rust = [
    ('lsystem.rs', 410),
    ('flow_field.rs', 356),
    ('noise_pattern.rs', 356),
]

for filename, loc in large_rust:
    data = rust_files[filename]
    x, y = data['x'], data['y']
    base_radius = 2 + (loc / 100) ** 0.5 * 2.5

    for i in range(1, 4):
        r = base_radius + i * 1.2
        circle = Circle((x, y), r)
        canvas.add_polyline(circle.get_points(), "accent")

# 8. Add annotations (key files only)
annotations = [
    # Python
    (77, 105, 'svg_exporter.py', 'annotations'),
    (77, 55, 'composition.py', 'annotations'),
    (77, 155, 'shapes.py', 'annotations'),

    # Rust
    (220, 105, 'lib.rs', 'annotations'),
    (220, 35, 'lsystem.rs', 'annotations'),
    (262, 70, 'flow_field.rs', 'annotations'),

    # Zone labels
    (77, 25, 'PYTHON', 'annotations'),
    (220, 25, 'RUST', 'annotations'),
]

for x, y, label, layer in annotations:
    canvas.dwg.add(canvas.dwg.text(
        label, insert=(x - len(label) * 1.5, y - 8),
        fill='#333333',
        font_size='6pt',
        font_family='monospace',
        font_weight='bold' if label in ['PYTHON', 'RUST'] else 'normal'
    ))

# Coordinate markers
canvas.dwg.add(canvas.dwg.text('0,0', insert=(15, 15), fill='#999999', font_size='5pt', font_family='monospace'))
canvas.dwg.add(canvas.dwg.text(f'{width-15},0', insert=(width-30, 15), fill='#999999', font_size='5pt', font_family='monospace'))

# Save
comp.save('axiart_diagram.svg')
print("✓ Generated: axiart_diagram.svg")

# Export PNG
try:
    import cairosvg
    cairosvg.svg2png(url='axiart_diagram.svg', write_to='axiart_diagram.png', output_width=3000)
    print("✓ Generated: axiart_diagram.png")
except ImportError:
    print("  (Install cairosvg for PNG export: pip install cairosvg)")

# Print summary
print("\n" + "="*50)
print("AXIART CODEBASE DIAGRAM")
print("="*50)
print("Architecture: Two-layer (Python wrappers → Rust core)")
print("Python files: 14 (~2,000 LOC)")
print("Rust files: 10 (~2,600 LOC)")
print("Core hub: svg_exporter.py (all patterns depend on it)")
print("Pattern pairs: 8 Python wrappers → 8 Rust implementations")
print("\nMarks: ~70 (circles + lines + accents + grid)")
print("Negative space: ~55%")
print("="*50)
