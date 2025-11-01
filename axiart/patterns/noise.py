"""Noise and texture field pattern generator using Perlin noise."""

import numpy as np
from noise import pnoise2
from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas


class NoisePattern:
    """
    Generate noise-based patterns including contour lines, stippling, and textures.

    Uses Perlin noise to create organic, natural-looking patterns
    including topographic-style contour lines and cellular textures.
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
            octaves: Number of noise octaves (detail level)
            persistence: Amplitude multiplier per octave
            lacunarity: Frequency multiplier per octave
            seed: Random seed for reproducibility
        """
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed if seed is not None else np.random.randint(0, 10000)

        self.contours = []
        self.points = []

    def _get_noise(self, x: float, y: float) -> float:
        """
        Get Perlin noise value at position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Noise value between -1 and 1
        """
        return pnoise2(
            x / self.scale,
            y / self.scale,
            octaves=self.octaves,
            persistence=self.persistence,
            lacunarity=self.lacunarity,
            base=self.seed
        )

    def generate_contour_lines(
        self,
        num_levels: int = 20,
        resolution: float = 2.0,
        min_value: float = -1.0,
        max_value: float = 1.0
    ):
        """
        Generate topographic-style contour lines.

        Args:
            num_levels: Number of contour levels
            resolution: Sampling resolution
            min_value: Minimum contour value
            max_value: Maximum contour value
        """
        # Create a grid of noise values
        x_samples = int(self.width / resolution)
        y_samples = int(self.height / resolution)

        noise_grid = np.zeros((y_samples, x_samples))

        for i in range(y_samples):
            for j in range(x_samples):
                x = j * resolution
                y = i * resolution
                noise_grid[i, j] = self._get_noise(x, y)

        # Generate contour levels
        levels = np.linspace(min_value, max_value, num_levels)

        # Simple marching squares implementation
        for level in levels:
            contour_segments = self._marching_squares(noise_grid, level, resolution)
            self.contours.extend(contour_segments)

    def _marching_squares(
        self,
        grid: np.ndarray,
        level: float,
        resolution: float
    ) -> List[List[Tuple[float, float]]]:
        """
        Simple marching squares algorithm for contour extraction.

        Args:
            grid: 2D array of noise values
            level: Contour level
            resolution: Grid resolution

        Returns:
            List of contour line segments
        """
        segments = []
        rows, cols = grid.shape

        for i in range(rows - 1):
            for j in range(cols - 1):
                # Get the four corners of the cell
                tl = grid[i, j]
                tr = grid[i, j + 1]
                bl = grid[i + 1, j]
                br = grid[i + 1, j + 1]

                # Determine cell configuration
                cell_value = 0
                if tl >= level:
                    cell_value |= 1
                if tr >= level:
                    cell_value |= 2
                if br >= level:
                    cell_value |= 4
                if bl >= level:
                    cell_value |= 8

                # Calculate interpolated edge positions
                x = j * resolution
                y = i * resolution

                # Edge midpoints (simplified - not interpolated)
                top = (x + resolution / 2, y)
                right = (x + resolution, y + resolution / 2)
                bottom = (x + resolution / 2, y + resolution)
                left = (x, y + resolution / 2)

                # Draw lines based on configuration
                if cell_value in [1, 14]:
                    segments.append([top, left])
                elif cell_value in [2, 13]:
                    segments.append([top, right])
                elif cell_value in [3, 12]:
                    segments.append([left, right])
                elif cell_value in [4, 11]:
                    segments.append([right, bottom])
                elif cell_value in [5]:
                    segments.append([top, left])
                    segments.append([right, bottom])
                elif cell_value in [6, 9]:
                    segments.append([top, bottom])
                elif cell_value in [7, 8]:
                    segments.append([left, bottom])
                elif cell_value in [10]:
                    segments.append([top, right])
                    segments.append([left, bottom])

        return segments

    def generate_stippling(
        self,
        num_points: int = 5000,
        density_map: bool = True,
        threshold: float = 0.0
    ):
        """
        Generate stippled texture using noise-based density.

        Args:
            num_points: Number of stipple points
            density_map: Use noise as density map
            threshold: Noise threshold for point placement
        """
        for _ in range(num_points):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)

            if density_map:
                noise_value = self._get_noise(x, y)
                # Only place point if noise is above threshold
                if noise_value > threshold:
                    self.points.append((x, y))
            else:
                self.points.append((x, y))

    def generate_cellular_texture(
        self,
        cell_size: float = 5.0,
        threshold: float = 0.0,
        pattern_type: str = "squares"  # squares, circles, hatching
    ):
        """
        Generate cellular texture based on noise values.

        Args:
            cell_size: Size of texture cells
            threshold: Noise threshold for drawing cells
            pattern_type: Type of cell pattern
        """
        x = 0
        while x < self.width:
            y = 0
            while y < self.height:
                noise_value = self._get_noise(x + cell_size / 2, y + cell_size / 2)

                if noise_value > threshold:
                    if pattern_type == "squares":
                        square = [
                            (x, y),
                            (x + cell_size, y),
                            (x + cell_size, y + cell_size),
                            (x, y + cell_size),
                            (x, y)
                        ]
                        self.contours.append(square)

                    elif pattern_type == "circles":
                        self.points.append((x + cell_size / 2, y + cell_size / 2))

                    elif pattern_type == "hatching":
                        # Diagonal hatching based on noise intensity
                        intensity = (noise_value + 1) / 2  # Normalize to [0, 1]
                        num_lines = int(intensity * 5)
                        for i in range(num_lines):
                            offset = i * (cell_size / 5)
                            line = [
                                (x + offset, y),
                                (x, y + offset)
                            ]
                            self.contours.append(line)

                y += cell_size
            x += cell_size

    def generate_hatching(
        self,
        line_spacing: float = 2.0,
        angle: float = 45.0,
        density_modulation: bool = True
    ):
        """
        Generate hatching pattern modulated by noise.

        Args:
            line_spacing: Base spacing between hatch lines
            angle: Hatch angle in degrees
            density_modulation: Modulate density based on noise
        """
        angle_rad = np.radians(angle)

        # Determine bounds
        diagonal = np.sqrt(self.width ** 2 + self.height ** 2)

        # Generate parallel lines
        num_lines = int(diagonal / line_spacing)

        for i in range(-num_lines, num_lines):
            offset = i * line_spacing

            # Line endpoints (extended beyond canvas)
            if abs(np.cos(angle_rad)) > 0.001:
                # Calculate line from left to right
                x1 = -diagonal
                y1 = offset - x1 * np.tan(angle_rad)
                x2 = self.width + diagonal
                y2 = offset - x2 * np.tan(angle_rad)
            else:
                # Vertical line
                x1 = x2 = offset
                y1 = -diagonal
                y2 = self.height + diagonal

            # Sample along the line and modulate based on noise
            if density_modulation:
                points = []
                num_samples = int(diagonal / 1.0)

                for t in np.linspace(0, 1, num_samples):
                    x = x1 + t * (x2 - x1)
                    y = y1 + t * (y2 - y1)

                    if 0 <= x <= self.width and 0 <= y <= self.height:
                        noise_value = self._get_noise(x, y)
                        # Only add point if noise is above threshold
                        if noise_value > -0.3:
                            points.append((x, y))
                        elif len(points) > 1:
                            # End current segment
                            self.contours.append(points)
                            points = []

                if len(points) > 1:
                    self.contours.append(points)
            else:
                # Simple line clipping to canvas bounds
                if (0 <= x1 <= self.width or 0 <= x2 <= self.width or
                    0 <= y1 <= self.height or 0 <= y2 <= self.height):
                    self.contours.append([(x1, y1), (x2, y2)])

    def draw(self, canvas: SVGCanvas, layer: str, draw_points_as_circles: bool = True):
        """
        Draw the noise pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
            draw_points_as_circles: Draw points as small circles
        """
        # Draw contour lines
        for contour in self.contours:
            if len(contour) > 1:
                canvas.add_polyline(contour, layer=layer)

        # Draw points
        if self.points:
            if draw_points_as_circles:
                canvas.add_points(self.points, layer=layer)
            else:
                # Draw as single pixel lines
                for point in self.points:
                    canvas.add_line(point, point, layer=layer)

    def get_contours(self) -> List[List[Tuple[float, float]]]:
        """Get all contour lines."""
        return [contour.copy() for contour in self.contours]

    def get_points(self) -> List[Tuple[float, float]]:
        """Get all stipple points."""
        return self.points.copy()
