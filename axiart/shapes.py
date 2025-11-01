"""Geometric shape utilities for artistic compositions."""

from typing import List, Tuple, Optional
import numpy as np


class Shape:
    """Base class for geometric shapes."""

    def __init__(self):
        self.points = []

    def get_points(self) -> List[Tuple[float, float]]:
        """Get the shape's points."""
        return self.points.copy()


class Rectangle(Shape):
    """Create a rectangle shape."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rotation: float = 0
    ):
        """
        Create a rectangle.

        Args:
            x: Left x coordinate
            y: Top y coordinate
            width: Rectangle width
            height: Rectangle height
            rotation: Rotation in degrees
        """
        super().__init__()

        # Create rectangle points
        corners = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
            (x, y)  # Close the shape
        ]

        if rotation != 0:
            # Rotate around center
            cx = x + width / 2
            cy = y + height / 2
            rad = np.radians(rotation)
            cos_r = np.cos(rad)
            sin_r = np.sin(rad)

            rotated = []
            for px, py in corners:
                # Translate to origin
                px -= cx
                py -= cy
                # Rotate
                new_x = px * cos_r - py * sin_r
                new_y = px * sin_r + py * cos_r
                # Translate back
                rotated.append((new_x + cx, new_y + cy))

            self.points = rotated
        else:
            self.points = corners


class Polygon(Shape):
    """Create a polygon from points."""

    def __init__(self, points: List[Tuple[float, float]], close: bool = True):
        """
        Create a polygon.

        Args:
            points: List of (x, y) points
            close: Whether to close the polygon
        """
        super().__init__()
        self.points = points.copy()
        if close and self.points[0] != self.points[-1]:
            self.points.append(self.points[0])


class Circle(Shape):
    """Create a circle as a polygon approximation."""

    def __init__(
        self,
        center: Tuple[float, float],
        radius: float,
        num_points: int = 64
    ):
        """
        Create a circle.

        Args:
            center: Center point (x, y)
            radius: Circle radius
            num_points: Number of points in polygon approximation
        """
        super().__init__()

        cx, cy = center
        points = []

        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * np.pi
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append((x, y))

        self.points = points


class Ellipse(Shape):
    """Create an ellipse as a polygon approximation."""

    def __init__(
        self,
        center: Tuple[float, float],
        radius_x: float,
        radius_y: float,
        rotation: float = 0,
        num_points: int = 64
    ):
        """
        Create an ellipse.

        Args:
            center: Center point (x, y)
            radius_x: Horizontal radius
            radius_y: Vertical radius
            rotation: Rotation in degrees
            num_points: Number of points in polygon approximation
        """
        super().__init__()

        cx, cy = center
        rad = np.radians(rotation)
        cos_r = np.cos(rad)
        sin_r = np.sin(rad)
        points = []

        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * np.pi
            # Point on unrotated ellipse
            x = radius_x * np.cos(angle)
            y = radius_y * np.sin(angle)

            # Rotate
            rx = x * cos_r - y * sin_r
            ry = x * sin_r + y * cos_r

            # Translate to center
            points.append((cx + rx, cy + ry))

        self.points = points


class Star(Shape):
    """Create a star shape."""

    def __init__(
        self,
        center: Tuple[float, float],
        outer_radius: float,
        inner_radius: float,
        num_points: int = 5
    ):
        """
        Create a star.

        Args:
            center: Center point (x, y)
            outer_radius: Outer radius (point tips)
            inner_radius: Inner radius (valleys)
            num_points: Number of star points
        """
        super().__init__()

        cx, cy = center
        points = []

        for i in range(num_points * 2 + 1):
            angle = (i / (num_points * 2)) * 2 * np.pi - np.pi / 2
            radius = outer_radius if i % 2 == 0 else inner_radius

            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append((x, y))

        self.points = points


class Wave(Shape):
    """Create a wavy line."""

    def __init__(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        amplitude: float,
        frequency: float,
        num_points: int = 100
    ):
        """
        Create a wavy line.

        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            amplitude: Wave amplitude
            frequency: Wave frequency
            num_points: Number of points
        """
        super().__init__()

        sx, sy = start
        ex, ey = end
        dx = ex - sx
        dy = ey - sy
        length = np.sqrt(dx ** 2 + dy ** 2)

        # Direction vector
        dir_x = dx / length if length > 0 else 0
        dir_y = dy / length if length > 0 else 0

        # Perpendicular vector
        perp_x = -dir_y
        perp_y = dir_x

        points = []
        for i in range(num_points + 1):
            t = i / num_points
            # Position along line
            base_x = sx + t * dx
            base_y = sy + t * dy

            # Wave offset
            wave = amplitude * np.sin(frequency * 2 * np.pi * t)
            x = base_x + wave * perp_x
            y = base_y + wave * perp_y

            points.append((x, y))

        self.points = points


def add_filled_shape(
    canvas,
    shape: Shape,
    fill_color: str,
    stroke_color: Optional[str] = None,
    stroke_width: float = 0.5
):
    """
    Add a filled shape to the canvas.

    Args:
        canvas: SVGCanvas object
        shape: Shape object
        fill_color: Fill color
        stroke_color: Stroke color (none if None)
        stroke_width: Stroke width
    """
    points = shape.get_points()

    if stroke_color:
        poly = canvas.dwg.polygon(
            points=points,
            fill=fill_color,
            stroke=stroke_color,
            stroke_width=stroke_width
        )
    else:
        poly = canvas.dwg.polygon(
            points=points,
            fill=fill_color,
            stroke="none"
        )

    canvas.dwg.add(poly)
