# AxiArt - Generative Art for AxiDraw V3

A modular Python system for creating algorithmic art optimized for the AxiDraw V3 pen plotter. Generate beautiful, plottable SVG artwork with dendrites, spirals, grids, noise fields, and flow patterns.

## Features

- **5 Pattern Generators**: Dendrite/branching, spirals, grids, noise/texture fields, and flow fields
- **SVG Export**: Clean vector output optimized for AxiDraw pen plotting
- **Composable System**: Layer multiple patterns with selective coloring
- **Minimalist Aesthetic**: Clean, professional designs suitable for pen plotting
- **Extensive Examples**: 10 example scripts showing diverse artistic variations

## Installation

```bash
cd axiart
pip install -e .
```

### Dependencies

- numpy >= 1.24.0
- svgwrite >= 1.4.3
- noise >= 1.2.2
- scipy >= 1.10.0

## Quick Start

```python
from axiart import SVGCanvas
from axiart.patterns import SpiralPattern

# Create canvas
canvas = SVGCanvas(width=297, height=210)
canvas.create_layer("main", color="black", stroke_width=0.5)
canvas.set_layer("main")

# Generate spiral
spiral = SpiralPattern(width=297, height=210)
spiral.generate_fermat_spiral(num_points=800, spacing=3.0)
spiral.draw(canvas, "main", as_points=True)

# Save
canvas.save("output.svg")
```

## Pattern Generators

### 1. Dendrite/Branching Patterns

Organic, tree-like or river-like structures using Diffusion-Limited Aggregation (DLA).

```python
from axiart.patterns import DendritePattern

dendrite = DendritePattern(
    width=297,
    height=210,
    num_particles=2000,
    attraction_distance=4.0,
    branching_style="vertical"  # vertical, horizontal, or radial
)
dendrite.generate()
dendrite.draw(canvas, "layer_name")
```

**Parameters:**
- `num_particles`: Number of particles to aggregate
- `attraction_distance`: Distance at which particles stick
- `branching_style`: "radial", "vertical", or "horizontal"
- `seed_points`: Custom starting points for growth

### 2. Spiral Patterns

Concentric circles and spirals with customizable rotation and decay.

```python
from axiart.patterns import SpiralPattern

spiral = SpiralPattern(
    width=297,
    height=210,
    num_revolutions=20,
    spiral_type="archimedean"  # archimedean, logarithmic, or concentric
)

# Archimedean/logarithmic spirals
spiral.generate(start_radius=5, num_spirals=3, angular_offset=2.094)

# Concentric circles
spiral.generate_circular_waves(
    num_circles=20,
    wave_amplitude=2,
    wave_frequency=5
)

# Fermat (parabolic) spiral
spiral.generate_fermat_spiral(num_points=1000, spacing=2.0)

spiral.draw(canvas, "layer_name")
```

### 3. Grid Patterns

Geometric grids (square, hexagonal, triangular) with distortion options.

```python
from axiart.patterns import GridPattern

grid = GridPattern(width=297, height=210, grid_type="hexagonal")

# Hexagonal grid
grid.generate_hexagonal_grid(cell_size=10, fill_cells=True)

# Square grid with jitter
grid.generate_square_grid(cell_size=15, jitter=1.5)

# Triangular grid
grid.generate_triangular_grid(cell_size=10)

# Apply distortion
grid.apply_radial_distortion(strength=0.15)

grid.draw(canvas, "layer_name")
```

### 4. Noise/Texture Fields

Perlin noise-based contours, topographic lines, and stippling.

```python
from axiart.patterns import NoisePattern

noise = NoisePattern(
    width=297,
    height=210,
    scale=100,      # Larger = smoother
    octaves=6,      # Detail level
    seed=42
)

# Topographic contour lines
noise.generate_contour_lines(num_levels=30, resolution=2.0)

# Stippling texture
noise.generate_stippling(num_points=5000, density_map=True, threshold=0.0)

# Cellular texture
noise.generate_cellular_texture(cell_size=5.0, pattern_type="squares")

# Hatching pattern
noise.generate_hatching(line_spacing=2.0, angle=45, density_modulation=True)

noise.draw(canvas, "layer_name")
```

### 5. Flow Field Patterns

Vector field-based particle traces creating organic flowing patterns.

```python
from axiart.patterns import FlowFieldPattern

flow = FlowFieldPattern(
    width=297,
    height=210,
    field_type="noise",  # noise, radial, spiral, waves, or custom
    scale=60,
    seed=42
)

# Generate streamlines
flow.generate_streamlines(num_lines=80, steps=250, step_size=1.2)

# Particle system with trails
flow.generate_particle_system(num_particles=50, steps=300, fade_length=50)

# Grid visualization of vector field
flow.generate_grid_visualization(grid_spacing=10, arrow_length=5)

# Curl noise (divergence-free)
flow.generate_curl_noise_lines(num_lines=100, steps=200)

flow.draw(canvas, "layer_name")
```

## Composition System

Layer multiple patterns with selective coloring:

```python
from axiart.composition import create_standard_composition, ColorPalette

# Create composition with color palette
comp = create_standard_composition(palette=ColorPalette.RED_ACCENT)

# Add patterns to different layers
comp.add_pattern(dendrite_pattern, "primary")
comp.add_pattern(noise_pattern, "accent")

# Save
comp.save("output.svg")
```

### Available Color Palettes

- `ColorPalette.MONO` - Black and white
- `ColorPalette.RED_ACCENT` - Black + red
- `ColorPalette.BLUE_ACCENT` - Black + blue
- `ColorPalette.GOLD_ACCENT` - Black + gold
- `ColorPalette.GREEN_ACCENT` - Black + green
- `ColorPalette.PURPLE_ACCENT` - Black + purple
- `ColorPalette.ORANGE_ACCENT` - Black + orange
- `ColorPalette.DUAL_RED_BLUE` - Black + red + blue
- `ColorPalette.DUAL_GOLD_TEAL` - Black + gold + teal
- `ColorPalette.SEPIA` - Sepia tones

