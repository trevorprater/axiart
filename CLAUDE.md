# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AxiArt is a generative art system for creating algorithmic artwork optimized for the AxiDraw V3 pen plotter. It uses a modular, layer-based composition system where patterns are generated algorithmically and then combined on an SVG canvas.

## Development Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Installation
```bash
uv sync
```

### Running Examples
```bash
cd examples
uv run python example_simple_starter.py      # Basic spiral example
uv run python example_abstract_character.py  # Complex artistic composition
uv run python example_mixed_landscape.py     # Multi-pattern landscape
uv run python example_showcase.py            # All patterns in one
```

### Code Formatting
```bash
uv run black axiart/                  # Format all code (line-length: 100)
```

### Testing (if pytest is installed)
```bash
uv run pytest                         # Run tests if they exist
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

**Pattern Generators** (`axiart/patterns/`)
- Each pattern class follows the same interface:
  1. Initialize with canvas dimensions and parameters
  2. Call a `generate_*()` method to compute the pattern
  3. Call `.draw(canvas, layer_name)` to render to canvas
  4. Optionally call `.get_points()`, `.get_lines()`, etc. for raw data
- Patterns store computed geometry internally and can be drawn multiple times

**Shapes System** (`axiart/shapes.py`)
- Basic geometric shapes: `Circle`, `Rectangle`, `Polygon`
- `add_filled_shape()` helper for creating filled shapes with strokes
- Shapes can be filled with color (critical for artistic compositions)

### Pattern Types

1. **DendritePattern** - Organic branching structures using Diffusion-Limited Aggregation (DLA)
   - Branching styles: `"radial"`, `"vertical"`, `"horizontal"`
   - Controlled by `num_particles`, `attraction_distance`, `seed_points`

2. **SpiralPattern** - Spirals and concentric circles
   - Types: Archimedean, logarithmic, Fermat (parabolic), circular waves
   - Each type has a different `generate_*()` method

3. **GridPattern** - Geometric grids with optional distortion
   - Grid types: square, hexagonal, triangular
   - Apply distortions: `apply_radial_distortion()`, custom functions

4. **NoisePattern** - Perlin noise-based textures
   - Outputs: contour lines, stippling, cellular texture, hatching
   - Controlled by `scale` (smoothness) and `octaves` (detail)

5. **FlowFieldPattern** - Vector field particle tracing
   - Field types: `"noise"`, `"radial"`, `"spiral"`, `"waves"`, `"custom"`
   - Outputs: streamlines, particle systems, grid visualization, curl noise

### Workflow: From Patterns to Art

The system is designed around **intentional artistic composition**, not just pattern demonstration:

1. **Create Composition with Layers** - Define layer hierarchy (back to front)
2. **Add Filled Shapes** - Use `shapes.py` to create colored geometric forms (faces, bodies, etc.)
3. **Layer Patterns with Purpose** - Each pattern serves a compositional role:
   - Grids → background structure
   - Spirals → focal points (eyes, centers)
   - Flow fields → texture and movement
   - Dendrites → organic growth (hair, trees)
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
- AxiDraw V3 compatible: max plotting area depends on model

### Direct SVG Manipulation
For advanced use, access the underlying `svgwrite.Drawing` object:
```python
canvas.dwg.add(canvas.dwg.rect(...))  # Direct svgwrite calls
```

### Color Palettes
Predefined palettes in `composition.py`:
- `ColorPalette.MONO`, `RED_ACCENT`, `BLUE_ACCENT`, `GOLD_ACCENT`, etc.
- Use with `create_standard_composition(palette=ColorPalette.RED_ACCENT)`

### Example Patterns
- Simple patterns: `example_dendrite.py`, `example_spiral.py`, etc.
- Artistic compositions: `example_abstract_character.py`, `example_portrait.py`
- The artistic examples demonstrate proper layer usage, filled shapes, and pattern constraining

## File Organization

```
axiart/
├── axiart/                  # Main package
│   ├── svg_exporter.py      # SVGCanvas - low-level canvas
│   ├── composition.py       # Composition - high-level layer system
│   ├── shapes.py            # Geometric shapes with fills
│   └── patterns/            # Pattern generators
│       ├── dendrite.py      # DLA branching
│       ├── spiral.py        # Spirals and circles
│       ├── grid.py          # Geometric grids
│       ├── noise.py         # Perlin noise patterns
│       └── flow_field.py    # Vector field patterns
├── examples/                # Example scripts (10 total)
├── README.md                # User documentation
├── ARTISTIC_GUIDE.md        # Artistic composition techniques
└── pyproject.toml           # Dependencies and config
```

## Dependencies

Core: `numpy`, `svgwrite`, `noise`, `scipy`

Development: `pytest`, `black` (both optional)

Python >= 3.9 required

## Design Philosophy

This system separates **pattern generation** (algorithmic) from **artistic composition** (intentional). The goal is to create artwork comparable to professional generative art, not just pattern demonstrations. Always consider:

- What is the subject/theme of the composition?
- How do layers work together to tell a story?
- Is color used strategically or randomly?
- Does the composition balance organic and geometric elements?

Examples like `example_abstract_character.py` demonstrate this philosophy - combining filled shapes (head, body) with purposeful pattern layering (spiral eyes, flow field mouth, dendrite decorations).
