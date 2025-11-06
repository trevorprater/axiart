# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AxiArt is a generative art system for creating algorithmic artwork optimized for pen plotters. It uses a modular, layer-based composition system where patterns are generated algorithmically and then combined on an SVG canvas.

## Development Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and requires building Rust acceleration libraries.

### Installation
```bash
uv sync                              # Install Python dependencies
uv run maturin develop --release     # Build Rust acceleration library (REQUIRED)
```

**CRITICAL**: The Rust library (`axiart_core`) must be built before running any examples. All pattern generators are pure Rust wrappers - they will fail with clear error messages if the Rust library is not built.

### Building Rust Library
```bash
uv run maturin develop               # Development build (faster compile)
uv run maturin develop --release     # Release build (optimized, use for benchmarks)
```

After modifying Rust code in `axiart-core/src/`, rebuild with the appropriate command.

### Running Examples
```bash
cd examples
uv run python example_simple_starter.py      # Basic spiral example
uv run python example_abstract_character.py  # Complex artistic composition
uv run python example_mixed_landscape.py     # Multi-pattern landscape
uv run python example_portrait_trevor_detailed.py  # Hyperrealistic portrait (58k stipple points)
uv run python example_voronoi.py             # Voronoi diagrams (cellular patterns)
uv run python example_lsystem.py             # L-Systems (fractals and plants)
uv run python example_truchet.py             # Truchet tiles (geometric patterns)
```

### Running Benchmarks
```bash
uv run python test_dendrite.py       # Benchmark dendrite DLA (10k particles)
uv run python test_spiral.py         # Benchmark spiral generation
uv run python test_grid.py           # Benchmark grid patterns
uv run python test_flowfield.py      # Benchmark flow fields
uv run python test_noisepattern.py   # Benchmark noise patterns
uv run python test_voronoi.py        # Benchmark Voronoi diagrams
uv run python test_lsystem.py        # Benchmark L-Systems
uv run python test_truchet.py        # Benchmark Truchet tiles
```

### Code Formatting
```bash
uv run black axiart/                 # Format Python code (line-length: 100)
cargo fmt --manifest-path axiart-core/Cargo.toml  # Format Rust code
```

## Architecture

### Core Components

**SVGCanvas** (`axiart/svg_exporter.py`)
- Low-level SVG canvas with layer management
- Handles drawing primitives: lines, polylines, points, curves
- Each layer has independent color, stroke width, and styling
- Direct access to underlying `svgwrite.Drawing` via `.dwg` attribute

**Composition** (`axiart/composition.py`)
- High-level composition system that wraps SVGCanvas
- Manages multiple named layers with opacity and blend effects
- Patterns are added to specific layers via `comp.add_pattern(pattern, "layer_name")`
- Access underlying canvas with `comp.get_canvas()` for direct drawing

**Pattern Generators** (`axiart/patterns/`) - **Pure Rust Wrappers**
- **CRITICAL**: All pattern generators are thin Python wrappers around Rust implementations
- **No fallback**: If Rust library is not built, imports will fail with helpful error messages
- **Zero Python implementation**: All computation happens in Rust for 10-300x speedup
- Each pattern class follows the same interface:
  1. Initialize with canvas dimensions and parameters (creates Rust generator)
  2. Call a `generate_*()` method to compute the pattern (delegates to Rust)
  3. Call `.draw(canvas, layer_name)` to render to canvas
  4. Optionally call `.get_points()`, `.get_lines()`, etc. for raw data
- Patterns store computed geometry internally and can be drawn multiple times
- See `RUST_PERFORMANCE.md` for detailed performance characteristics

**Shapes System** (`axiart/shapes.py`)
- Basic geometric shapes: `Circle`, `Rectangle`, `Polygon`
- `add_filled_shape()` helper for creating filled shapes with strokes
- Shapes can be filled with color (critical for artistic compositions)

### Pattern Types (All Rust-Accelerated)

