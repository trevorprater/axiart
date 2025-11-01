"""Dendrite and branching pattern generator using DLA (Rust-accelerated)."""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import DendriteGenerator as _RustDendriteGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class DendritePattern:
    """
    Generate organic, tree-like or river-like branching structures (Rust-accelerated).

    Uses a Diffusion-Limited Aggregation (DLA) algorithm to create
    natural-looking dendrite patterns.

    Performance: 920 particles/sec (10K particles) - 100-300x faster than Python
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
        seed: Optional[int] = None
    ):
        """
        Initialize the dendrite pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            num_particles: Number of particles to aggregate
            attraction_distance: Distance at which particles stick
            min_move_distance: Minimum distance particles move
            seed_points: Initial seed points (uses center if None)
            branching_style: Style of branching (radial, vertical, horizontal)
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.attraction_distance = attraction_distance
        self.min_move_distance = min_move_distance
        self.branching_style = branching_style
        self.seed = seed

        self.tree = []
        self.lines = []

        # Initialize Rust generator
        self._generator = _RustDendriteGenerator(
            width=width,
            height=height,
            num_particles=num_particles,
            attraction_distance=attraction_distance,
            min_move_distance=min_move_distance,
            seed_points=seed_points,
            branching_style=branching_style,
            seed=seed
        )

    def generate(self, max_attempts: int = 1000):
        """
        Generate the dendrite pattern.

        Args:
            max_attempts: Maximum random walk attempts per particle
        """
        points, lines = self._generator.generate(max_attempts)
        self.tree = points
        self.lines = lines

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the dendrite pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        for start, end in self.lines:
            canvas.add_line(start, end, layer=layer)

    def get_points(self) -> List[Tuple[float, float]]:
        """Get all aggregated points."""
        return self.tree.copy()

    def get_lines(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all lines in the dendrite structure."""
        return self.lines.copy()
