# Code Diagram Generator

A Claude skill that creates elegant, museum-quality visual diagrams of codebases using the axiart library.

## Overview

Transforms code structure into geometric art: elegant technical diagrams that are both informative and aesthetically compelling. Not traditional box-and-arrow charts, but artistic representations of software architecture.

## Aesthetic Philosophy

**Geometric Elegance with Algorithmic Whispers**

- 70% geometric scaffolding (clean shapes, precise layout)
- 30% algorithmic accent (subtle patterns)
- 3,000-8,000 marks total
- 40-50% negative space
- Strategic color accents (1-2 colors)

## Installation

This skill is automatically available in Claude Code when working in the axiart repository.

### Dependencies

```bash
# Required
pip install networkx>=3.0

# Optional (for PNG export)
pip install cairosvg pillow
```

## Usage

Ask Claude to generate a code diagram:

```
Generate a diagram of the axiart codebase
```

```
Visualize the architecture of the axiart/patterns directory
```

```
Create a dependency map for the Rust modules
```

Claude will:
1. Analyze the codebase structure
2. Generate an elegant geometric diagram
3. Export SVG + PNG + philosophy document

## Manual Usage

You can also run the generator script directly:

```bash
python .claude/skills/code-diagram-generator/generator.py \
  --target ./axiart \
  --project-name "axiart" \
  --layout force-directed \
  --accent concentric \
  --output-dir ./diagrams
```

### Options

- `--target PATH` - Directory to analyze (default: current directory)
- `--project-name NAME` - Project name for output files
- `--layout ALGORITHM` - Layout algorithm:
  - `force-directed` (default) - For dependency-heavy codebases
  - `hierarchical` - For tree-like structures
  - `circular` - For radial arrangements
- `--accent PATTERN` - Algorithmic accent:
  - `concentric` (default) - Concentric circles in complex files
  - `stippling` - Dot density suggesting complexity
  - `none` - Pure geometric clarity
- `--highlight-files FILES` - Comma-separated files to emphasize
- `--output-dir DIR` - Output directory (default: ./diagrams)
- `--max-depth N` - Maximum directory depth

## Output

Three files are generated:

1. **`{project}_diagram.svg`** - Vector diagram (297×210mm, A4)
2. **`{project}_diagram.png`** - Raster preview (3000px, 300 DPI)
3. **`{project}_philosophy.md`** - Explanation of visualization choices

## Supported Languages

- Python (`.py`)
- JavaScript/TypeScript (`.js`, `.ts`, `.tsx`, `.jsx`)
- Rust (`.rs`)
- Go (`.go`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`, `.hpp`)

Dependency extraction works best with Python, JS/TS, Rust, and Go.

## Visual Encoding

**Files → Circles**
- Radius proportional to √(LOC)
- Positioned by layout algorithm
- Black stroke, no fill

**Dependencies → Lines**
- Thin gray lines connect imports
- Shows information flow
- Reveals module coupling

**Directories → Zones**
- Subtle background regions (optional)
- Groups related files
- Light fills for clarity

**Complexity → Patterns**
- Top 10% complex files get accent
- Concentric circles or stippling
- Very subtle, never overwhelming

**Entry Points → Color**
- Blue accent for highlighted files
- Emphasizes critical paths
- Strategic color use only

## Examples

### Simple Project Structure

```bash
python generator.py \
  --target ~/myproject/src \
  --project-name "myproject" \
  --layout hierarchical \
  --accent none
```

Clean geometric layout showing directory hierarchy.

### Complex Microservices

```bash
python generator.py \
  --target ~/services \
  --project-name "services" \
  --layout force-directed \
  --accent concentric \
  --highlight-files "main.py,server.js"
```

Dependency graph with complexity hints and entry point highlighting.

### Large Codebase

```bash
python generator.py \
  --target ~/linux/kernel \
  --project-name "linux-kernel" \
  --layout force-directed \
  --max-depth 2 \
  --accent none
```

Limit depth to avoid overwhelming complexity.

## Design Constraints

**The skill enforces:**
- Maximum 8,000 marks (geometric elements)
- Minimum 40% negative space
- Maximum 2 accent colors
- Sparse grid (10-20 lines)
- Legible annotations (6pt minimum)

**The skill avoids:**
- Dense spaghetti diagrams
- Visual chaos or aggression
- Unreadable text
- Overwhelming patterns
- Filling the entire canvas

## Philosophy

Code is invisible architecture. We make it visible through geometric translation, not literal representation.

A good code diagram is a scientific instrument: precise, elegant, revealing hidden structure through carefully chosen geometric primitives and spatial relationships.

**Restraint is the highest virtue.**

## Skill Details

- **Version**: 1.0
- **Created for**: Claude Code
- **Aesthetic**: Geometric elegance with algorithmic whispers
- **Inspiration**: Museum exhibits, scientific instruments, architectural blueprints

## Examples

See the `examples/` directory in the axiart repository for generated diagrams.

## Troubleshooting

**"No source files found"**
- Check the target directory path
- Ensure it contains supported file types

**"networkx not installed"**
```bash
pip install networkx
```

**"PNG export failed"**
```bash
pip install cairosvg pillow
```

**Diagram too dense**
- Use `--max-depth` to limit recursion
- Choose `--accent none` for clarity
- Filter out small files (edit generator.py)

**Layout looks poor**
- Try different `--layout` algorithms
- Adjust `--highlight-files` for emphasis
- Increase canvas size for large codebases

## License

Same as axiart (see repository root).