1. **DendritePattern** - Organic branching structures using Diffusion-Limited Aggregation (DLA)
   - **Performance**: 920 particles/sec (10,000 particles in 10.8s)
   - **Implementation**: Custom spatial grid hash for O(1) nearest neighbor lookup
   - Branching styles: `"radial"`, `"vertical"`, `"horizontal"`
   - Controlled by `num_particles`, `attraction_distance`, `seed_points`
   - No capacity limits - tested with 10,000+ particles
   - Use for: hair, beards, trees, organic textures

2. **SpiralPattern** - Spirals and concentric circles
   - **Performance**: 12-20M points/sec
   - Types: Archimedean, logarithmic, Fermat (parabolic), circular waves
   - Methods: `generate()`, `generate_fermat_spiral()`, `generate_circular_waves()`
   - Use for: focal points, phyllotaxis patterns, ripples

3. **GridPattern** - Geometric grids with optional distortion
   - **Performance**: 8-12M points/sec, 2.2M hexagons/sec
   - Grid types: square, hexagonal
   - Apply distortions: `apply_radial_distortion()`, `apply_jitter()`
   - Custom distortions: Get data with `.get_lines()`, transform in Python, draw manually
   - Use for: backgrounds, structure, computational substrates

4. **NoisePattern** - Perlin noise-based textures using marching squares
   - **Performance**: 12M points/sec (stippling), 1.67M segments/sec (contours)
   - Outputs: contour lines, stippling, cellular texture, hatching
   - Controlled by `scale` (smoothness) and `octaves` (detail)
   - Parallel generation enabled by default
   - Use for: shading, skin texture, organic backgrounds, topographic effects

5. **FlowFieldPattern** - Vector field particle tracing with parallel generation
   - **Performance**: 12.5M points/sec with parallel streamlines
   - Field types: `"noise"`, `"radial"`, `"spiral"`, `"waves"`
   - Outputs: streamlines, curl noise (divergence-free), grid visualization
   - Parallel generation: 1.8x speedup on multi-core systems
   - Use for: movement, energy flows, atmospheric effects

6. **VoronoiPattern** - Cellular patterns using Voronoi diagrams
   - **Performance**: High-performance sampling-based edge detection
   - Supports Lloyd's relaxation for uniform cell distribution
   - Parameters: `num_sites`, `relaxation_iterations`, `sampling_resolution`
   - Outputs: sites (cell centers) and edges (cell boundaries)
   - Use for: organic textures, stained glass effects, cellular patterns, natural divisions

7. **LSystemPattern** - Fractal patterns using Lindenmayer systems
   - **Performance**: High-speed string expansion and turtle graphics interpretation
   - Presets: Koch curve, Sierpinski triangle, Dragon curve, Hilbert curve, plant variants
   - Custom rules: Define your own axiom and replacement rules
   - Turtle commands: F/G (forward), +/- (turn), [ ] (push/pop state)
   - Use for: plants, trees, fractals, organic growth, space-filling curves

8. **TruchetPattern** - Geometric tiling patterns with rotated tiles
   - **Performance**: High-speed tile generation with flexible patterns
   - Tile types: `"diagonal"`, `"arc"`, `"double_arc"`, `"triangle"`, `"maze"`
   - Parameters: `grid_size`, `randomness` (0.0=structured, 1.0=random), `arc_segments`
   - Outputs: lines (for diagonal/triangle/maze) or curves (for arc-based tiles)
   - Use for: geometric backgrounds, maze-like patterns, flowing curves, structured chaos

### Workflow: From Patterns to Art

The system is designed around **intentional artistic composition**, not just pattern demonstration:

1. **Create Composition with Layers** - Define layer hierarchy (back to front)
2. **Add Filled Shapes** - Use `shapes.py` to create colored geometric forms (faces, bodies, etc.)
3. **Layer Patterns with Purpose** - Each pattern serves a compositional role:
   - Grids → background structure
   - Voronoi → cellular textures, natural divisions
   - Spirals → focal points (eyes, centers)
   - Flow fields → texture and movement
   - Dendrites → organic growth (hair, trees)
   - L-Systems → plants, fractals, branching structures
   - Truchet → geometric backgrounds, emergent patterns
   - Noise → shading and depth
4. **Strategic Color Use** - Mostly black + 1-2 accent colors
5. **Constrain Patterns to Regions** - Filter pattern outputs to specific areas

