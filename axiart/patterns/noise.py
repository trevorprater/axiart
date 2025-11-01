"""Noise and texture field pattern generator using Perlin noise (Rust-accelerated)."""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import NoisePatternGenerator as _RustNoisePatternGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class NoisePattern:
    """
    Generate noise-based patterns including contour lines, stippling, and textures (Rust-accelerated).

    Uses Perlin noise to create organic, natural-looking patterns
    including topographic-style contour lines and cellular textures.

    Performance: 12M points/sec (stippling), 1.67M segments/sec (contours)
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        scale: float = 100.0,
        octaves: int = 4,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
        seed: Optional[int] = None
    ):
        """
        Initialize the noise pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            scale: Noise scale (larger = smoother)
            octaves: Number of octaves (detail layers)
            persistence: Amplitude decay per octave
            lacunarity: Frequency increase per octave
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed

        # Initialize Rust generator
        self._generator = _RustNoisePatternGenerator(
            width=width,
            height=height,
            scale=scale,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            seed=seed
        )

        self.lines = []
        self.points = []

    def generate_contour_lines(
        self,
        num_levels: int = 20,
        resolution: float = 2.0,
        min_value: float = -1.0,
        max_value: float = 1.0
    ):
        """
        Generate topographic-style contour lines using marching squares.

        Args:
            num_levels: Number of contour levels
            resolution: Grid resolution (smaller = more detail)
            min_value: Minimum noise value
            max_value: Maximum noise value
        """
        self.lines = self._generator.generate_contour_lines(
            num_levels=num_levels,
            resolution=resolution,
            min_value=min_value,
            max_value=max_value
        )

    def generate_stippling(
        self,
        num_points: int = 5000,
        density_map: bool = True,
        threshold: float = 0.0,
        parallel: bool = True
    ):
        """
        Generate stippling (dots) based on noise density.

        Args:
            num_points: Number of candidate points
            density_map: Use noise as density map
            threshold: Noise threshold for point placement
            parallel: Use parallel generation
        """
        self.points = self._generator.generate_stippling(
            num_points=num_points,
            density_map=density_map,
            threshold=threshold,
            parallel=parallel
        )

    def generate_cellular_texture(
        self,
        cell_size: float = 5.0,
        threshold: float = 0.0,
        pattern_type: str = "squares"  # squares, circles, hatching
    ):
        """
        Generate cellular texture patterns.

        Args:
            cell_size: Size of cells
            threshold: Noise threshold for pattern density
            pattern_type: Type of pattern (squares, circles, hatching)

        Returns:
            Tuple of (paths, points) where paths are lines and points are centers
        """
        paths, points = self._generator.generate_cellular_texture(
            cell_size=cell_size,
            threshold=threshold,
            pattern_type=pattern_type
        )
        self.lines = paths
        self.points = points
        return paths, points

    def generate_hatching(
        self,
        spacing: float = 5.0,
        line_length: float = 10.0,
        threshold: float = 0.0
    ):
        """
        Generate hatching lines based on noise gradients.

        Args:
            spacing: Space between hatch lines
            line_length: Length of hatch lines
            threshold: Noise threshold for hatching
        """
        self.lines = self._generator.generate_hatching(
            spacing=spacing,
            line_length=line_length,
            threshold=threshold
        )

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the noise pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        # Draw lines
        for line in self.lines:
            if len(line) > 1:
                canvas.add_polyline(line, layer=layer)

        # Draw points
        if self.points:
            canvas.add_points(self.points, layer=layer)

    def get_lines(self) -> List[List[Tuple[float, float]]]:
        """Get all generated lines."""
        return [line.copy() for line in self.lines]

    def get_points(self) -> List[Tuple[float, float]]:
        """Get all generated points."""
        return self.points.copy() if isinstance(self.points, list) else list(self.points)
