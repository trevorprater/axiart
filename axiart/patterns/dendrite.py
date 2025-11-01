"""Dendrite and branching pattern generator using DLA (Diffusion-Limited Aggregation)."""

import numpy as np
from typing import List, Tuple, Optional
from ..svg_exporter import SVGCanvas

# Try to import Rust implementation for 100-300x speedup
try:
    from axiart_core import DendriteGenerator as _RustDendriteGenerator
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False


class DendritePattern:
    """
    Generate organic, tree-like or river-like branching structures.

    Uses a Diffusion-Limited Aggregation (DLA) algorithm to create
    natural-looking dendrite patterns.
    """

    def __init__(
        self,
        width: float = 297,
        height: float = 210,
        num_particles: int = 3000,
        attraction_distance: float = 5.0,
        min_move_distance: float = 2.0,
        seed_points: Optional[List[Tuple[float, float]]] = None,
        branching_style: str = "radial"  # radial, vertical, horizontal
    ):
        """
        Initialize the dendrite pattern generator.

        Args:
            width: Canvas width
            height: Canvas height
            num_particles: Number of particles to aggregate
            attraction_distance: Distance at which particles stick
            min_move_distance: Minimum distance particles move
            seed_points: Initial seed points (uses center if None)
            branching_style: Style of branching (radial, vertical, horizontal)
        """
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.attraction_distance = attraction_distance
        self.min_move_distance = min_move_distance
        self.branching_style = branching_style

        # Initialize seed points
        if seed_points is None:
            if branching_style == "vertical":
                # Start from bottom
                self.tree = [(width / 2, height)]
            elif branching_style == "horizontal":
                # Start from left
                self.tree = [(0, height / 2)]
            else:
                # Start from center
                self.tree = [(width / 2, height / 2)]
        else:
            self.tree = list(seed_points)

        self.lines = []

        # Use Rust implementation if available (100-300x faster)
        self._use_rust = _RUST_AVAILABLE
        if self._use_rust:
            self._rust_generator = _RustDendriteGenerator(
                width=width,
                height=height,
                num_particles=num_particles,
                attraction_distance=attraction_distance,
                min_move_distance=min_move_distance,
                seed_points=seed_points,
                branching_style=branching_style,
                seed=None,  # Can add seed parameter to __init__ if needed
            )

    def _get_random_particle_position(self) -> Tuple[float, float]:
        """Generate a random starting position for a particle."""
        if self.branching_style == "vertical":
            # Spawn from top
            return (np.random.uniform(0, self.width), 0)
        elif self.branching_style == "horizontal":
            # Spawn from right
            return (self.width, np.random.uniform(0, self.height))
        else:
            # Spawn from edges
            edge = np.random.randint(0, 4)
            if edge == 0:  # top
                return (np.random.uniform(0, self.width), 0)
            elif edge == 1:  # right
                return (self.width, np.random.uniform(0, self.height))
            elif edge == 2:  # bottom
                return (np.random.uniform(0, self.width), self.height)
            else:  # left
                return (0, np.random.uniform(0, self.height))

    def _random_walk(self, pos: Tuple[float, float]) -> Tuple[float, float]:
        """Perform a random walk step."""
        angle = np.random.uniform(0, 2 * np.pi)
        dx = np.cos(angle) * self.min_move_distance
        dy = np.sin(angle) * self.min_move_distance

        # Add slight bias towards center for radial, or towards seed direction
        if self.branching_style == "radial":
            center_x, center_y = self.width / 2, self.height / 2
            bias_x = (center_x - pos[0]) * 0.02
            bias_y = (center_y - pos[1]) * 0.02
            dx += bias_x
            dy += bias_y
        elif self.branching_style == "vertical":
            # Bias downward
            dy += self.min_move_distance * 0.3
        elif self.branching_style == "horizontal":
            # Bias leftward
            dx -= self.min_move_distance * 0.3

        new_x = np.clip(pos[0] + dx, 0, self.width)
        new_y = np.clip(pos[1] + dy, 0, self.height)

        return (new_x, new_y)

    def _find_nearest_point(self, pos: Tuple[float, float]) -> Tuple[Optional[int], float]:
        """Find the nearest point in the tree and its distance."""
        if not self.tree:
            return None, float('inf')

        tree_array = np.array(self.tree)
        distances = np.sqrt(
            (tree_array[:, 0] - pos[0]) ** 2 +
            (tree_array[:, 1] - pos[1]) ** 2
        )
        nearest_idx = np.argmin(distances)
        return nearest_idx, distances[nearest_idx]

    def generate(self, max_attempts: int = 1000):
        """
        Generate the dendrite pattern.

        Args:
            max_attempts: Maximum random walk attempts per particle
        """
        # Use Rust implementation if available
        if self._use_rust:
            points, lines = self._rust_generator.generate(max_attempts)
            self.tree = points
            self.lines = lines
            return

        # Fallback to Python implementation
        for particle_idx in range(self.num_particles):
            # Spawn a new particle
            particle_pos = self._get_random_particle_position()

            # Random walk until it sticks or exceeds max attempts
            for attempt in range(max_attempts):
                # Find nearest point in tree
                nearest_idx, distance = self._find_nearest_point(particle_pos)

                if distance < self.attraction_distance:
                    # Particle sticks to tree
                    nearest_point = self.tree[nearest_idx]
                    self.tree.append(particle_pos)
                    self.lines.append((nearest_point, particle_pos))
                    break

                # Continue random walk
                particle_pos = self._random_walk(particle_pos)

                # Check if particle went out of bounds (respawn)
                if (particle_pos[0] < 0 or particle_pos[0] > self.width or
                    particle_pos[1] < 0 or particle_pos[1] > self.height):
                    particle_pos = self._get_random_particle_position()

            # Progress indicator
            if (particle_idx + 1) % 500 == 0:
                print(f"Generated {particle_idx + 1}/{self.num_particles} particles")

    def draw(self, canvas: SVGCanvas, layer: str):
        """
        Draw the dendrite pattern on the canvas.

        Args:
            canvas: SVGCanvas to draw on
            layer: Layer name to draw on
        """
        for start, end in self.lines:
            canvas.add_line(start, end, layer=layer)

    def get_points(self) -> List[Tuple[float, float]]:
        """Get all aggregated points."""
        return self.tree.copy()

    def get_lines(self) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Get all lines in the dendrite structure."""
        return self.lines.copy()
