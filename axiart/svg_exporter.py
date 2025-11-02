"""SVG Canvas and exporter for pen plotters."""

import svgwrite
from typing import List, Tuple, Optional, Union


class SVGCanvas:
    """
    A canvas for creating SVG artwork optimized for pen plotters.

    Supports multiple layers, selective coloring, and clean vector output.
    """

    def __init__(
        self,
        width: float = 297,  # A4 width in mm
        height: float = 210,  # A4 height in mm
        background: str = "white",
        units: str = "mm"
    ):
        """
        Initialize the SVG canvas.

        Args:
            width: Canvas width in specified units
            height: Canvas height in specified units
            background: Background color
            units: Unit of measurement (mm, px, etc.)
        """
        self.width = width
        self.height = height
        self.background = background
        self.units = units

        # Create SVG drawing
        self.dwg = svgwrite.Drawing(
            size=(f"{width}{units}", f"{height}{units}"),
            viewBox=f"0 0 {width} {height}"
        )

        # Add background
        if background != "none":
            self.dwg.add(self.dwg.rect(
                insert=(0, 0),
                size=(f"{width}{units}", f"{height}{units}"),
                fill=background
            ))

        # Layers for organizing content
        self.layers = {}
        self.current_layer = None

    def create_layer(self, name: str, color: str = "black", stroke_width: float = 0.5):
        """
        Create a new drawing layer.

        Args:
            name: Layer name
            color: Default stroke color for this layer
            stroke_width: Default stroke width for this layer
        """
        group = self.dwg.g(id=name, stroke=color, fill="none", stroke_width=stroke_width)
        self.layers[name] = {
            "group": group,
            "color": color,
            "stroke_width": stroke_width
        }
        self.dwg.add(group)
        return name

    def set_layer(self, name: str):
        """Set the current active layer."""
        if name not in self.layers:
            raise ValueError(f"Layer '{name}' does not exist")
        self.current_layer = name

    def add_polyline(
        self,
        points: List[Tuple[float, float]],
        layer: Optional[str] = None,
        color: Optional[str] = None,
        stroke_width: Optional[float] = None,
        close: bool = False
    ):
        """
        Add a polyline to the canvas.

        Args:
            points: List of (x, y) coordinate tuples
            layer: Target layer (uses current layer if None)
            color: Stroke color (uses layer default if None)
            stroke_width: Stroke width (uses layer default if None)
            close: Whether to close the path
        """
        if not points:
            return

        target_layer = layer or self.current_layer
        if target_layer is None:
            raise ValueError("No layer specified and no current layer set")

        layer_info = self.layers[target_layer]
        stroke_color = color or layer_info["color"]
        width = stroke_width if stroke_width is not None else layer_info["stroke_width"]

        if close:
            shape = self.dwg.polygon(
                points=points,
                stroke=stroke_color,
                fill="none",
                stroke_width=width
            )
        else:
            shape = self.dwg.polyline(
                points=points,
                stroke=stroke_color,
                fill="none",
                stroke_width=width
            )

        layer_info["group"].add(shape)

    def add_line(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        layer: Optional[str] = None,
        color: Optional[str] = None,
        stroke_width: Optional[float] = None
    ):
        """
        Add a line to the canvas.

        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            layer: Target layer
            color: Stroke color
            stroke_width: Stroke width
        """
        target_layer = layer or self.current_layer
        if target_layer is None:
            raise ValueError("No layer specified and no current layer set")

        layer_info = self.layers[target_layer]
        stroke_color = color or layer_info["color"]
        width = stroke_width if stroke_width is not None else layer_info["stroke_width"]

        line = self.dwg.line(
            start=start,
            end=end,
            stroke=stroke_color,
            stroke_width=width
        )
        layer_info["group"].add(line)

    def add_circle(
        self,
        center: Tuple[float, float],
        radius: float,
        layer: Optional[str] = None,
        color: Optional[str] = None,
        stroke_width: Optional[float] = None,
        fill: str = "none"
    ):
        """
        Add a circle to the canvas.

        Args:
            center: Center point (x, y)
            radius: Circle radius
            layer: Target layer
            color: Stroke color
            stroke_width: Stroke width
            fill: Fill color
        """
        target_layer = layer or self.current_layer
        if target_layer is None:
            raise ValueError("No layer specified and no current layer set")

        layer_info = self.layers[target_layer]
        stroke_color = color or layer_info["color"]
        width = stroke_width if stroke_width is not None else layer_info["stroke_width"]

        circle = self.dwg.circle(
            center=center,
            r=radius,
            stroke=stroke_color,
            stroke_width=width,
            fill=fill
        )
        layer_info["group"].add(circle)

    def add_path(
        self,
        path_data: str,
        layer: Optional[str] = None,
        color: Optional[str] = None,
        stroke_width: Optional[float] = None
    ):
        """
        Add an SVG path to the canvas.

        Args:
            path_data: SVG path data string
            layer: Target layer
            color: Stroke color
            stroke_width: Stroke width
        """
        target_layer = layer or self.current_layer
        if target_layer is None:
            raise ValueError("No layer specified and no current layer set")

        layer_info = self.layers[target_layer]
        stroke_color = color or layer_info["color"]
        width = stroke_width if stroke_width is not None else layer_info["stroke_width"]

        path = self.dwg.path(
            d=path_data,
            stroke=stroke_color,
            stroke_width=width,
            fill="none"
        )
        layer_info["group"].add(path)

    def add_points(
        self,
        points: List[Tuple[float, float]],
        layer: Optional[str] = None,
        color: Optional[str] = None,
        radius: float = 0.3
    ):
        """
        Add stippled points (small circles) for texture effects.

        Args:
            points: List of (x, y) coordinate tuples
            layer: Target layer
            color: Fill color for points
            radius: Point radius
        """
        target_layer = layer or self.current_layer
        if target_layer is None:
            raise ValueError("No layer specified and no current layer set")

        layer_info = self.layers[target_layer]
        fill_color = color or layer_info["color"]

        for point in points:
            circle = self.dwg.circle(
                center=point,
                r=radius,
                fill=fill_color,
                stroke="none"
            )
            layer_info["group"].add(circle)

    def save(self, filename: str):
        """
        Save the SVG to a file.

        Args:
            filename: Output filename
        """
        self.dwg.saveas(filename)
        print(f"SVG saved to {filename}")
