# Creating Artistic Compositions with AxiArt

This guide shows how to create intentional, artistic compositions beyond simple pattern demonstrations - achieving results comparable to professional generative artwork.

## Philosophy: From Patterns to Art

The pattern generators are **tools**, not the artwork itself. Great generative art combines:

1. **Intentional composition** - What are you creating? (face, landscape, abstract form)
2. **Layered storytelling** - Each layer adds meaning
3. **Selective color** - Strategic use of 1-3 accent colors
4. **Filled shapes + line work** - Combine both for depth
5. **Organic + geometric balance** - Natural and structured elements together

## Key Techniques

### 1. Start with Filled Shapes

Use filled geometric shapes to establish your composition's structure:

```python
from axiart.shapes import Circle, Rectangle, Polygon, add_filled_shape

# Create a filled circle for a face
head = Circle(center=(148, 100), radius=55)
add_filled_shape(canvas, head, fill_color="#FFE66D", stroke_color="black")

# Create a polygon for a body
body = Polygon([
    (120, 150),
    (176, 150),
    (190, 210),
    (106, 210)
])
add_filled_shape(canvas, body, fill_color="#A8DADC", stroke_color="black")
```

### 2. Layer Patterns with Purpose

Each pattern should serve a compositional purpose:

- **Grids**: Background structure, organization
- **Spirals**: Eyes, focal points, centers of attention
- **Flow fields**: Texture, movement, organic feeling
- **Dendrites**: Hair, trees, organic growth from edges
- **Noise**: Shading, depth, atmospheric effects

```python
# Background: Subtle distorted grid
grid = GridPattern(width=297, height=210)
grid.generate_square_grid(cell_size=12, jitter=0.3)
grid.apply_radial_distortion(strength=0.05)
comp.add_pattern(grid, "background")

# Focal point: Concentric spirals for eyes
eye = SpiralPattern(center=(125, 90))
eye.generate_circular_waves(num_circles=12, wave_amplitude=0.3)
comp.add_pattern(eye, "accent_color")
```

### 3. Use Color Strategically

Follow the "mostly black + 1-2 accents" rule:

```python
comp = Composition(width=297, height=210, background="#FAFAFA")

# Layer hierarchy
comp.add_layer("fills", color="none")          # Filled shapes
comp.add_layer("background", color="#CCC")     # Subtle grid
comp.add_layer("primary", color="black")       # Main linework
comp.add_layer("accent1", color="#FF6B6B")     # Red highlights
comp.add_layer("accent2", color="#4ECDC4")     # Teal details
```

### 4. Create Depth with Overlays

Add semi-transparent fills behind line patterns:

```python
# Add colored background behind pattern
bg_circle = Circle(center=(125, 90), radius=18)
add_filled_shape(canvas, bg_circle, fill_color="#E0F7FA", stroke_color="none")

# Then draw pattern on top
eye_pattern = SpiralPattern(center=(125, 90))
eye_pattern.generate_circular_waves(...)
comp.add_pattern(eye_pattern, "accent_layer")
```

### 5. Constrain Patterns to Regions

Filter pattern points to specific areas:

```python
# Generate texture
texture = NoisePattern(scale=25)
texture.generate_stippling(num_points=1000)

# Only keep points in specific region
filtered = [
    (x, y) for x, y in texture.get_points()
    if 100 < x < 200 and 150 < y < 210  # Body area only
]
canvas.add_points(filtered, "texture_layer")
```

### 6. Balance Organic and Geometric

Combine structured grids with organic dendrites:

```python
# Geometric structure
grid.generate_hexagonal_grid(cell_size=15)

# Organic growth from corners
dendrite = DendritePattern(
    num_particles=300,
    branching_style="radial",
    seed_points=[(15, 15)]  # Corner
)
dendrite.generate()
```

## Complete Example: Abstract Face

Here's how to create an artistic face composition:

