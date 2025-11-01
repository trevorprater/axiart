"""
Rust-accelerated Dendrite pattern generator

This module provides a drop-in replacement for the Python DendritePattern
using the high-performance Rust implementation.
"""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart_core import DendriteGenerator as RustDendriteGenerator
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


class DendritePattern:
    """
    High-performance Dendrite Pattern using Rust backend.

    This is a drop-in replacement for the Python DendritePattern with
    20-300x better performance using KD-tree spatial indexing.

    Falls back to Python implementation if Rust extension is not available.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        num_particles: int = 3000,
        attraction_distance: float = 5.0,
        min_move_distance: float = 2.0,
        seed_points: Optional[List[Tuple[float, float]]] = None,
        branching_style: str = "radial",  # radial, vertical, horizontal
        seed: Optional[int] = None,
    ):
        """
        Initialize the dendrite pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            num_particles: Number of particles to aggregate
            attraction_distance: Distance at which particles stick
            min_move_distance: Minimum distance particles move (ignored in Rust version)
            seed_points: Initial seed points (uses center if None)
            branching_style: Style of branching (radial, vertical, horizontal)
            seed: Random seed for reproducibility
        """
        if not RUST_AVAILABLE:
            # Fall back to Python implementation
            from .dendrite import DendritePattern as PythonDendrite
            print("⚠️  Rust extension not available, using Python implementation")
            self._impl = PythonDendrite(
                width, height, num_particles, attraction_distance,
                min_move_distance, seed_points, branching_style
            )
            self._is_rust = False
        else:
            self._generator = RustDendriteGenerator(
                width=width,
                height=height,
                num_particles=num_particles,
                attraction_distance=attraction_distance,
                min_move_distance=min_move_distance,
                seed_points=seed_points,
                branching_style=branching_style,
                seed=seed,
            )
            self._is_rust = True
            self._points = []
            self._lines = []

    def generate(self, max_attempts: int = 1000):
        """
        Generate the dendrite pattern.

        Args:
            max_attempts: Maximum random walk attempts per particle
        """
        if not self._is_rust:
            self._impl.generate(max_attempts)
        else:
            self._points, self._lines = self._generator.generate(max_attempts)

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the dendrite pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        if not self._is_rust:
            self._impl.draw(canvas, layer)
        else:
            for start, end in self._lines:
                canvas.add_line(start, end, layer=layer)

    def get_points(self) -> List[Tuple[float, float]]:
        """Get all aggregated points."""
        if not self._is_rust:
            return self._impl.get_points()
        return self._points.copy()

    def get_lines(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all lines in the dendrite structure."""
        if not self._is_rust:
            return self._impl.get_lines()
        return self._lines.copy()
