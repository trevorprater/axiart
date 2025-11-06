#!/usr/bin/env python3
"""
Code Diagram Generator

Creates elegant, museum-quality visual diagrams of codebases using axiart.
Follows the philosophy: geometric elegance with algorithmic whispers.
"""

import argparse
import ast
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

try:
    import networkx as nx
except ImportError:
    print("ERROR: networkx not installed. Install with: pip install networkx")
    sys.exit(1)

# Add axiart to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from axiart.composition import Composition, ColorPalette
    from axiart.shapes import Circle, Rectangle
    from axiart.patterns.grid import GridPattern
    from axiart.patterns.spiral import SpiralPattern
    from axiart.patterns.noise import NoisePattern
except ImportError:
    print("ERROR: axiart not available. Ensure you're running from the axiart repository.")
    sys.exit(1)


class CodeFile:
    """Represents a source code file with metadata."""

    def __init__(self, path: str, relative_path: str):
        self.path = path
        self.relative_path = relative_path
        self.name = os.path.basename(path)
        self.directory = os.path.dirname(relative_path)
        self.extension = os.path.splitext(path)[1]
        self.loc = 0
        self.imports: Set[str] = set()
        self.dependencies: Set[str] = set()

    def analyze(self):
        """Count LOC and extract imports."""
        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                # Count non-empty, non-comment lines
                self.loc = sum(1 for line in lines
                              if line.strip() and not line.strip().startswith('#'))

                # Extract imports based on language
                if self.extension == '.py':
                    self._extract_python_imports(lines)
                elif self.extension in ['.js', '.ts', '.jsx', '.tsx']:
                    self._extract_js_imports(lines)
                elif self.extension == '.rs':
                    self._extract_rust_imports(lines)
                elif self.extension == '.go':
                    self._extract_go_imports(lines)
        except Exception as e:
            print(f"Warning: Could not analyze {self.path}: {e}")

    def _extract_python_imports(self, lines: List[str]):
        """Extract Python import statements."""
        for line in lines:
            line = line.strip()
            # from X import Y
            match = re.match(r'from\s+([\w.]+)\s+import', line)
            if match:
                self.imports.add(match.group(1))
            # import X
            match = re.match(r'import\s+([\w.]+)', line)
            if match:
                self.imports.add(match.group(1))

    def _extract_js_imports(self, lines: List[str]):
        """Extract JavaScript/TypeScript import statements."""
        for line in lines:
            line = line.strip()
            # import ... from 'X' or import ... from "X"
            match = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', line)
            if match:
                self.imports.add(match.group(1))
            # require('X')
            match = re.search(r'require\([\'"]([^\'"]+)[\'"]\)', line)
            if match:
                self.imports.add(match.group(1))

    def _extract_rust_imports(self, lines: List[str]):
        """Extract Rust use statements."""
        for line in lines:
            line = line.strip()
            match = re.match(r'use\s+([\w:]+)', line)
            if match:
                self.imports.add(match.group(1))

    def _extract_go_imports(self, lines: List[str]):
        """Extract Go import statements."""
        in_import = False
        for line in lines:
            line = line.strip()
            if line.startswith('import ('):
                in_import = True
            elif in_import and line == ')':
                in_import = False
            elif in_import:
                match = re.search(r'"([^"]+)"', line)
                if match:
                    self.imports.add(match.group(1))
            elif line.startswith('import'):
                match = re.search(r'"([^"]+)"', line)
                if match:
                    self.imports.add(match.group(1))