See `ARTISTIC_GUIDE.md` for detailed artistic techniques.

### Layer System

Layers are drawn in creation order (first created = bottom layer). Typical layer setup:

```python
comp.add_layer("fills", color="none")           # Filled shapes (bottom)
comp.add_layer("background", color="#CCC")      # Subtle grid
comp.add_layer("primary", color="black")        # Main linework
comp.add_layer("accent1", color="#FF6B6B")      # Color highlights
comp.add_layer("details", color="black")        # Top layer
```

## Important Implementation Details

### Pattern Generation Flow
1. Pattern objects store canvas dimensions on initialization
2. `generate_*()` methods compute geometry and store in internal attributes (`self.lines`, `self.points`, etc.)
3. `.draw(canvas, layer_name)` renders stored geometry to the specified layer
4. Patterns can be drawn multiple times or raw data accessed via `.get_*()` methods

### Canvas Coordinates
- Default: A4 paper in mm (297×210)
- Origin: Top-left (0, 0)
- All dimensions in millimeters by default
- Pen plotter compatible: max plotting area depends on specific hardware

### Direct SVG Manipulation
For advanced use, access the underlying `svgwrite.Drawing` object:
```python
canvas.dwg.add(canvas.dwg.rect(...))  # Direct svgwrite calls
```

### Color Palettes
Predefined palettes in `composition.py`:
- `ColorPalette.MONO`, `RED_ACCENT`, `BLUE_ACCENT`, `GOLD_ACCENT`, etc.
- Use with `create_standard_composition(palette=ColorPalette.RED_ACCENT)`

### Example Categories

**Simple Pattern Demonstrations**:
- `example_dendrite.py`, `example_spiral.py`, `example_grid.py`, etc.
- `example_voronoi.py`, `example_lsystem.py`, `example_truchet.py`
- Each demonstrates a single pattern type with basic parameters

**Artistic Compositions**:
- `example_abstract_character.py` - Combining filled shapes with patterns (faces, eyes)
- `example_mixed_landscape.py` - Multi-pattern landscape composition
- Demonstrate proper layer usage, filled shapes, and pattern constraining

**Self-Portraits** (Algorithmic/Abstract):
- `example_self_portrait_claude.py` - Neural Landscape (dual-hemisphere, 11 layers)
- `example_self_portrait_mandala.py` - 8-fold radial symmetry with rotational duplication
- `example_self_portrait_flow.py` - Vertical flowing process (no spirals)
- Demonstrate region-constrained patterns, rotational transforms, custom filtering

**Human Portraits** (Hyperrealistic):
- `example_portrait_trevor.py` - Basic algorithmic portrait (3k stipple points)
- `example_portrait_trevor_detailed.py` - Maximum detail (58k stipple, 5.8k dendrites)
- Demonstrate filled shapes + organic textures, multi-layer stippling, anatomical positioning

**Advanced Techniques**:
- `example_warped_space.py` - Gravitational lens with multiple distortion strengths
- Demonstrates distortion techniques and visual effects

## File Organization

```
axiart/
├── axiart/                  # Main Python package
│   ├── svg_exporter.py      # SVGCanvas - low-level canvas
│   ├── composition.py       # Composition - high-level layer system
│   ├── shapes.py            # Geometric shapes with fills
│   └── patterns/            # Pattern generators (Python wrappers)
│       ├── dendrite.py      # DLA branching (Rust wrapper)
│       ├── spiral.py        # Spirals and circles (Rust wrapper)
│       ├── grid.py          # Geometric grids (Rust wrapper)
│       ├── noise.py         # Perlin noise patterns (Rust wrapper)
│       ├── flow_field.py    # Vector field patterns (Rust wrapper)
│       ├── voronoi.py       # Voronoi diagrams (Rust wrapper)
│       ├── lsystem.py       # L-Systems (Rust wrapper)
│       └── truchet.py       # Truchet tiles (Rust wrapper)
├── axiart-core/             # Rust acceleration library
│   ├── Cargo.toml           # Rust dependencies
│   └── src/
│       ├── lib.rs           # PyO3 module definition
│       ├── dendrite.rs      # Spatial grid hash DLA
│       ├── noise_core.rs    # Perlin noise with fBm
│       ├── flow_field.rs    # Parallel streamlines
│       ├── noise_pattern.rs # Marching squares
│       ├── spiral.rs        # Geometric spirals
│       ├── grid.rs          # Grid generation
│       ├── voronoi.rs       # Voronoi diagrams with Lloyd's relaxation
│       ├── lsystem.rs       # L-System string expansion and turtle interpretation
│       └── truchet.rs       # Truchet tile generation
├── examples/                # Example scripts (19 total)
├── test_*.py                # Performance benchmark scripts
├── README.md                # User documentation
├── RUST_PERFORMANCE.md      # Detailed benchmarks and architecture
├── ARTISTIC_GUIDE.md        # Artistic composition techniques (if exists)
├── CLAUDE.md                # This file
└── pyproject.toml           # Build system + dependencies (Maturin)
```

