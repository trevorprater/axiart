"""Grid pattern generator for square and hexagonal grids."""

import numpy as np
from typing import List, Tuple, Optional, Callable
from ..svg_exporter import SVGCanvas


class GridPattern:
    """
    Generate geometric grid structures.

    Supports square grids, hexagonal grids, and variations with
    distortions, randomness, and custom transformations.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        grid_type: str = "square"  # square, hexagonal, triangular
    ):
        """
        Initialize the grid pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            grid_type: Type of grid (square, hexagonal, triangular)
        """
        self.width = width
        self.height = height
        self.grid_type = grid_type
        self.lines = []
        self.cells = []

    def generate_square_grid(
        self,
        cell_size: float = 10,
        offset: Tuple[float, float] = (0, 0),
        draw_horizontal: bool = True,
        draw_vertical: bool = True,
        jitter: float = 0  # Random displacement
    ):
        """
        Generate a square grid.

        Args:
            cell_size: Size of grid cells
            offset: Grid offset (x, y)
            draw_horizontal: Draw horizontal lines
            draw_vertical: Draw vertical lines
            jitter: Random jitter amount (0 = perfect grid)
        """
        offset_x, offset_y = offset

        # Horizontal lines
        if draw_horizontal:
            y = offset_y
            while y <= self.height:
                points = []
                x = offset_x
                while x <= self.width:
                    jitter_x = np.random.uniform(-jitter, jitter) if jitter > 0 else 0
                    jitter_y = np.random.uniform(-jitter, jitter) if jitter > 0 else 0
                    points.append((x + jitter_x, y + jitter_y))
                    x += cell_size / 10  # Subdivide for smoother jittered lines

                if len(points) > 1:
                    self.lines.append(points)

                y += cell_size

        # Vertical lines
        if draw_vertical:
            x = offset_x
            while x <= self.width:
                points = []
                y = offset_y
                while y <= self.height:
                    jitter_x = np.random.uniform(-jitter, jitter) if jitter > 0 else 0
                    jitter_y = np.random.uniform(-jitter, jitter) if jitter > 0 else 0
                    points.append((x + jitter_x, y + jitter_y))
                    y += cell_size / 10

                if len(points) > 1:
                    self.lines.append(points)

                x += cell_size

    def generate_hexagonal_grid(
        self,
        cell_size: float = 10,
        offset: Tuple[float, float] = (0, 0),
        fill_cells: bool = False
    ):
        """
        Generate a hexagonal grid.

        Args:
            cell_size: Size of hexagonal cells
            offset: Grid offset (x, y)
            fill_cells: Whether to draw complete hexagon cells
        """
        offset_x, offset_y = offset

        # Hexagon geometry
        width = cell_size * 2
        height = np.sqrt(3) * cell_size
        horiz_spacing = width * 0.75
        vert_spacing = height

        row = 0
        y = offset_y

        while y - cell_size <= self.height:
            x = offset_x
            if row % 2 == 1:
                x += horiz_spacing / 2

            col = 0
            while x - cell_size <= self.width:
                if fill_cells:
                    # Draw complete hexagon
                    hexagon = self._create_hexagon(x, y, cell_size)
                    self.cells.append(hexagon)
                else:
                    # Just store center point for later use
                    self.cells.append([(x, y)])

                x += horiz_spacing
                col += 1

            y += vert_spacing
            row += 1

    def _create_hexagon(
        self,
        center_x: float,
        center_y: float,
        size: float
    ) -> List[Tuple[float, float]]:
        """Create a hexagon polygon."""
        points = []
        for i in range(6):
            angle = np.pi / 3 * i - np.pi / 2  # Start from top
            x = center_x + size * np.cos(angle)
            y = center_y + size * np.sin(angle)
            points.append((x, y))
        points.append(points[0])  # Close the hexagon
        return points

    def generate_triangular_grid(
        self,
        cell_size: float = 10,
        offset: Tuple[float, float] = (0, 0)
    ):
        """
        Generate a triangular grid.

        Args:
            cell_size: Size of triangular cells
            offset: Grid offset (x, y)
        """
        offset_x, offset_y = offset

        height = cell_size * np.sqrt(3) / 2
        row = 0
        y = offset_y

        while y <= self.height + height:
            x = offset_x
            col = 0

            while x <= self.width + cell_size:
                # Determine triangle orientation
                pointing_up = (row + col) % 2 == 0

                if pointing_up:
                    triangle = [
                        (x, y + height),
                        (x + cell_size / 2, y),
                        (x + cell_size, y + height),
                        (x, y + height)
                    ]
                else:
                    triangle = [
                        (x, y),
                        (x + cell_size, y),
                        (x + cell_size / 2, y + height),
                        (x, y)
                    ]

                self.cells.append(triangle)

                x += cell_size / 2
                col += 1

            y += height
            row += 1

    def apply_distortion(
        self,
        distortion_fn: Callable[[float, float], Tuple[float, float]]
    ):
        """
        Apply a custom distortion function to the grid.

        Args:
            distortion_fn: Function that takes (x, y) and returns (new_x, new_y)
        """
        # Apply to lines
        distorted_lines = []
        for line in self.lines:
            distorted_line = [distortion_fn(x, y) for x, y in line]
            distorted_lines.append(distorted_line)
        self.lines = distorted_lines

        # Apply to cells
        distorted_cells = []
        for cell in self.cells:
            distorted_cell = [distortion_fn(x, y) for x, y in cell]
            distorted_cells.append(distorted_cell)
        self.cells = distorted_cells

    def apply_radial_distortion(
        self,
        center: Optional[Tuple[float, float]] = None,
        strength: float = 0.1
    ):
        """
        Apply radial distortion (bulge/pinch effect).

        Args:
            center: Center of distortion (uses canvas center if None)
            strength: Distortion strength (positive = bulge, negative = pinch)
        """
        if center is None:
            center = (self.width / 2, self.height / 2)

        cx, cy = center
        max_dist = np.sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)

        def radial_fn(x, y):
            dx = x - cx
            dy = y - cy
            dist = np.sqrt(dx ** 2 + dy ** 2)

            if dist < 0.001:
                return x, y

            # Apply radial distortion
            factor = 1 + strength * (dist / max_dist)
            new_x = cx + dx * factor
            new_y = cy + dy * factor

            return new_x, new_y

        self.apply_distortion(radial_fn)

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the grid pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        # Draw lines
        for line in self.lines:
            if len(line) > 1:
                canvas.add_polyline(line, layer=layer)

        # Draw cells
        for cell in self.cells:
            if len(cell) > 1:
                canvas.add_polyline(cell, layer=layer, close=True)

    def get_lines(self) -> List[List[Tuple[float, float]]]:
        """Get all grid lines."""
        return [line.copy() for line in self.lines]

    def get_cells(self) -> List[List[Tuple[float, float]]]:
        """Get all grid cells."""
        return [cell.copy() for cell in self.cells]
