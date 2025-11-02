# AxiArt - Generative Art for AxiDraw V3

A high-performance Python/Rust system for creating algorithmic art optimized for the AxiDraw V3 pen plotter. Generate plottable SVG artwork with dendrites, spirals, grids, noise fields, and flow patterns.

**Performance**: Pattern generation accelerated 10-300x using Rust implementations with zero capacity limits.

## Features

- **6 Rust-accelerated pattern generators**: Dendrites, spirals, grids, noise fields, flow fields, and Perlin noise
- **High performance**: 8-20M points/sec generation speed depending on pattern type
- **SVG export**: Clean vector output optimized for AxiDraw pen plotting
- **Composable system**: Layer multiple patterns with selective coloring
- **Production-ready**: Tested with 10,000+ particles, extreme configurations

## Performance Benchmarks

| Pattern | Performance | Speedup vs Python |
|---------|-------------|-------------------|
| DendritePattern | 920 particles/sec (10K particles) | 100-300x |
| FlowFieldPattern | 12.5M points/sec | 5-20x |
| NoisePattern | 12M points/sec (stippling) | 5-15x |
| SpiralPattern | 12-20M points/sec | 2-5x |
| GridPattern | 8-12M points/sec | 2-4x |

See `RUST_PERFORMANCE.md` for detailed benchmarks and architecture.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and Rust bindings via Maturin.

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install dependencies
cd axiart
uv sync

# Build Rust acceleration library (required)
uv run maturin develop --release
```

### Dependencies

**Runtime**:
- Python >= 3.9
- svgwrite >= 1.4.3

**Build**:
- Rust toolchain (automatically installed by Maturin)
- Maturin >= 1.7

**Note**: `numpy`, `noise`, and `scipy` are no longer required for pattern generation (handled by Rust).

## Quick Start

```python
from axiart import SVGCanvas
from axiart.patterns import SpiralPattern

# Create canvas (A4 dimensions in mm)
canvas = SVGCanvas(width=297, height=210)
canvas.create_layer("main", color="black", stroke_width=0.5)
canvas.set_layer("main")

# Generate spiral (Rust-accelerated)
spiral = SpiralPattern(width=297, height=210, num_revolutions=20)
spiral.generate(start_radius=5, num_spirals=3)
spiral.draw(canvas, "main")

# Save
canvas.save("output.svg")
```

## Pattern Generators

All pattern classes are thin Python wrappers around Rust implementations. They maintain the same API but execute at Rust speed.

### 1. DendritePattern

Organic branching structures using Diffusion-Limited Aggregation (DLA).

```python
from axiart.patterns import DendritePattern

dendrite = DendritePattern(
    width=297,
    height=210,
    num_particles=5000,
    attraction_distance=5.0,
    branching_style="radial"  # radial, vertical, horizontal
)
dendrite.generate(max_attempts=1000)
dendrite.draw(canvas, "layer_name")
```

**Performance**: 920 particles/sec (10,000 particles). Handles unlimited particles with O(1) spatial grid hash.

### 2. SpiralPattern

Archimedean, logarithmic, and concentric spirals.

```python
from axiart.patterns import SpiralPattern

spiral = SpiralPattern(
    width=297,
    height=210,
    num_revolutions=20,
    spiral_type="archimedean"  # archimedean, logarithmic, concentric
)

# Generate spirals
spiral.generate(start_radius=5, num_spirals=3, angular_offset=2.094)

# Circular waves
spiral.generate_circular_waves(
    num_circles=30,
    wave_amplitude=5.0,
    wave_frequency=10.0
)

spiral.draw(canvas, "layer_name")
```

**Performance**: 12-20M points/sec.

### 3. GridPattern

Square and hexagonal grids with radial distortion.

```python
from axiart.patterns import GridPattern

grid = GridPattern(width=297, height=210)

# Square grid with optional jitter
grid.generate_square_grid(cell_size=10, jitter=0.5)

# Hexagonal grid
grid.generate_hexagonal_grid(cell_size=10)

# Apply radial distortion
grid.apply_radial_distortion(center=None, strength=0.5)