## Rust Acceleration Architecture

**All pattern generation is implemented in Rust** via PyO3 bindings compiled with Maturin.

### Key Technical Details

**Python Wrappers Are Minimal**:
- Python pattern classes (e.g., `DendritePattern`) are thin wrappers
- On `__init__`, they create a Rust generator object (e.g., `_RustDendriteGenerator`)
- All `generate_*()` methods delegate directly to Rust
- No Python fallback exists - if Rust library isn't built, imports fail immediately

**Rust Module Structure** (`axiart-core/src/`):
- `lib.rs` - PyO3 module definition, exports all generators
- `dendrite.rs` - Spatial grid hash DLA (328 lines)
- `noise_core.rs` - Perlin noise with fBm (140 lines)
- `flow_field.rs` - Parallel streamlines using rayon (357 lines)
- `noise_pattern.rs` - Marching squares for contours (357 lines)
- `spiral.rs` - Geometric spiral generation (232 lines)
- `grid.rs` - Grid generation with distortion (153 lines)
- `voronoi.rs` - Voronoi diagrams with Lloyd's relaxation (~270 lines)
- `lsystem.rs` - L-System expansion and turtle graphics (~320 lines)
- `truchet.rs` - Truchet tile generation with multiple tile types (~280 lines)

**Performance Characteristics**:
- **100-300x speedup** for dendrite generation (spatial hash vs Python loops)
- **5-20x speedup** for flow fields (parallel rayon + Rust speed)
- **2-5x speedup** for grids and spirals (Rust geometric calculations)
- **No capacity limits** - tested with 10,000+ dendrite particles, 50,000+ stipple points

**Why No Fallback**:
The previous architecture had Python implementations with `_RUST_AVAILABLE` checks. This was removed because:
1. Maintaining duplicate Python/Rust implementations was error-prone
2. Performance difference was too large (100-300x) to justify fallback
3. Rust library build is required anyway via `pyproject.toml` build system
4. Clear error messages guide users to run `maturin develop --release`

**When Adding New Patterns**:
1. Implement in Rust first (`axiart-core/src/`)
2. Export via PyO3 in `lib.rs`
3. Create Python wrapper in `axiart/patterns/`
4. Wrapper should only: initialize Rust generator, delegate method calls, provide `.draw()`
5. Rebuild Rust library: `uv run maturin develop --release`

## Dependencies

**Runtime**:
- Python >= 3.9
- svgwrite >= 1.4.3

**Build** (handled by Maturin):
- Rust toolchain (automatically installed)
- Maturin >= 1.7

**Important**: `numpy`, `noise`, and `scipy` are **no longer required** for pattern generation - all computation is in Rust. They remain as dependencies only for backwards compatibility with existing examples.

## Design Philosophy

This system separates **pattern generation** (algorithmic) from **artistic composition** (intentional). The goal is to create artwork comparable to professional generative art, not just pattern demonstrations. Always consider:

- What is the subject/theme of the composition?
- How do layers work together to tell a story?
- Is color used strategically or randomly?
- Does the composition balance organic and geometric elements?

Examples like `example_abstract_character.py` demonstrate this philosophy - combining filled shapes (head, body) with purposeful pattern layering (spiral eyes, flow field mouth, dendrite decorations).
