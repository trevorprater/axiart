"""Flow field pattern generator using vector fields and particle systems."""

import numpy as np
from noise import pnoise2
from typing import List, Tuple, Optional, Callable
from ..svg_exporter import SVGCanvas


class FlowFieldPattern:
    """
    Generate flow field patterns using vector fields.

    Creates organic, flowing patterns by tracing particles through
    a vector field, which can be based on Perlin noise, mathematical
    functions, or custom field definitions.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        field_type: str = "noise",  # noise, radial, spiral, custom
        scale: float = 50.0,
        seed: Optional[int] = None
    ):
        """
        Initialize the flow field pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            field_type: Type of vector field
            scale: Field scale (affects flow smoothness)
            seed: Random seed for noise-based fields
        """
        self.width = width
        self.height = height
        self.field_type = field_type
        self.scale = scale
        self.seed = seed if seed is not None else np.random.randint(0, 10000)

        self.paths = []
        self.custom_field_fn = None

    def set_custom_field(self, field_fn: Callable[[float, float], Tuple[float, float]]):
        """
        Set a custom vector field function.

        Args:
            field_fn: Function that takes (x, y) and returns (dx, dy) vector
        """
        self.custom_field_fn = field_fn

    def _get_field_vector(self, x: float, y: float) -> Tuple[float, float]:
        """
        Get the vector field value at a position.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tuple of (dx, dy) vector components
        """
        if self.field_type == "noise":
            # Use Perlin noise to determine angle
            noise_val = pnoise2(
                x / self.scale,
                y / self.scale,
                octaves=4,
                persistence=0.5,
                lacunarity=2.0,
                base=self.seed
            )
            angle = noise_val * np.pi * 4  # Map to angle

            dx = np.cos(angle)
            dy = np.sin(angle)
            return dx, dy

        elif self.field_type == "radial":
            # Radial field from center
            cx, cy = self.width / 2, self.height / 2
            dx = x - cx
            dy = y - cy
            dist = np.sqrt(dx ** 2 + dy ** 2)

            if dist < 0.001:
                return 0, 0

            # Normalize and optionally add rotation
            return dx / dist, dy / dist

        elif self.field_type == "spiral":
            # Spiral field
            cx, cy = self.width / 2, self.height / 2
            dx = x - cx
            dy = y - cy

            # Rotate 90 degrees and normalize
            magnitude = np.sqrt(dx ** 2 + dy ** 2) + 0.001
            return -dy / magnitude, dx / magnitude

        elif self.field_type == "waves":
            # Wave-based field
            freq = 2 * np.pi / self.scale
            dx = np.sin(y * freq)
            dy = np.cos(x * freq)
            return dx, dy

        elif self.field_type == "custom" and self.custom_field_fn:
            return self.custom_field_fn(x, y)

        else:
            return 0, 0

    def generate_streamlines(
        self,
        num_lines: int = 100,
        steps: int = 200,
        step_size: float = 1.0,
        start_positions: Optional[List[Tuple[float, float]]] = None
    ):
        """
        Generate streamlines by tracing particles through the vector field.

        Args:
            num_lines: Number of streamlines to generate
            steps: Number of steps per streamline
            step_size: Step size for integration
            start_positions: Custom starting positions (random if None)
        """
        if start_positions is None:
            # Generate random starting positions
            start_positions = [
                (np.random.uniform(0, self.width), np.random.uniform(0, self.height))
                for _ in range(num_lines)
            ]

        for start_pos in start_positions:
            path = [start_pos]
            x, y = start_pos

            for _ in range(steps):
                # Get vector field at current position
                dx, dy = self._get_field_vector(x, y)

                # Update position
                x += dx * step_size
                y += dy * step_size

                # Check bounds
                if x < 0 or x > self.width or y < 0 or y > self.height:
                    break

                path.append((x, y))

                # Check if path is too short (stuck)
                if len(path) > 5:
                    # Check if we're moving
                    recent_dist = np.sqrt(
                        (path[-1][0] - path[-5][0]) ** 2 +
                        (path[-1][1] - path[-5][1]) ** 2
                    )
                    if recent_dist < step_size * 2:
                        break

            if len(path) > 2:
                self.paths.append(path)

    def generate_particle_system(
        self,
        num_particles: int = 50,
        steps: int = 300,
        step_size: float = 0.8,
        fade_length: int = 50
    ):
        """
        Generate particle trails with fading effect.

        Args:
            num_particles: Number of particles
            steps: Number of steps to simulate
            step_size: Step size
            fade_length: Length of visible trail
        """
        # Initialize particles at random positions
        particles = [
            (np.random.uniform(0, self.width), np.random.uniform(0, self.height))
            for _ in range(num_particles)
        ]

        # Store all particle trails
        trails = [[] for _ in range(num_particles)]

        for step in range(steps):
            for i, (x, y) in enumerate(particles):
                # Get vector field
                dx, dy = self._get_field_vector(x, y)

                # Update position
                new_x = x + dx * step_size
                new_y = y + dy * step_size

                # Wrap or respawn if out of bounds
                if new_x < 0 or new_x > self.width or new_y < 0 or new_y > self.height:
                    new_x = np.random.uniform(0, self.width)
                    new_y = np.random.uniform(0, self.height)
                    trails[i] = []  # Clear trail

                particles[i] = (new_x, new_y)
                trails[i].append((new_x, new_y))

                # Limit trail length
                if len(trails[i]) > fade_length:
                    trails[i] = trails[i][-fade_length:]

                # Add trail segments as paths
                if len(trails[i]) > 1 and step % 10 == 0:  # Save every 10 steps
                    self.paths.append(trails[i].copy())

    def generate_grid_visualization(
        self,
        grid_spacing: float = 10.0,
        arrow_length: float = 5.0
    ):
        """
        Generate a grid visualization of the vector field.

        Args:
            grid_spacing: Spacing between grid points
            arrow_length: Length of arrow indicators
        """
        x = 0
        while x <= self.width:
            y = 0
            while y <= self.height:
                # Get field vector
                dx, dy = self._get_field_vector(x, y)

                # Normalize and scale
                magnitude = np.sqrt(dx ** 2 + dy ** 2) + 0.001
                dx = (dx / magnitude) * arrow_length
                dy = (dy / magnitude) * arrow_length

                # Create arrow
                end_x = x + dx
                end_y = y + dy

                # Arrow line
                arrow = [(x, y), (end_x, end_y)]
                self.paths.append(arrow)

                # Arrow head (small)
                head_size = arrow_length * 0.3
                angle = np.arctan2(dy, dx)

                left_angle = angle + 2.5
                right_angle = angle - 2.5

                left_x = end_x - head_size * np.cos(left_angle)
                left_y = end_y - head_size * np.sin(left_angle)
                right_x = end_x - head_size * np.cos(right_angle)
                right_y = end_y - head_size * np.sin(right_angle)

                self.paths.append([(end_x, end_y), (left_x, left_y)])
                self.paths.append([(end_x, end_y), (right_x, right_y)])

                y += grid_spacing
            x += grid_spacing

    def generate_curl_noise_lines(
        self,
        num_lines: int = 100,
        steps: int = 200,
        step_size: float = 1.0
    ):
        """
        Generate lines using curl noise (divergence-free noise field).

        Args:
            num_lines: Number of lines
            steps: Steps per line
            step_size: Step size
        """
        for _ in range(num_lines):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(0, self.height)

            path = [(x, y)]

            for _ in range(steps):
                # Compute curl of noise field
                epsilon = 0.1
                noise_x_plus = pnoise2((x + epsilon) / self.scale, y / self.scale, base=self.seed)
                noise_x_minus = pnoise2((x - epsilon) / self.scale, y / self.scale, base=self.seed)
                noise_y_plus = pnoise2(x / self.scale, (y + epsilon) / self.scale, base=self.seed)
                noise_y_minus = pnoise2(x / self.scale, (y - epsilon) / self.scale, base=self.seed)

                # Curl computation
                dx = (noise_y_plus - noise_y_minus) / (2 * epsilon)
                dy = -(noise_x_plus - noise_x_minus) / (2 * epsilon)

                # Move particle
                x += dx * step_size
                y += dy * step_size

                if x < 0 or x > self.width or y < 0 or y > self.height:
                    break

                path.append((x, y))

            if len(path) > 2:
                self.paths.append(path)

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the flow field pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        for path in self.paths:
            if len(path) > 1:
                canvas.add_polyline(path, layer=layer)

    def get_paths(self) -> List[List[Tuple[float, float]]]:
        """Get all flow field paths."""
        return [path.copy() for path in self.paths]