grid.draw(canvas, "layer_name")
```

**Performance**: 8-12M points/sec. Supports 2.2M hexagons/sec generation.

### 4. NoisePattern

Perlin noise-based contours, stippling, and textures using marching squares.

```python
from axiart.patterns import NoisePattern

noise = NoisePattern(
    width=297,
    height=210,
    scale=100.0,      # Larger = smoother
    octaves=4,        # Detail layers
    seed=42
)

# Topographic contour lines (marching squares)
noise.generate_contour_lines(num_levels=30, resolution=2.0)

# Parallel stippling
noise.generate_stippling(num_points=20000, density_map=True, parallel=True)

# Cellular texture
noise.generate_cellular_texture(cell_size=5.0, pattern_type="squares")

# Hatching
noise.generate_hatching(spacing=5.0, line_length=10.0, threshold=0.0)

noise.draw(canvas, "layer_name")
```

**Performance**: 12M points/sec (stippling), 1.67M segments/sec (contours). Parallel generation enabled by default.

### 5. FlowFieldPattern

Vector field particle tracing with parallel streamline generation.

```python
from axiart.patterns import FlowFieldPattern

flow = FlowFieldPattern(
    width=297,
    height=210,
    field_type="noise",  # noise, radial, spiral, waves
    scale=50.0,
    seed=42
)

# Parallel streamlines (1.8x speedup on multi-core)
flow.generate_streamlines(num_lines=100, steps=200, parallel=True)

# Curl noise (divergence-free)
flow.generate_curl_noise_lines(num_lines=100, steps=200, parallel=True)

# Grid visualization
flow.generate_grid_visualization(grid_resolution=20)

flow.draw(canvas, "layer_name")
```

**Performance**: 12.5M points/sec with parallel generation.

## Composition System

Layer multiple patterns with selective coloring:

```python
from axiart.composition import create_standard_composition, ColorPalette

# Create composition with predefined palette
comp = create_standard_composition(palette=ColorPalette.RED_ACCENT)

# Add patterns to layers
comp.add_pattern(dendrite_pattern, "primary")
comp.add_pattern(noise_pattern, "accent")

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

comp.add_layer("background", color="#CCCCCC", stroke_width=0.3)
comp.add_layer("main", color="black", stroke_width=0.5)
comp.add_layer("accent", color="#D32F2F", stroke_width=0.6)

comp.add_pattern(pattern1, "background")
comp.add_pattern(pattern2, "main")
comp.add_pattern(pattern3, "accent")

comp.save("output.svg")
```

## Examples

The `examples/` directory contains example scripts demonstrating individual patterns and complex compositions.

### Running Examples

```bash
cd examples
uv run python example_simple_starter.py
uv run python example_abstract_character.py
uv run python example_mixed_landscape.py
```

All examples generate SVG files in the `examples/` directory.

### Hyperrealistic Portraits

AxiArt can create highly detailed algorithmic portraits using maximum-density techniques:

```bash
cd examples
uv run python example_portrait_trevor_detailed.py
```

**Techniques used:**
- **58,000 stipple points** for smooth skin gradients (3-layer progressive shading)
- **5,800 dendrite particles** for realistic hair and beard texture
- **45 contour levels** for facial structure and depth
- **Multi-directional cross-hatching** for fabric volume
- **Fine stroke widths** (0.12-0.42mm) for detail precision

**Detail density:**
- Beard: 2,000 dendrite particles with dual-layer branching
- Hair: 2,400 particles across left/right clusters
- Skin: 50,000 points across 3 stippling layers (light/mid/shadow)
- Eyes: Detailed structures with eyelids and reflections
- Glasses: Geometric frames with highlights

This demonstrates the system's capability for **maximum realism within line-based pen plotting constraints**. The portrait combines:
- Filled geometric shapes (face, glasses, clothing)
- Organic dendrite textures (hair, beard)
- Noise-based gradients (skin shading)
- Anatomically accurate feature placement

**Note**: This is algorithmic realism optimized for pen plotting, not photographic rendering. All detail is created through line density, stippling, and branching patterns.

## AxiDraw Compatibility

All generated SVGs are optimized for AxiDraw V3:

- **Units**: millimeters (default A4: 297x210mm)
- **Clean vectors**: Lines and curves only, no bitmap data
- **Stroke-based**: All paths use strokes (except stippling points)
- **Layer organization**: Multiple layers for pen changes
- **Default stroke width**: 0.5mm

### Common Canvas Sizes

```python
# A4 (default)
canvas = SVGCanvas(width=297, height=210)

