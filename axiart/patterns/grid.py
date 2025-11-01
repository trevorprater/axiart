"""Grid pattern generator for square and hexagonal grids (Rust-accelerated)."""

from typing import List, Tuple, Optional, Callable
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import GridGenerator as _RustGridGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class GridPattern:
    """
    Generate geometric grid structures (Rust-accelerated).

    Supports square grids, hexagonal grids, and radial distortions.

    Performance: 8-12M points/sec (pure Rust implementation)
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        grid_type: str = "square"  # square, hexagonal
    ):
        """
        Initialize the grid pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            grid_type: Type of grid (square, hexagonal)
        """
        self.width = width
        self.height = height
        self.grid_type = grid_type
        self.lines = []
        self.cells = []

        # Initialize Rust generator
        self._generator = _RustGridGenerator(width=width, height=height)

    def generate_square_grid(
        self,
        cell_size: float = 10,
        jitter: float = 0
    ):
        """
        Generate a square grid.

        Args:
            cell_size: Size of grid cells
            jitter: Random jitter amount (0 = perfect grid)
        """
        self.lines = self._generator.generate_square_grid(
            cell_size=cell_size,
            jitter=jitter
        )

    def generate_hexagonal_grid(
        self,
        cell_size: float = 10
    ):
        """
        Generate a hexagonal grid.

        Args:
            cell_size: Size of hexagonal cells
        """
        self.lines = self._generator.generate_hexagonal_grid(cell_size=cell_size)

    def apply_radial_distortion(
        self,
        center: Optional[Tuple[float, float]] = None,
        strength: float = 0.5
    ):
        """
        Apply radial distortion to existing grid lines.

        Args:
            center: Center point for distortion (uses canvas center if None)
            strength: Distortion strength (0 = no distortion, 1 = strong)
        """
        if not self.lines:
            raise ValueError("No grid lines to distort. Generate a grid first.")

        self.lines = self._generator.apply_radial_distortion(
            lines=self.lines,
            center=center,
            strength=strength
        )

    def apply_custom_distortion(
        self,
        distortion_func: Callable[[float, float], Tuple[float, float]]
    ):
        """
        Apply a custom distortion function to grid points.

        Args:
            distortion_func: Function that takes (x, y) and returns (new_x, new_y)
        """
        distorted_lines = []
        for line in self.lines:
            distorted_points = [distortion_func(x, y) for x, y in line]
            distorted_lines.append(distorted_points)
        self.lines = distorted_lines

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the grid pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        for line in self.lines:
            if len(line) > 1:
                canvas.add_polyline(line, layer=layer)

        for cell in self.cells:
            if len(cell) > 1:
                canvas.add_polygon(cell, layer=layer)

    def get_lines(self) -> List[List[Tuple[float, float]]]:
        """Get all grid lines."""
        return [line.copy() for line in self.lines]

    def get_cells(self) -> List[List[Tuple[float, float]]]:
        """Get all grid cells."""
        return [cell.copy() for cell in self.cells]