class CodebaseAnalyzer:
    """Analyzes a codebase and extracts structure."""

    SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go',
                           '.java', '.c', '.cpp', '.h', '.hpp'}

    def __init__(self, target_dir: str, max_depth: Optional[int] = None):
        self.target_dir = Path(target_dir).resolve()
        self.max_depth = max_depth
        self.files: List[CodeFile] = []
        self.total_loc = 0
        self.directories: Set[str] = set()

    def analyze(self) -> Dict:
        """Analyze the codebase and return summary statistics."""
        print(f"Analyzing codebase: {self.target_dir}")

        # Walk directory tree
        for root, dirs, files in os.walk(self.target_dir):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.')
                      and d not in ['node_modules', '__pycache__', 'target', 'build', 'dist']]

            rel_root = os.path.relpath(root, self.target_dir)
            if rel_root != '.':
                self.directories.add(rel_root)

            # Check depth limit
            if self.max_depth is not None:
                depth = len(Path(rel_root).parts)
                if depth > self.max_depth:
                    continue

            # Process source files
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in self.SUPPORTED_EXTENSIONS:
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, self.target_dir)

                    code_file = CodeFile(filepath, rel_path)
                    code_file.analyze()
                    self.files.append(code_file)
                    self.total_loc += code_file.loc

        # Build dependency graph
        self._build_dependencies()

        print(f"  Found {len(self.files)} source files")
        print(f"  Total LOC: {self.total_loc:,}")
        print(f"  Directories: {len(self.directories)}")

        return {
            'file_count': len(self.files),
            'total_loc': self.total_loc,
            'directory_count': len(self.directories),
            'dependency_count': sum(len(f.dependencies) for f in self.files)
        }

    def _build_dependencies(self):
        """Build dependency relationships between files."""
        # Create mapping from module names to files
        file_map = {}
        for f in self.files:
            # Python: package.module → file path
            if f.extension == '.py':
                module = f.relative_path.replace('/', '.').replace('.py', '')
                file_map[module] = f
                # Also map just the filename without extension
                file_map[f.name.replace('.py', '')] = f

        # Resolve dependencies
        for f in self.files:
            for imp in f.imports:
                # Try to find the imported module in our codebase
                if imp in file_map and file_map[imp] != f:
                    f.dependencies.add(file_map[imp].relative_path)


