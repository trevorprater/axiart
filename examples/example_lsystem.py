#!/usr/bin/env python3
"""Example: L-Systems - Fractal Plants and Curves"""

import sys
sys.path.insert(0, '..')

from axiart import SVGCanvas
from axiart.patterns import LSystemPattern


def main():
    """Demonstrate L-System patterns."""

    # Create a canvas
    canvas = SVGCanvas(width=297, height=210, background="white")

    # Create layers
    canvas.create_layer("fractals", color="black", stroke_width=0.5)
    canvas.create_layer("plants", color="#2D5016", stroke_width=0.7)
    canvas.create_layer("curves", color="#4A90E2", stroke_width=0.6)

    # Example 1: Koch Snowflake (top left)
    koch = LSystemPattern(
        width=297,
        height=210,
        preset="koch_snowflake",
        iterations=4,
        step_length=2.0,
        start_x=50,
        start_y=50
    )
    koch.generate()
    koch.draw(canvas, "fractals")

    # Example 2: Dragon Curve (top right)
    dragon = LSystemPattern(
        width=297,
        height=210,
        preset="dragon",
        iterations=10,
        step_length=3.0,
        start_x=200,
        start_y=50
    )
    dragon.generate()
    dragon.draw(canvas, "curves")

    # Example 3: Plant (bottom left)
    plant1 = LSystemPattern(
        width=297,
        height=210,
        preset="plant1",
        iterations=5,
        step_length=3.0,
        start_x=70,
        start_y=200
    )
    plant1.generate()
    plant1.draw(canvas, "plants")

    # Example 4: Bushy Plant (bottom center)
    plant2 = LSystemPattern(
        width=297,
        height=210,
        preset="bushy",
        iterations=4,
        step_length=4.0,
        start_x=148.5,
        start_y=200
    )
    plant2.generate()
    plant2.draw(canvas, "plants")

    # Example 5: Custom L-System - Square Spiral (bottom right)
    custom = LSystemPattern.create_custom(
        width=297,
        height=210,
        axiom="F",
        rules={"F": "F+F-F-F+F"},
        angle=90.0,
        iterations=3,
        step_length=2.5,
        start_x=230,
        start_y=180,
        start_angle=0.0
    )
    custom.generate()
    custom.draw(canvas, "fractals")

    # Save
    canvas.save("output_lsystem.svg")
    print("✓ Saved L-System patterns to output_lsystem.svg")
    print(f"  Koch Snowflake: {len(koch.get_lines())} lines")
    print(f"  Dragon Curve: {len(dragon.get_lines())} lines")
    print(f"  Plant 1: {len(plant1.get_lines())} lines")
    print(f"  Bushy Plant: {len(plant2.get_lines())} lines")
    print(f"  Custom: {len(custom.get_lines())} lines")


if __name__ == "__main__":
    main()
