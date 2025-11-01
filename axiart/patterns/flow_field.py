"""Flow field pattern generator using vector fields and particle systems (Rust-accelerated)."""

from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import FlowFieldGenerator as _RustFlowFieldGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class FlowFieldPattern:
    """
    Generate flow field patterns using vector fields (Rust-accelerated).

    Creates organic, flowing patterns by tracing particles through
    a vector field, which can be based on Perlin noise, mathematical
    functions, or custom field definitions.

    Performance: 12.5M points/sec (pure Rust implementation with parallel generation)
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        field_type: str = "noise",  # noise, radial, spiral, waves
        scale: float = 50.0,
        seed: Optional[int] = None
    ):
        """
        Initialize the flow field pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            field_type: Type of vector field (noise, radial, spiral, waves)
            scale: Scale for noise-based fields
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.field_type = field_type
        self.scale = scale
        self.seed = seed

        # Initialize Rust generator
        self._generator = _RustFlowFieldGenerator(
            width=width,
            height=height,
            field_type=field_type,
            scale=scale,
            seed=seed
        )

        self.paths = []

    def generate_streamlines(
        self,
        num_lines: int = 50,
        steps: int = 100,
        step_size: float = 1.0,
        parallel: bool = True
    ):
        """
        Generate streamlines by tracing particles through the flow field.

        Args:
            num_lines: Number of streamlines to generate
            steps: Number of steps per streamline
            step_size: Distance to move at each step
            parallel: Use parallel generation (faster on multi-core systems)
        """
        self.paths = self._generator.generate_streamlines(
            num_lines=num_lines,
            steps=steps,
            step_size=step_size,
            parallel=parallel
        )

    def generate_curl_noise_lines(
        self,
        num_lines: int = 50,
        steps: int = 100,
        step_size: float = 1.0,
        parallel: bool = True
    ):
        """
        Generate divergence-free flow lines using curl noise.

        Args:
            num_lines: Number of lines to generate
            steps: Number of steps per line
            step_size: Distance to move at each step
            parallel: Use parallel generation (faster on multi-core systems)
        """
        self.paths = self._generator.generate_curl_noise_lines(
            num_lines=num_lines,
            steps=steps,
            step_size=step_size,
            parallel=parallel
        )

    def generate_grid_visualization(
        self,
        grid_resolution: int = 20
    ):
        """
        Generate a grid visualization of the vector field.

        Args:
            grid_resolution: Number of grid cells in each dimension
        """
        self.paths = self._generator.generate_grid_visualization(
            grid_resolution=grid_resolution
        )

    def draw(self, canvas: SVGCanvas, layer: str, as_points: bool = False):
        """
        Draw the flow field pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
            as_points: Draw as points instead of lines
        """
        for path in self.paths:
            if as_points:
                canvas.add_points(path, layer=layer)
            else:
                if len(path) > 1:
                    canvas.add_polyline(path, layer=layer)

    def get_paths(self) -> List[List[Tuple[float, float]]]:
        """Get all flow field paths."""
        return [path.copy() for path in self.paths]