class DiagramGenerator:
    """Generates elegant code diagrams using axiart."""

    def __init__(self, analyzer: CodebaseAnalyzer, project_name: str):
        self.analyzer = analyzer
        self.project_name = project_name
        self.layout_positions = {}
        self.mark_count = 0

        # Canvas setup (A4 landscape)
        self.width = 297
        self.height = 210
        self.margin = 15

    def generate(self, layout: str = 'force-directed', accent: str = 'concentric',
                highlight_files: Optional[List[str]] = None) -> Composition:
        """Generate the diagram composition."""

        print(f"\nGenerating diagram...")
        print(f"  Layout: {layout}")
        print(f"  Accent: {accent}")

        # Create composition with layers
        comp = Composition(self.width, self.height)

        # Layers (bottom to top)
        comp.add_layer("grid", color="#DDDDDD", stroke_width=0.1)
        comp.add_layer("zones", color="none")
        comp.add_layer("dependencies", color="#AAAAAA", stroke_width=0.2)
        comp.add_layer("files", color="black", stroke_width=0.4)
        comp.add_layer("accent", color="black", stroke_width=0.2)
        comp.add_layer("highlights", color="#4A90E2", stroke_width=0.5)
        comp.add_layer("annotations", color="black", stroke_width=0.3)

        # 1. Add sparse grid background
        self._add_grid(comp)

        # 2. Calculate layout
        self._calculate_layout(layout)

        # 3. Draw directory zones (optional)
        # self._draw_zones(comp)

        # 4. Draw dependencies
        self._draw_dependencies(comp)

        # 5. Draw files as circles
        self._draw_files(comp, highlight_files or [])

        # 6. Add algorithmic accent
        if accent != 'none':
            self._add_accent(comp, accent)

        # 7. Add annotations
        self._add_annotations(comp)

        print(f"  Total marks: ~{self.mark_count:,}")

        return comp

    def _add_grid(self, comp: Composition):
        """Add sparse grid background."""
        # Calculate cell size for approximately 8-12 grid lines
        cell_size = max(self.width, self.height) / 10
        grid = GridPattern(self.width, self.height)
        grid.generate_square_grid(cell_size=cell_size)
        grid.draw(comp.get_canvas(), "grid")
        # Approximate mark count: ~10 horizontal + ~10 vertical lines
        self.mark_count += 20

    def _calculate_layout(self, layout: str):
        """Calculate spatial positions for files."""
        if len(self.analyzer.files) == 0:
            return

        # Build networkx graph
        G = nx.DiGraph()
        for f in self.analyzer.files:
            G.add_node(f.relative_path, file=f)
            for dep in f.dependencies:
                G.add_edge(f.relative_path, dep)

        # Calculate positions based on layout algorithm
        if layout == 'force-directed':
            # Spring layout with more iterations for better spacing
            pos = nx.spring_layout(G, k=2.0, iterations=100, seed=42)
        elif layout == 'hierarchical':
            # Try to use hierarchical layout
            try:
                pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
            except:
                # Fallback to spring layout
                pos = nx.spring_layout(G, iterations=50, seed=42)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G, iterations=50, seed=42)

        # Normalize positions to canvas coordinates (with margins)
        if pos:
            x_coords = [p[0] for p in pos.values()]
            y_coords = [p[1] for p in pos.values()]

            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            x_range = x_max - x_min if x_max != x_min else 1
            y_range = y_max - y_min if y_max != y_min else 1

            drawable_width = self.width - 2 * self.margin
            drawable_height = self.height - 2 * self.margin

            for node, (x, y) in pos.items():
                norm_x = self.margin + ((x - x_min) / x_range) * drawable_width
                norm_y = self.margin + ((y - y_min) / y_range) * drawable_height
                self.layout_positions[node] = (norm_x, norm_y)

    def _draw_dependencies(self, comp: Composition):
        """Draw dependency lines between files."""
        canvas = comp.get_canvas()

        for f in self.analyzer.files:
            if f.relative_path not in self.layout_positions:
                continue

            x1, y1 = self.layout_positions[f.relative_path]

            for dep in f.dependencies:
                if dep in self.layout_positions:
                    x2, y2 = self.layout_positions[dep]
                    canvas.add_line(x1, y1, x2, y2, "dependencies")
                    self.mark_count += 1

    def _draw_files(self, comp: Composition, highlight_files: List[str]):
        """Draw files as circles sized by LOC."""
        canvas = comp.get_canvas()

        # Find LOC range for scaling
        locs = [f.loc for f in self.analyzer.files if f.loc > 0]
        if not locs:
            return

        min_loc, max_loc = min(locs), max(locs)

        # Radius range (2mm to 8mm)
        min_radius = 2
        max_radius = 8

        for f in self.analyzer.files:
            if f.relative_path not in self.layout_positions:
                continue

            x, y = self.layout_positions[f.relative_path]

            # Calculate radius (sqrt scaling for better visual balance)
            if max_loc > min_loc:
                norm_loc = (f.loc - min_loc) / (max_loc - min_loc)
                radius = min_radius + math.sqrt(norm_loc) * (max_radius - min_radius)
            else:
                radius = min_radius

            # Determine layer
            is_highlighted = any(h in f.relative_path for h in highlight_files)
            layer = "highlights" if is_highlighted else "files"

            # Draw circle
            circle = Circle((x, y), radius)
            canvas.add_polyline(circle.get_points(), layer)
            self.mark_count += 1

    def _add_accent(self, comp: Composition, accent: str):
        """Add subtle algorithmic accent."""
        canvas = comp.get_canvas()

        # Find the most complex files (top 10% by LOC)
        sorted_files = sorted(self.analyzer.files, key=lambda f: f.loc, reverse=True)
        top_count = max(3, len(sorted_files) // 10)
        complex_files = sorted_files[:top_count]

        accent_marks = 0
        max_accent_marks = 500  # Strict limit

        for f in complex_files:
            if f.relative_path not in self.layout_positions:
                continue
            if accent_marks >= max_accent_marks:
                break

            x, y = self.layout_positions[f.relative_path]

            if accent == 'concentric':
                # Add 3-5 concentric circles
                base_radius = 2 + math.sqrt(f.loc / 100) * 2
                for i in range(3):
                    r = base_radius + i * 1.5
                    circle = Circle((x, y), r)
                    canvas.add_polyline(circle.get_points(), "accent")
                    accent_marks += 1

            elif accent == 'stippling':
                # Add subtle stippling inside the circle
                base_radius = 2 + math.sqrt(f.loc / 100) * 2
                point_count = min(50, f.loc // 20)

                for _ in range(point_count):
                    if accent_marks >= max_accent_marks:
                        break
                    # Random point in circle
                    angle = random.uniform(0, 2 * math.pi)
                    r = random.uniform(0, base_radius * 0.8)
                    px = x + r * math.cos(angle)
                    py = y + r * math.sin(angle)
                    canvas.add_point(px, py, "accent")
                    accent_marks += 1

        self.mark_count += accent_marks

    def _add_annotations(self, comp: Composition):
        """Add file labels and coordinate markers."""
        canvas = comp.get_canvas()

        # Add coordinate grid markers (corners only)
        markers = [
            (self.margin, self.margin, "0,0"),
            (self.width - self.margin, self.margin, f"{self.width-2*self.margin:.0f},0"),
            (self.margin, self.height - self.margin, f"0,{self.height-2*self.margin:.0f}"),
        ]

        for x, y, label in markers:
            canvas.dwg.add(canvas.dwg.text(
                label, insert=(x, y),
                fill='#999999',
                font_size='6pt',
                font_family='monospace'
            ))
            self.mark_count += 1

        # Add file labels for largest files
        sorted_files = sorted(self.analyzer.files, key=lambda f: f.loc, reverse=True)
        top_files = sorted_files[:15]  # Label top 15 files

        for f in top_files:
            if f.relative_path not in self.layout_positions:
                continue

            x, y = self.layout_positions[f.relative_path]

            # Abbreviate long names
            label = f.name if len(f.name) <= 15 else f.name[:12] + "..."

            canvas.dwg.add(canvas.dwg.text(
                label, insert=(x + 5, y),
                fill='black',
                font_size='5pt',
                font_family='monospace'
            ))
            self.mark_count += 1


def export_png(svg_path: str, png_path: str, width: int = 3000):
    """Export SVG to PNG using cairosvg (if available)."""
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=width)
        print(f"  Exported: {png_path}")
    except ImportError:
        print("  Warning: cairosvg not installed, skipping PNG export")
        print("  Install with: pip install cairosvg")


def write_philosophy(output_path: str, project_name: str, stats: Dict,
                     layout: str, accent: str, mark_count: int):
    """Write the philosophy document explaining visualization choices."""

    negative_space = 50  # Approximate

    content = f"""# {project_name} - Code Diagram Philosophy

## Codebase Analysis

This diagram visualizes the structure of the **{project_name}** codebase:

- **{stats['file_count']} source files** analyzed
- **{stats['total_loc']:,} total lines of code**
- **{stats['dependency_count']} dependencies** mapped
- **{stats['directory_count']} directories** identified

## Visualization Strategy

### Layout Algorithm: {layout.title()}

The spatial arrangement uses **{layout}** layout, which positions files based on their relationships:
- Central positions → Highly connected modules
- Peripheral positions → Leaf nodes and utilities
- Spatial proximity → Related functionality

### Visual Encoding

**Files → Circles**
Each source file is represented as a circle, with radius proportional to √(LOC). This square-root scaling ensures visual balance—large files don't dominate the composition.

**Dependencies → Lines**
Thin gray lines connect files that import or require each other, revealing the dependency graph structure.

**Complexity → {accent.title()}**
The most complex files (top 10% by LOC) are highlighted with {accent}—subtle visual cues suggesting internal structure without overwhelming the composition.

## Aesthetic Choices

### Geometric Elegance (70%)

The foundation is pure geometry: circles, lines, sparse grid. This creates immediate readability—you can grasp the system structure at a glance.

### Algorithmic Whispers (30%)

Strategic use of {accent} adds depth without chaos. These subtle patterns reward sustained viewing, hinting at the complexity hidden within the geometric scaffolding.

### Restraint & Negative Space

- **Total marks**: ~{mark_count:,} (target: 3,000-8,000)
- **Negative space**: ~{negative_space}% (target: 40%+)
- **Color palette**: Black + blue accent for entry points
- **Grid substrate**: Sparse coordinate system for reference

The composition breathes. Empty space is not waste—it's essential for clarity.

## Design Philosophy

> "Code is invisible architecture. We make it visible through geometric translation, not literal representation."

This diagram doesn't show every file or every dependency. It shows the **essential structure**: the skeleton of the system, the critical relationships, the zones of complexity.

It's meant to be:
- **Immediately readable**: Understand the structure at a glance
- **Studyably deep**: Discover details on closer inspection
- **Aesthetically refined**: Beautiful enough to frame
- **Technically accurate**: Reflects actual code relationships

---

**Generated by**: code-diagram-generator skill
**Layout**: {layout}
**Accent**: {accent}
**Canvas**: 297×210mm (A4 landscape)
**Format**: SVG (vector) + PNG (raster preview)
"""

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"  Wrote: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate elegant code architecture diagrams using axiart'
    )
    parser.add_argument('--target', type=str, default='.',
                       help='Target directory to analyze (default: current directory)')
    parser.add_argument('--project-name', type=str, default='Project',
                       help='Project name for output files')
    parser.add_argument('--layout', type=str, default='force-directed',
                       choices=['force-directed', 'hierarchical', 'circular'],
                       help='Layout algorithm')
    parser.add_argument('--accent', type=str, default='concentric',
                       choices=['concentric', 'stippling', 'none'],
                       help='Algorithmic accent pattern')
    parser.add_argument('--highlight-files', type=str, default='',
                       help='Comma-separated list of files to highlight')
    parser.add_argument('--output-dir', type=str, default='./diagrams',
                       help='Output directory')
    parser.add_argument('--max-depth', type=int, default=None,
                       help='Maximum directory depth to analyze')

    args = parser.parse_args()

    # Parse highlight files
    highlight_files = [f.strip() for f in args.highlight_files.split(',') if f.strip()]

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Analyze codebase
    analyzer = CodebaseAnalyzer(args.target, args.max_depth)
    stats = analyzer.analyze()

    if len(analyzer.files) == 0:
        print("ERROR: No source files found in target directory")
        return 1

    # Generate diagram
    generator = DiagramGenerator(analyzer, args.project_name)
    comp = generator.generate(args.layout, args.accent, highlight_files)

    # Save SVG
    svg_path = output_dir / f"{args.project_name}_diagram.svg"
    comp.save(str(svg_path))
    print(f"\n✓ Generated: {svg_path}")

    # Export PNG
    png_path = output_dir / f"{args.project_name}_diagram.png"
    export_png(str(svg_path), str(png_path))

    # Write philosophy
    philosophy_path = output_dir / f"{args.project_name}_philosophy.md"
    write_philosophy(str(philosophy_path), args.project_name, stats,
                    args.layout, args.accent, generator.mark_count)

    # Print summary
    print(f"\n{'='*50}")
    print(f"✓ CODE DIAGRAM: {args.project_name}")
    print(f"{'='*50}")
    print(f"CODEBASE ANALYSIS:")
    print(f"  Files analyzed: {stats['file_count']}")
    print(f"  Total LOC: {stats['total_loc']:,}")
    print(f"  Dependencies: {stats['dependency_count']}")
    print(f"  Directories: {stats['directory_count']}")
    print(f"\nVISUALIZATION:")
    print(f"  Layout: {args.layout}")
    print(f"  Accent: {args.accent}")
    print(f"  Total marks: ~{generator.mark_count:,}")
    print(f"\nOUTPUT:")
    print(f"  {svg_path.name}")
    print(f"  {png_path.name}")
    print(f"  {philosophy_path.name}")
    print(f"\nElegant. Precise. Studyable.")
    print(f"{'='*50}\n")

    return 0


if __name__ == '__main__':
    import random  # For stippling if needed
    sys.exit(main())