### Custom Composition

```python
from axiart.composition import Composition

comp = Composition(width=297, height=210, background="white")

# Add custom layers
comp.add_layer("background", color="#CCCCCC", stroke_width=0.3)
comp.add_layer("main", color="black", stroke_width=0.5)
comp.add_layer("accent", color="#D32F2F", stroke_width=0.6)

# Add patterns
comp.add_pattern(pattern1, "background")
comp.add_pattern(pattern2, "main")
comp.add_pattern(pattern3, "accent")

comp.save("output.svg")
```

## Examples

The `examples/` directory contains 10 diverse example scripts:

### Individual Patterns

1. **example_simple_starter.py** - Minimal example with Fermat spiral
2. **example_dendrite.py** - Tree-like branching structures
3. **example_spiral.py** - Archimedean spirals and concentric circles
4. **example_grid.py** - Hexagonal and distorted square grids
5. **example_noise.py** - Topographic contours and stippling
6. **example_flow.py** - Flow field streamlines

### Mixed Compositions

7. **example_mixed_organic.py** - Organic theme (dendrites + flow + noise)
8. **example_mixed_geometric.py** - Geometric theme (grids + spirals + flow)
9. **example_mixed_landscape.py** - Landscape theme (contours + trees + sun)
10. **example_showcase.py** - Comprehensive showcase of all patterns

### Running Examples

```bash
cd examples
python example_simple_starter.py
python example_mixed_landscape.py
# etc.
```

All examples generate SVG files in the `examples/` directory with the prefix `output_`.

## AxiDraw Compatibility

All generated SVGs are optimized for AxiDraw V3:

- **Units**: Default to mm (A4 size: 297×210mm)
- **Clean vectors**: No bitmap data, only lines and curves
- **Stroke-based**: All paths use strokes, not fills (except stippling)
- **Layer organization**: Multiple layers for pen changes
- **Optimal stroke width**: Default 0.5mm suitable for most pens

### Plotting Tips

1. **Import to Inkscape** for final adjustments
2. **Use AxiDraw extension** to preview pen paths
3. **Layer order**: Background layers plot first
4. **Pen changes**: Use layers for different colored pens
5. **Test plots**: Start with simple examples before complex compositions

## Advanced Usage

### Custom Vector Fields

```python
flow = FlowFieldPattern(width=297, height=210, field_type="custom")

# Define custom field function
def my_field(x, y):
    dx = np.sin(y / 20)
    dy = np.cos(x / 20)
    return dx, dy

flow.set_custom_field(my_field)
flow.generate_streamlines(num_lines=50, steps=200)
```

### Custom Grid Distortions

```python
grid = GridPattern(width=297, height=210)
grid.generate_square_grid(cell_size=10)

# Define custom distortion
def wave_distortion(x, y):
    new_x = x + 5 * np.sin(y / 20)
    new_y = y + 5 * np.cos(x / 20)
    return new_x, new_y

grid.apply_distortion(wave_distortion)
```

### Accessing Raw Data

All patterns provide methods to access generated data:

```python
# Get dendrite points and lines
points = dendrite.get_points()
lines = dendrite.get_lines()

# Get spiral paths
spirals = spiral.get_spirals()

# Get grid elements
grid_lines = grid.get_lines()
grid_cells = grid.get_cells()

# Get noise contours
contours = noise.get_contours()
stipple_points = noise.get_points()

# Get flow field paths
flow_paths = flow.get_paths()
```

## Canvas Dimensions

Common AxiDraw plotting sizes (in mm):

- **A4**: 297 × 210 (default)
- **A3**: 420 × 297
- **Letter**: 279.4 × 215.9
- **Custom**: Any size supported by your AxiDraw model

```python
# A3 canvas
canvas = SVGCanvas(width=420, height=297)
```

## Performance Tips

- **Dendrites**: Reduce `num_particles` for faster generation
- **Flow fields**: Reduce `num_lines` and `steps` for simpler patterns
- **Noise contours**: Increase `resolution` to reduce detail
- **Stippling**: Fewer points = faster generation

## Project Structure

```
axiart/
├── pyproject.toml          # Project dependencies
├── README.md               # This file
├── axiart/
│   ├── __init__.py
│   ├── svg_exporter.py     # SVG canvas and export
│   ├── composition.py      # Layer composition system
│   └── patterns/
│       ├── __init__.py
│       ├── dendrite.py     # DLA branching patterns
│       ├── spiral.py       # Spiral generators
│       ├── grid.py         # Grid patterns
│       ├── noise.py        # Perlin noise patterns
│       └── flow_field.py   # Vector field patterns
└── examples/               # 10 example scripts
    ├── example_simple_starter.py
    ├── example_dendrite.py
    ├── example_spiral.py
    ├── example_grid.py
    ├── example_noise.py
    ├── example_flow.py
    ├── example_mixed_organic.py
    ├── example_mixed_geometric.py
    ├── example_mixed_landscape.py
    └── example_showcase.py
```

## License

This project is open source. Feel free to use, modify, and distribute.

## Credits

Inspired by the generative art community and optimized for AxiDraw V3 pen plotters by Evil Mad Scientist Laboratories.

## Contributing

Contributions welcome! Some ideas for extensions:

- Additional pattern generators (Voronoi, reaction-diffusion, L-systems)
- More color palettes
- Animation/sequence generation
- Integration with plotting libraries
- Performance optimizations

---

Happy plotting! 🎨🖊️
