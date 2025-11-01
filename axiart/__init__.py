"""AxiArt - Generative art system for AxiDraw V3 pen plotter."""

from .svg_exporter import SVGCanvas
from .composition import Composition
from . import shapes

__version__ = "0.1.0"
__all__ = ["SVGCanvas", "Composition", "shapes"]
