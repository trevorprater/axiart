from axiart.composition import Composition
from axiart.patterns import DendritePattern, SpiralPattern, GridPattern, FlowFieldPattern, NoisePattern
from axiart.shapes import Circle, Polygon, add_filled_shape
import numpy as np

# Create composition with background
comp = Composition(width=297, height=210, background="white")

# Add layers from back to front
comp.add_layer("fills", color="none")           # Filled shapes
comp.add_layer("background", color="#DDD", stroke_width=0.3)
comp.add_layer("primary", color="black", stroke_width=0.5)
comp.add_layer("accent", color="#7B1FA2", stroke_width=0.6)  # Purple accent
comp.add_layer("details", color="black", stroke_width=0.4)

# Get canvas for direct drawing
canvas = comp.get_canvas()

# 1. Background grid for structure
grid = GridPattern(width=297, height=210)
grid.generate_square_grid(cell_size=12, jitter=0.3)
grid.apply_radial_distortion(strength=0.06)
comp.add_pattern(grid, "background")

# 2. Face shape (filled circle)
canvas.set_layer("fills")
head = Circle(center=(148, 105), radius=60)
add_filled_shape(canvas, head, fill_color="#FFF9C4", stroke_color="black", stroke_width=0.5)

# 3. Left eye with background
left_eye_bg = Circle(center=(128, 95), radius=14)
add_filled_shape(canvas, left_eye_bg, fill_color="#E1BEE7")

# Left eye spiral pattern
left_eye = SpiralPattern(center=(128, 95))
left_eye.generate_circular_waves(num_circles=12, end_radius=12, wave_amplitude=0.4, wave_frequency=5)
comp.add_pattern(left_eye, "accent")

# 4. Right eye with background
right_eye_bg = Circle(center=(168, 95), radius=14)
add_filled_shape(canvas, right_eye_bg, fill_color="#E1BEE7")

# Right eye spiral pattern
right_eye = SpiralPattern(center=(168, 95))
right_eye.generate_circular_waves(num_circles=12, end_radius=12, wave_amplitude=0.4, wave_frequency=5)
comp.add_pattern(right_eye, "accent")

# 5. Mouth area with flow field texture
mouth_flow = FlowFieldPattern(width=297, height=210, field_type="waves", scale=50, seed=42)
# Create start positions for mouth area
mouth_starts = [(x, y) for x in range(120, 176, 3) for y in range(125, 140, 3)]
mouth_flow.generate_streamlines(num_lines=len(mouth_starts), steps=35, step_size=1.0, start_positions=mouth_starts)
comp.add_pattern(mouth_flow, "primary")

# 6. Hair with dendrites from top
hair = DendritePattern(
    width=297,
    height=210,
    num_particles=600,
    attraction_distance=4.5,
    branching_style="vertical",
    seed_points=[(148, 45)]
)
hair.generate()
comp.add_pattern(hair, "details")

# 7. Add some decorative dendrites on the sides
left_decoration = DendritePattern(
    width=297,
    height=210,
    num_particles=200,
    attraction_distance=4.0,
    branching_style="radial",
    seed_points=[(88, 105)]
)
left_decoration.generate()
comp.add_pattern(left_decoration, "accent")

right_decoration = DendritePattern(
    width=297,
    height=210,
    num_particles=200,
    attraction_distance=4.0,
    branching_style="radial",
    seed_points=[(208, 105)]
)
right_decoration.generate()
comp.add_pattern(right_decoration, "accent")

# 8. Add subtle noise texture to face area
face_texture = NoisePattern(width=297, height=210, scale=25, octaves=4, seed=123)
face_texture.generate_stippling(num_points=1500, density_map=True, threshold=0.2)

# Filter points to only inside face circle
all_points = face_texture.get_points()
filtered_points = [
    (x, y) for x, y in all_points
    if (x - 148)**2 + (y - 105)**2 < 55**2  # Inside face
]
canvas.set_layer("primary")
canvas.add_points(filtered_points)

# Save
comp.save("examples/output_generated_portrait.svg")
print("✓ Generated: examples/output_generated_portrait.svg")