# A3
canvas = SVGCanvas(width=420, height=297)

# Letter
canvas = SVGCanvas(width=279.4, height=215.9)
```

## Accessing Raw Data

All patterns provide methods to access generated geometry:

```python
# Dendrite
points = dendrite.get_points()
lines = dendrite.get_lines()

# Spiral
spirals = spiral.get_spirals()

# Grid
grid_lines = grid.get_lines()

# Noise
contour_lines = noise.get_lines()
stipple_points = noise.get_points()

# Flow field
flow_paths = flow.get_paths()
```

## Rust Acceleration Architecture

AxiArt uses Rust for all computationally expensive pattern generation:

- **Custom spatial grid hash** for O(1) nearest neighbor queries (dendrites)
- **Parallel streamline generation** using rayon (flow fields)
- **Marching squares** for contour extraction (noise patterns)
- **SIMD-optimized geometry** for grid and spiral generation
- **Zero-copy NumPy integration** via PyO3

Python pattern classes are thin wrappers that:
1. Initialize Rust generators
2. Pass parameters to Rust
3. Receive computed geometry
4. Provide drawing methods

If Rust library is not built, initialization will fail with clear instructions.

See `RUST_PERFORMANCE.md` for comprehensive benchmarks, API reference, and architecture details.

## Performance Considerations

Pattern generation is extremely fast due to Rust acceleration:

- **DendritePattern**: 10,000 particles in ~11 seconds
- **FlowFieldPattern**: 1,000 streamlines (200 steps each) in ~0.016 seconds
- **NoisePattern**: 50,000 stipple points in ~0.004 seconds
- **GridPattern**: 3,000 hexagons in ~0.0014 seconds
- **SpiralPattern**: 500,000 points in ~0.04 seconds

All patterns support unlimited complexity with no capacity limits.

## Project Structure

```
axiart/
├── pyproject.toml           # Project configuration
├── README.md                # This file
├── RUST_PERFORMANCE.md      # Detailed benchmarks and architecture
├── CLAUDE.md                # Development guidance
├── axiart/
│   ├── __init__.py
│   ├── svg_exporter.py      # SVG canvas and export
│   ├── composition.py       # Layer composition system
│   ├── shapes.py            # Geometric primitives
│   └── patterns/            # Pattern generators (Python wrappers)
│       ├── __init__.py
│       ├── dendrite.py      # DLA branching (Rust)
│       ├── spiral.py        # Spirals (Rust)
│       ├── grid.py          # Grids (Rust)
│       ├── noise.py         # Noise patterns (Rust)
│       └── flow_field.py    # Flow fields (Rust)
├── axiart-core/             # Rust acceleration library
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs           # PyO3 module definition
│       ├── dendrite.rs      # Spatial grid hash DLA (328 lines)
│       ├── noise_core.rs    # Perlin noise with fBm (140 lines)
│       ├── flow_field.rs    # Parallel streamlines (357 lines)
│       ├── noise_pattern.rs # Marching squares (357 lines)
│       ├── spiral.rs        # Geometric spirals (194 lines)
│       └── grid.rs          # Grid generation (153 lines)
├── examples/                # Example scripts
└── test_*.py                # Benchmark scripts
```

## Development

```bash
# Build Rust library in development mode
uv run maturin develop

# Build optimized release version
uv run maturin develop --release

# Format Python code
uv run black axiart/

# Run benchmarks
uv run python test_final_dendrite.py
uv run python test_flowfield.py
uv run python test_noisepattern.py
uv run python test_spiral.py
uv run python test_grid.py
```

## License

Open source. Free to use, modify, and distribute.

## Credits

Optimized for AxiDraw V3 pen plotters by Evil Mad Scientist Laboratories.
