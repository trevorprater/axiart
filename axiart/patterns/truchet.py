"""Truchet tiles pattern generator (Rust-accelerated)."""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import TruchetGenerator as _RustTruchetGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class TruchetPattern:
    """
    Generate geometric patterns using Truchet tiles (Rust-accelerated).

    Creates patterns by arranging rotated tiles on a grid. Each tile can
    be oriented in 4 directions, creating emergent patterns.

    Tile types:
    - diagonal: Simple diagonal lines
    - arc: Quarter-circle arcs
    - double_arc: Two quarter-circles per tile
    - triangle: Triangle patterns
    - maze: Maze-like connected lines

    Performance: High-performance tile generation with flexible patterns
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        tile_type: str = "arc",
        grid_size: int = 20,
        randomness: float = 0.5,
        arc_segments: int = 16,
        seed: Optional[int] = None
    ):
        """
        Initialize the Truchet tiles pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            tile_type: Type of tile (diagonal, arc, double_arc, triangle, maze)
            grid_size: Number of tiles along the shortest dimension
            randomness: Random vs structured (0.0 = structured, 1.0 = completely random)
            arc_segments: Number of segments for arc approximation (higher = smoother)
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.tile_type = tile_type
        self.grid_size = grid_size
        self.randomness = randomness
        self.arc_segments = arc_segments
        self.seed = seed

        self.lines = []
        self.curves = []

        # Initialize Rust generator
        self._generator = _RustTruchetGenerator(
            width=width,
            height=height,
            tile_type=tile_type,
            grid_size=grid_size,
            randomness=randomness,
            arc_segments=arc_segments,
            seed=seed
        )

    def generate(self):
        """
        Generate the Truchet tiles pattern.

        Creates tiles with random or structured rotations.
        """
        lines, curves = self._generator.generate()
        self.lines = lines
        self.curves = curves

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the Truchet pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        # Draw straight lines
        for start, end in self.lines:
            canvas.add_line(start, end, layer=layer)

        # Draw curves as polylines
        for curve in self.curves:
            if len(curve) > 1:
                canvas.add_polyline(curve, layer=layer)

    def get_lines(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all straight line segments."""
        return self.lines.copy()

    def get_curves(self) -> List[List[Tuple[float, float]]]:
        """Get all curve polylines."""
        return [curve.copy() for curve in self.curves]