```python
from axiart.composition import Composition
from axiart.patterns import SpiralPattern, FlowFieldPattern, DendritePattern
from axiart.shapes import Circle, Rectangle, add_filled_shape

# Setup
comp = Composition(width=297, height=210, background="white")
comp.add_layer("fills", color="none")
comp.add_layer("grid", color="#DDD", stroke_width=0.3)
comp.add_layer("main", color="black", stroke_width=0.5)
comp.add_layer("accent", color="#9C27B0", stroke_width=0.6)

canvas = comp.get_canvas()

# 1. Background grid for structure
grid = GridPattern(width=297, height=210)
grid.generate_square_grid(cell_size=15)
comp.add_pattern(grid, "grid")

# 2. Face shape (filled circle)
canvas.set_layer("fills")
face = Circle(center=(148, 105), radius=60)
add_filled_shape(canvas, face, fill_color="#FFF9C4", stroke_color="black")

# 3. Eyes (concentric spirals with color background)
# Left eye
left_eye_bg = Circle(center=(125, 95), radius=15)
add_filled_shape(canvas, left_eye_bg, fill_color="#E1BEE7")

left_eye = SpiralPattern(center=(125, 95))
left_eye.generate_circular_waves(num_circles=10, end_radius=12)
comp.add_pattern(left_eye, "accent")

# Right eye (similar)
right_eye_bg = Circle(center=(171, 95), radius=15)
add_filled_shape(canvas, right_eye_bg, fill_color="#E1BEE7")

right_eye = SpiralPattern(center=(171, 95))
right_eye.generate_circular_waves(num_circles=10, end_radius=12)
comp.add_pattern(right_eye, "accent")

# 4. Mouth (flow field texture)
mouth_flow = FlowFieldPattern(field_type="waves")
mouth_starts = [(x, y) for x in range(115, 181, 2) for y in range(130, 145, 2)]
mouth_flow.generate_streamlines(
    num_lines=len(mouth_starts),
    steps=30,
    start_positions=mouth_starts
)
comp.add_pattern(mouth_flow, "main")

# 5. Hair (dendrites from top)
hair = DendritePattern(
    num_particles=500,
    branching_style="vertical",
    seed_points=[(148, 45)]
)
hair.generate()
comp.add_pattern(hair, "main")

# Save
comp.save("artistic_face.svg")
```

## Composition Checklist

When creating artistic work, ask yourself:

- [ ] Does it have a clear subject or focal point?
- [ ] Do the layers work together or compete?
- [ ] Is color used strategically (not randomly)?
- [ ] Is there balance between filled and line work?
- [ ] Do organic and geometric elements complement each other?
- [ ] Does each pattern serve a compositional purpose?
- [ ] Would this work well as a physical pen plot?

## Examples to Study

Check these examples in `examples/`:

- `example_portrait.py` - Abstract portrait with filled shapes + patterns
- `example_abstract_character.py` - Complete character with personality
- `example_mixed_landscape.py` - Landscape composition with layers

Compare these to the simpler pattern demonstrations to see how intentional composition elevates the work.

## Advanced Tips

### Custom Color Backgrounds for Patterns

```python
# Semi-transparent color fill behind a pattern area
canvas.dwg.add(canvas.dwg.rect(
    insert=(100, 100),
    size=(50, 30),
    fill="#FFCCCB",
    stroke="none",
    opacity=0.5
))
```

### Layer Order Matters

Layers are drawn in order created - create layers from back to front:

```python
comp.add_layer("background", ...)   # Drawn first (back)
comp.add_layer("midground", ...)
comp.add_layer("foreground", ...)   # Drawn last (front)
```

### Positioning Patterns Strategically

Use `start_positions` to control where patterns appear:

```python
# Create flow field only in specific area
starts = [
    (x, y)
    for x in range(100, 200, 5)
    for y in range(100, 150, 5)
]
flow.generate_streamlines(start_positions=starts)
```

### Combining Pattern Outputs

Get raw data from patterns and combine:

```python
# Get dendrite lines
dendrite_lines = dendrite.get_lines()

# Get noise points
noise_points = noise.get_points()

# Filter and combine based on your composition needs
combined = custom_filter_function(dendrite_lines, noise_points)
```

## Learning Resources

1. Study the `claude-face.jpeg` reference in `examples/`
2. Run `example_abstract_character.py` and study the code
3. Experiment with layer order and colors
4. Try creating recognizable subjects (faces, animals, landscapes)
5. Print/plot your work to see what works physically

Remember: The best generative art combines algorithmic patterns with human artistic intent!
