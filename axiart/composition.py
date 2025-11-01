"""Composition system for layering and combining multiple patterns."""

from typing import Dict, List, Tuple, Optional
from .svg_exporter import SVGCanvas


class Composition:
    """
    System for composing multiple patterns with layering and styling.

    Manages multiple pattern layers with individual colors, opacity,
    and blend effects to create complex compositions.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        background: str = "white"
    ):
        """
        Initialize the composition.

        Args:
            width: Canvas width
            height: Canvas height
            background: Background color
        """
        self.width = width
        self.height = height
        self.background = background
        self.canvas = SVGCanvas(width, height, background)

        # Layer configurations
        self.layer_configs = {}

    def add_layer(
        self,
        name: str,
        color: str = "black",
        stroke_width: float = 0.5,
        opacity: float = 1.0
    ):
        """
        Add a new layer to the composition.

        Args:
            name: Layer name
            color: Stroke color
            stroke_width: Stroke width
            opacity: Layer opacity (0-1)
        """
        self.canvas.create_layer(name, color, stroke_width)
        self.layer_configs[name] = {
            "color": color,
            "stroke_width": stroke_width,
            "opacity": opacity
        }
        return name

    def add_pattern(self, pattern, layer: str, **kwargs):
        """
        Add a pattern to a specific layer.

        Args:
            pattern: Pattern object with a draw() method
            layer: Target layer name
            **kwargs: Additional arguments to pass to pattern.draw()
        """
        if layer not in self.layer_configs:
            raise ValueError(f"Layer '{layer}' does not exist. Create it with add_layer() first.")

        self.canvas.set_layer(layer)
        pattern.draw(self.canvas, layer, **kwargs)

    def save(self, filename: str):
        """
        Save the composition to an SVG file.

        Args:
            filename: Output filename
        """
        self.canvas.save(filename)

    def get_canvas(self) -> SVGCanvas:
        """Get the underlying SVGCanvas for direct manipulation."""
        return self.canvas


class ColorPalette:
    """
    Predefined color palettes for pen plotting.

    Provides curated color combinations suitable for AxiDraw
    with selective coloring (mostly black + accent colors).
    """

    # Classic black and white
    MONO = {
        "background": "white",
        "primary": "black"
    }

    # Black with red accent
    RED_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#D32F2F"
    }

    # Black with blue accent
    BLUE_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#1976D2"
    }

    # Black with gold accent
    GOLD_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#F9A825"
    }

    # Black with green accent
    GREEN_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#388E3C"
    }

    # Black with purple accent
    PURPLE_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#7B1FA2"
    }

    # Black with orange accent
    ORANGE_ACCENT = {
        "background": "white",
        "primary": "black",
        "accent": "#F57C00"
    }

    # Dual accent: red and blue
    DUAL_RED_BLUE = {
        "background": "white",
        "primary": "black",
        "accent1": "#D32F2F",
        "accent2": "#1976D2"
    }

    # Dual accent: gold and teal
    DUAL_GOLD_TEAL = {
        "background": "white",
        "primary": "black",
        "accent1": "#F9A825",
        "accent2": "#00897B"
    }

    # Sepia tones
    SEPIA = {
        "background": "#FFF8E7",
        "primary": "#3E2723",
        "accent": "#8D6E63"
    }


def create_standard_composition(
    width: float = 297,
    height: float = 210,
    palette: Dict[str, str] = None
) -> Composition:
    """
    Create a composition with standard layer setup.

    Creates a composition with predefined layers for common use cases:
    - background: Background elements
    - primary: Main pattern layer (black)
    - accent1: First accent color layer
    - accent2: Second accent color layer (if available)

    Args:
        width: Canvas width
        height: Canvas height
        palette: Color palette dictionary (uses MONO if None)

    Returns:
        Configured Composition object
    """
    if palette is None:
        palette = ColorPalette.MONO

    comp = Composition(width, height, palette.get("background", "white"))

    # Add standard layers
    comp.add_layer("background", color=palette.get("primary", "black"), stroke_width=0.3)
    comp.add_layer("primary", color=palette.get("primary", "black"), stroke_width=0.5)

    if "accent" in palette:
        comp.add_layer("accent", color=palette["accent"], stroke_width=0.5)

    if "accent1" in palette:
        comp.add_layer("accent1", color=palette["accent1"], stroke_width=0.5)

    if "accent2" in palette:
        comp.add_layer("accent2", color=palette["accent2"], stroke_width=0.5)

    return comp
