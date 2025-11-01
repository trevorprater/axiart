"""Spiral and concentric circle pattern generator."""

import numpy as np
from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas


class SpiralPattern:
    """
    Generate concentric circles and spiral patterns.

    Supports various spiral types including Archimedean spirals,
    logarithmic spirals, and concentric circles with customizable
    rotation and decay.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        center: Optional[Tuple[float, float]] = None,
        num_revolutions: int = 20,
        points_per_revolution: int = 100,
        spiral_type: str = "archimedean"  # archimedean, logarithmic, concentric
    ):
        """
        Initialize the spiral pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            center: Center point (uses canvas center if None)
            num_revolutions: Number of spiral revolutions
            points_per_revolution: Points per revolution (resolution)
            spiral_type: Type of spiral (archimedean, logarithmic, concentric)
        """
        self.width = width
        self.height = height
        self.center = center if center else (width / 2, height / 2)
        self.num_revolutions = num_revolutions
        self.points_per_revolution = points_per_revolution
        self.spiral_type = spiral_type

        self.spirals = []

    def generate(
        self,
        start_radius: float = 5,
        end_radius: Optional[float] = None,
        rotation_offset: float = 0,
        growth_factor: float = 1.0,
        num_spirals: int = 1,
        angular_offset: float = 0
    ):
        """
        Generate spiral pattern.

        Args:
            start_radius: Starting radius
            end_radius: Ending radius (uses max if None)
            rotation_offset: Rotation offset in radians
            growth_factor: Growth rate for spirals
            num_spirals: Number of parallel spirals
            angular_offset: Angular offset between spirals
        """
        if end_radius is None:
            # Calculate maximum radius that fits in canvas
            end_radius = min(self.center[0], self.center[1],
                           self.width - self.center[0],
                           self.height - self.center[1]) * 0.9

        total_points = self.num_revolutions * self.points_per_revolution

        for spiral_idx in range(num_spirals):
            points = []
            offset_angle = angular_offset * spiral_idx

            for i in range(total_points):
                # Calculate angle
                theta = (i / self.points_per_revolution) * 2 * np.pi + rotation_offset + offset_angle

                # Calculate radius based on spiral type
                t = i / total_points  # normalized parameter [0, 1]

                if self.spiral_type == "archimedean":
                    # Linear growth
                    r = start_radius + (end_radius - start_radius) * t * growth_factor

                elif self.spiral_type == "logarithmic":
                    # Exponential growth
                    a = start_radius
                    b = np.log(end_radius / start_radius) / (self.num_revolutions * 2 * np.pi)
                    r = a * np.exp(b * theta * growth_factor)

                elif self.spiral_type == "concentric":
                    # Concentric circles
                    revolution = int(i / self.points_per_revolution)
                    r = start_radius + (end_radius - start_radius) * (revolution / self.num_revolutions) * growth_factor

                else:
                    raise ValueError(f"Unknown spiral type: {self.spiral_type}")

                # Convert to Cartesian coordinates
                x = self.center[0] + r * np.cos(theta)
                y = self.center[1] + r * np.sin(theta)

                points.append((x, y))

            self.spirals.append(points)

    def generate_circular_waves(
        self,
        num_circles: int = 20,
        start_radius: float = 10,
        end_radius: Optional[float] = None,
        points_per_circle: int = 100,
        wave_amplitude: float = 0,
        wave_frequency: float = 5
    ):
        """
        Generate concentric circular waves with optional undulation.

        Args:
            num_circles: Number of concentric circles
            start_radius: Starting radius
            end_radius: Ending radius
            points_per_circle: Points per circle
            wave_amplitude: Amplitude of waves (0 for perfect circles)
            wave_frequency: Frequency of waves
        """
        if end_radius is None:
            end_radius = min(self.center[0], self.center[1],
                           self.width - self.center[0],
                           self.height - self.center[1]) * 0.9

        for circle_idx in range(num_circles):
            points = []
            base_radius = start_radius + (end_radius - start_radius) * (circle_idx / num_circles)

            for i in range(points_per_circle + 1):  # +1 to close the circle
                theta = (i / points_per_circle) * 2 * np.pi

                # Add wave modulation
                r = base_radius + wave_amplitude * np.sin(wave_frequency * theta)

                x = self.center[0] + r * np.cos(theta)
                y = self.center[1] + r * np.sin(theta)

                points.append((x, y))

            self.spirals.append(points)

    def generate_fermat_spiral(
        self,
        num_points: int = 1000,
        spacing: float = 2.0,
        rotation: float = 0
    ):
        """
        Generate a Fermat (parabolic) spiral pattern.

        Args:
            num_points: Number of points
            spacing: Spacing between points
            rotation: Rotation offset
        """
        points = []
        golden_angle = np.pi * (3 - np.sqrt(5))  # Golden angle in radians

        for i in range(num_points):
            theta = i * golden_angle + rotation
            r = spacing * np.sqrt(i)

            x = self.center[0] + r * np.cos(theta)
            y = self.center[1] + r * np.sin(theta)

            # Only add if within bounds
            if 0 <= x <= self.width and 0 <= y <= self.height:
                points.append((x, y))

        self.spirals.append(points)

    def draw(self, canvas: SVGCanvas, layer: str, as_points: bool = False):
        """
        Draw the spiral pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
            as_points: Draw as points instead of lines
        """
        for spiral_points in self.spirals:
            if as_points:
                canvas.add_points(spiral_points, layer=layer)
            else:
                if len(spiral_points) > 1:
                    canvas.add_polyline(spiral_points, layer=layer)

    def get_spirals(self) -> List[List[Tuple[float, float]]]:
        """Get all spiral point lists."""
        return [spiral.copy() for spiral in self.spirals]
