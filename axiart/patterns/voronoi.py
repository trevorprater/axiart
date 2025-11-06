"""Voronoi diagram pattern generator (Rust-accelerated)."""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import VoronoiGenerator as _RustVoronoiGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class VoronoiPattern:
    """
    Generate cellular patterns using Voronoi diagrams (Rust-accelerated).

    Creates space-dividing patterns where each region contains points
    closest to a specific site. Perfect for organic textures, stained
    glass effects, and cellular patterns.

    Performance: High-performance sampling-based edge detection
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        num_sites: int = 100,
        relaxation_iterations: int = 0,
        clip_to_bounds: bool = True,
        sampling_resolution: int = 800,
        seed: Optional[int] = None
    ):
        """
        Initialize the Voronoi pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            num_sites: Number of Voronoi sites (cell centers)
            relaxation_iterations: Number of Lloyd's relaxation iterations for uniform cells (0 = random)
            clip_to_bounds: Whether to clip edges to canvas boundaries
            sampling_resolution: Resolution for edge detection (higher = more accurate but slower)
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.num_sites = num_sites
        self.relaxation_iterations = relaxation_iterations
        self.clip_to_bounds = clip_to_bounds
        self.sampling_resolution = sampling_resolution
        self.seed = seed

        self.sites = []
        self.edges = []

        # Initialize Rust generator
        self._generator = _RustVoronoiGenerator(
            width=width,
            height=height,
            num_sites=num_sites,
            relaxation_iterations=relaxation_iterations,
            clip_to_bounds=clip_to_bounds,
            sampling_resolution=sampling_resolution,
            seed=seed
        )

    def generate(self):
        """
        Generate the Voronoi diagram.

        Creates sites and detects cell boundaries.
        """
        sites, edges = self._generator.generate()
        self.sites = sites
        self.edges = edges

    def draw(self, canvas: SVGCanvas, layer: str, draw_sites: bool = False):
        """
        Draw the Voronoi pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
            draw_sites: Whether to draw the site points
        """
        # Draw edges
        for start, end in self.edges:
            canvas.add_line(start, end, layer=layer)

        # Optionally draw sites
        if draw_sites:
            canvas.add_points(self.sites, layer=layer, radius=1.0)

    def get_sites(self) -> List[Tuple[float, float]]:
        """Get all Voronoi sites."""
        return self.sites.copy()

    def get_edges(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all cell boundary edges."""
        return self.edges.copy()
