"""L-System (Lindenmayer System) pattern generator (Rust-accelerated)."""

from typing import List, Tuple, Optional, Dict
from ..svg_exporter import SVGCanvas

try:
    from axiart.axiart_core import LSystemGenerator as _RustLSystemGenerator
except ImportError as e:
    raise ImportError(
        "Rust acceleration library not found. Please build it with:\n"
        "  uv run maturin develop --release\n"
        f"Original error: {e}"
    )


class LSystemPattern:
    """
    Generate fractal patterns using L-Systems (Rust-accelerated).

    L-Systems use string rewriting rules to create complex fractal
    structures. Perfect for plants, trees, fractals, and organic growth.

    Available presets:
    - koch, koch_snowflake: Classic Koch curve and snowflake
    - sierpinski: Sierpinski triangle
    - dragon: Dragon curve
    - hilbert: Hilbert space-filling curve
    - plant1, plant2, bushy: Various plant-like structures

    Performance: High-performance string expansion and turtle interpretation
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        preset: str = "plant1",
        iterations: int = 4,
        step_length: Optional[float] = None,
        start_x: Optional[float] = None,
        start_y: Optional[float] = None,
        start_angle: Optional[float] = None
    ):
        """
        Initialize the L-System pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            preset: Preset L-System name (koch, snowflake, sierpinski, dragon, hilbert, plant1, plant2, bushy)
            iterations: Number of iterations to expand the L-System (more = more detail)
            step_length: Length of each forward step (None = auto-calculated)
            start_x: Starting x position (None = preset default)
            start_y: Starting y position (None = preset default)
            start_angle: Starting angle in degrees (None = preset default)
        """
        self.width = width
        self.height = height
        self.preset = preset
        self.iterations = iterations

        self.lines = []

        # Initialize Rust generator
        self._generator = _RustLSystemGenerator(
            width=width,
            height=height,
            preset=preset,
            iterations=iterations,
            step_length=step_length,
            start_x=start_x,
            start_y=start_y,
            start_angle=start_angle
        )

    @classmethod
    def create_custom(
        cls,
        width: float = 297,
        height: float = 210,
        axiom: str = "F",
        rules: Optional[Dict[str, str]] = None,
        angle: float = 25.0,
        iterations: int = 4,
        step_length: float = 5.0,
        start_x: Optional[float] = None,
        start_y: Optional[float] = None,
        start_angle: float = 90.0
    ):
        """
        Create a custom L-System with your own rules.

        Args:
            width: Canvas width
            height: Canvas height
            axiom: Starting string
            rules: Dictionary mapping characters to replacement strings
            angle: Turning angle in degrees
            iterations: Number of iterations
            step_length: Length of forward steps
            start_x: Starting x position (None = center)
            start_y: Starting y position (None = center)
            start_angle: Starting angle in degrees

        Turtle commands:
            F, G: Move forward drawing a line
            f: Move forward without drawing
            +: Turn left by angle
            -: Turn right by angle
            [: Push state onto stack
            ]: Pop state from stack

        Example:
            pattern = LSystemPattern.create_custom(
                axiom="F",
                rules={"F": "F+F-F-F+F"},
                angle=90.0,
                iterations=3
            )
        """
        instance = cls.__new__(cls)
        instance.width = width
        instance.height = height
        instance.preset = "custom"
        instance.iterations = iterations
        instance.lines = []

        # Initialize Rust generator with custom rules
        instance._generator = _RustLSystemGenerator.create_custom(
            width=width,
            height=height,
            axiom=axiom,
            rules=rules,
            angle=angle,
            iterations=iterations,
            step_length=step_length,
            start_x=start_x,
            start_y=start_y,
            start_angle=start_angle
        )

        return instance

    def generate(self):
        """
        Generate the L-System pattern.

        Expands the L-System string and interprets it as turtle graphics.
        """
        lines = self._generator.generate()
        self.lines = lines

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the L-System pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        for start, end in self.lines:
            canvas.add_line(start, end, layer=layer)

    def get_lines(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all lines in the L-System structure."""
        return self.lines.copy()
