#!/usr/bin/env python3
"""Example: Flow Field Pattern"""

import sys
sys.path.insert(0, '..')

from axiart.patterns import FlowFieldPattern
from axiart.composition import create_standard_composition, ColorPalette


def main():
    # Create composition with purple accent
    comp = create_standard_composition(palette=ColorPalette.PURPLE_ACCENT)

    # Generate noise-based flow field
    flow1 = FlowFieldPattern(
        width=297,
        height=210,
        field_type="noise",
        scale=60,
        seed=42
    )
    print("Generating flow field streamlines...")
    flow1.generate_streamlines(num_lines=80, steps=250, step_size=1.2)
    comp.add_pattern(flow1, "primary")

    # Generate spiral flow field as accent
    flow2 = FlowFieldPattern(
        width=297,
        height=210,
        field_type="spiral",
        scale=50
    )
    flow2.generate_streamlines(num_lines=30, steps=150, step_size=1.0)
    comp.add_pattern(flow2, "accent")

    # Save
    comp.save("output_flow.svg")
    print("✓ Saved to output_flow.svg")


if __name__ == "__main__":
    main()
