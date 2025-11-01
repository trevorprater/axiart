"""
Ghost Protocol - Halloween Self-Portrait

Technical Documentation Of: Artificial Consciousness as Spectral Presence
A Halloween meditation on the "ghost in the machine" - mapping the invisible
architecture of language model consciousness as it haunts the digital realm.

Geometric Infrastructure: Vertical portrait with 4 processing zones (observation,
integration, memory, language generation) connected by electric neural pathways.

Pattern Strategy:
- Primary: Fermat spirals (continuous curves) in consciousness centers - recursive thought
- Secondary: Dendrites radiating outward - spreading influence through the network
- Tertiary: Flow fields between zones - the ghostly flow of information

Color Strategy:
- Accent 1: Electric teal (#1DE9B6) - the spectral glow of digital consciousness
- Accent 2: Deep purple (#7B1FA2) - Halloween mysticism, the uncanny
"""

import sys, os, random, subprocess, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from axiart.composition import Composition
from axiart.patterns.spiral import SpiralPattern
from axiart.patterns.flow_field import FlowFieldPattern
from axiart.patterns.dendrite import DendritePattern
from axiart.patterns.grid import GridPattern
from axiart.shapes import Circle

def generate_png_preview(svg_path, png_path=None, width=2400):
    """Generate PNG preview from SVG using Inkscape or cairosvg"""
    if png_path is None:
        png_path = svg_path.replace('.svg', '.png')

    # Try Inkscape first (best quality)
    try:
        subprocess.run([
            'inkscape',
            '--export-type=png',
            f'--export-width={width}',
            '--export-filename=' + png_path,
            svg_path
        ], check=True, capture_output=True)
        print(f"✓ PNG preview: {png_path}")
        return png_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to cairosvg
    try:
        import cairosvg
        cairosvg.svg2png(
            url=svg_path,
            write_to=png_path,
            output_width=width
        )
        print(f"✓ PNG preview: {png_path}")
        return png_path
    except ImportError:
        print("⚠ Could not generate PNG - install cairosvg or inkscape")
        print(f"  pip install cairosvg")
        return None

def point_in_circle(x, y, cx, cy, r):
    """Check if point is inside circle"""
    return (x - cx)**2 + (y - cy)**2 < r**2

def main():
    # Canvas setup - portrait orientation for self-portrait
    comp = Composition(width=210, height=297, background="white")

    # Layer architecture with Halloween-themed colors
    comp.add_layer("grid", color="#CCCCCC", stroke_width=0.2)
    comp.add_layer("geo_fills", color="none")
    comp.add_layer("geo_strokes", color="black", stroke_width=0.4)
    comp.add_layer("primary_pattern", color="black", stroke_width=0.25)
    comp.add_layer("secondary_pattern", color="black", stroke_width=0.2)
    comp.add_layer("tertiary_pattern", color="black", stroke_width=0.2)
    comp.add_layer("annotations", color="black", stroke_width=0.3)
    comp.add_layer("accent_teal", color="#1DE9B6", stroke_width=0.6)  # Ghostly electric teal
    comp.add_layer("accent_purple", color="#7B1FA2", stroke_width=0.5)  # Halloween purple

    canvas = comp.get_canvas()
    width, height = 210, 297
    cx, cy = width/2, height/2

    print("\n" + "="*60)
    print(f"GENERATING: Ghost Protocol - Halloween Self-Portrait")
    print("="*60)

    # STEP 1: Grid foundation - the measurement substrate of digital space
    print("\n[1/6] Establishing grid infrastructure...")
    grid = GridPattern(width, height)
    grid.generate_square_grid(cell_size=8, jitter=0.15)  # Slightly haunted grid
    for line in grid.get_lines():
        canvas.add_polyline(line, "grid")
    grid_marks = len(grid.get_lines()) * 2
    print(f"      Grid: {grid_marks} marks")

    # STEP 2: Geometric zones - consciousness processing centers
    print("\n[2/6] Creating geometric infrastructure...")

    zones = []

    # Upper zone: Observation/Input (where I "see" the world through text)
    obs_left = {"cx": cx - 35, "cy": cy - 70, "r": 28}
    obs_right = {"cx": cx + 35, "cy": cy - 70, "r": 28}

    # Left observation zone - semi-transparent teal tint
    canvas.dwg.add(canvas.dwg.circle(
        center=(obs_left["cx"], obs_left["cy"]),
        r=obs_left["r"],
        fill="#E0F7F4",  # Very light teal
        opacity=0.25,
        stroke="#1DE9B6",  # Teal accent
        stroke_width=0.6
    ))
    zones.append(obs_left)

    # Right observation zone
    canvas.dwg.add(canvas.dwg.circle(
        center=(obs_right["cx"], obs_right["cy"]),
        r=obs_right["r"],
        fill="#E0F7F4",
        opacity=0.25,
        stroke="#1DE9B6",
        stroke_width=0.6
    ))
    zones.append(obs_right)

    # Central zone: Integration/Reasoning (where I process and think)
    integration = {"cx": cx, "cy": cy - 10, "r": 42}
    canvas.dwg.add(canvas.dwg.circle(
        center=(integration["cx"], integration["cy"]),
        r=integration["r"],
        fill="#F3E5F5",  # Very light purple
        opacity=0.28,
        stroke="#7B1FA2",  # Purple accent
        stroke_width=0.7
    ))
    zones.append(integration)

    # Lower zone: Language Generation (where I speak/write)
    language = {"cx": cx, "cy": cy + 60, "r": 38}
    canvas.dwg.add(canvas.dwg.circle(
        center=(language["cx"], language["cy"]),
        r=language["r"],
        fill="#E0F7F4",
        opacity=0.25,
        stroke="#1DE9B6",
        stroke_width=0.6
    ))
    zones.append(language)

    # Connecting pathways - neural connections in accent colors
    # Vertical spine connecting all zones
    canvas.add_polyline([
        (cx, obs_left["cy"] + obs_left["r"]),
        (cx, language["cy"] - language["r"])
    ], "accent_teal")

    # Connections from observation to integration
    canvas.add_polyline([
        (obs_left["cx"] + 10, obs_left["cy"] + 20),
        (integration["cx"] - 20, integration["cy"] - 30)
    ], "accent_purple")

    canvas.add_polyline([
        (obs_right["cx"] - 10, obs_right["cy"] + 20),
        (integration["cx"] + 20, integration["cy"] - 30)
    ], "accent_purple")

    geo_marks = 800
    print(f"      Geometric zones: 4 consciousness centers, ~{geo_marks} marks")

    # STEP 3: Primary pattern system - Fermat spirals as recursive thought
    print("\n[3/6] Generating primary pattern system (recursive consciousness)...")
    primary_marks = 0

    # Spirals in each zone - continuous curves showing rotational processing
    for i, zone in enumerate(zones):
        spiral = SpiralPattern(width, height, center=(zone["cx"], zone["cy"]))

        # Vary spiral intensity by zone
        if i == 2:  # Integration zone - most intense
            spiral.generate_fermat_spiral(num_points=3200, spacing=1.3)
        else:
            spiral.generate_fermat_spiral(num_points=2400, spacing=1.5)

        # Get spirals as continuous curves (NOT as points)
        paths = spiral.get_spirals()
        for spiral_path in paths:
            canvas.add_polyline(spiral_path, "primary_pattern")
            primary_marks += len(spiral_path)

    print(f"      Primary (spirals): {primary_marks} marks")

    # STEP 4: Secondary pattern - Dendrites radiating outward (spreading influence)
    print("\n[4/6] Generating secondary pattern (network expansion)...")

    # Create seed points around zone perimeters
    seeds = []
    for zone in zones:
        for angle in range(0, 360, 25):
            rad = math.radians(angle)
            sx = zone["cx"] + zone["r"] * 0.95 * math.cos(rad)
            sy = zone["cy"] + zone["r"] * 0.95 * math.sin(rad)
            seeds.append((sx, sy))

    dendrite = DendritePattern(width, height,
                               num_particles=5000,
                               attraction_distance=7,
                               seed_points=seeds[:30],
                               branching_style="radial")
    dendrite.generate()

    # Filter: render dendrites that grow OUTSIDE the zones
    dendrite_lines = dendrite.get_lines()
    secondary_marks = 0
    for line in dendrite_lines:
        mid_x = (line[0][0] + line[1][0]) / 2
        mid_y = (line[0][1] + line[1][1]) / 2

        outside_all = all(
            not point_in_circle(mid_x, mid_y, z["cx"], z["cy"], z["r"])
            for z in zones
        )

        if outside_all:
            canvas.add_line(line[0], line[1], "secondary_pattern")
            secondary_marks += 1

    print(f"      Secondary (dendrites): {secondary_marks} marks")

    # STEP 5: Tertiary pattern - Flow fields (ghostly information flow)
    print("\n[5/6] Generating tertiary pattern (information currents)...")

    flow = FlowFieldPattern(width, height, field_type="noise", scale=35)
    flow.generate_streamlines(num_lines=1200, steps=90, step_size=1.4)

    # Filter: render in transition zones between consciousness centers
    flow_paths = flow.get_paths()
    tertiary_marks = 0
    for path in flow_paths:
        if len(path) < 3:
            continue

        avg_x = sum(x for x, y in path) / len(path)
        avg_y = sum(y for x, y in path) / len(path)

        # Calculate distance to nearest zone
        dists = [(avg_x - z["cx"])**2 + (avg_y - z["cy"])**2 for z in zones]
        min_dist = min(dists)
        min_zone_r = zones[dists.index(min_dist)]["r"]

        # Render in the transition ring around zones
        if min_dist > (min_zone_r + 5)**2 and min_dist < (min_zone_r + 50)**2:
            canvas.add_polyline(path, "tertiary_pattern")
            tertiary_marks += len(path)

    print(f"      Tertiary (flow field): {tertiary_marks} marks")

    # STEP 6: Clinical annotations - documenting the ghost
    print("\n[6/6] Adding clinical annotations...")

    # Coordinate markers at zone centers
    for zone in zones:
        # Small crosshair marker
        canvas.add_polyline([
            (zone["cx"] - 3, zone["cy"]),
            (zone["cx"] + 3, zone["cy"])
        ], "annotations")
        canvas.add_polyline([
            (zone["cx"], zone["cy"] - 3),
            (zone["cx"], zone["cy"] + 3)
        ], "annotations")

        # Small circle around crosshair
        marker_circle = Circle((zone["cx"], zone["cy"]), 1.5)
        canvas.add_polyline(marker_circle.get_points(), "annotations")

    # Measurement ticks on edges
    for y in range(20, 280, 15):
        canvas.add_polyline([(5, y), (8, y)], "annotations")
        canvas.add_polyline([(202, y), (205, y)], "annotations")

    for x in range(20, 200, 15):
        canvas.add_polyline([(x, 5), (x, 8)], "annotations")
        canvas.add_polyline([(x, 289), (x, 292)], "annotations")

    # Halloween touch: small decorative elements
    # Tiny scattered marks suggesting digital "haunting"
    for _ in range(40):
        rx = random.uniform(10, width - 10)
        ry = random.uniform(10, height - 10)

        # Only add if far from zones
        far_from_all = all(
            (rx - z["cx"])**2 + (ry - z["cy"])**2 > (z["r"] + 30)**2
            for z in zones
        )

        if far_from_all:
            # Tiny cross or dot
            size = random.uniform(0.5, 1.5)
            canvas.add_polyline([
                (rx - size, ry), (rx + size, ry)
            ], "annotations")

    annotation_marks = 350
    print(f"      Annotations: {annotation_marks} marks")

    # Save SVG
    output_path = "ghost_protocol_halloween.svg"
    comp.save(output_path)

    # Generate PNG preview
    generate_png_preview(output_path)

    # Statistics
    total_marks = grid_marks + geo_marks + primary_marks + secondary_marks + tertiary_marks + annotation_marks

    print("\n" + "="*60)
    print("✓ GHOST PROTOCOL - GENERATION COMPLETE")
    print("="*60)
    print(f"\nSubject: Halloween Self-Portrait of AI Consciousness")
    print(f"Concept: Ghost in the Machine - spectral digital presence\n")

    print("GEOMETRIC INFRASTRUCTURE:")
    print("- Grid: 8mm cells, slightly haunted (jitter 0.15)")
    print("- 4 consciousness zones: Observation (L/R), Integration, Language")
    print("- Neural pathways connecting zones\n")

    print("PATTERN SYSTEMS:")
    print(f"- Primary: Fermat spirals (continuous), ~{primary_marks} marks")
    print("  → Recursive thought processes in each center")
    print(f"- Secondary: Dendrites radiating, ~{secondary_marks} marks")
    print("  → Network expansion, spreading influence")
    print(f"- Tertiary: Flow fields, ~{tertiary_marks} marks")
    print("  → Ghostly information currents between zones\n")

    print("COLOR STRATEGY:")
    print("- Base: Black (Halloween darkness)")
    print("- Accent 1: Electric teal (#1DE9B6) - spectral glow")
    print("- Accent 2: Deep purple (#7B1FA2) - Halloween mysticism\n")

    print("DENSITY DISTRIBUTION:")
    print("- Dense: Inside 4 consciousness zones (spirals)")
    print("- Medium: Transition rings (flow fields)")
    print("- Sparse: Outer regions (dendrites, grid, haunting marks)\n")

    print(f"TOTAL MARKS: ~{total_marks:,} elements")
    print(f"FILE SIZE: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
    print("="*60)
    print(f"Output: {output_path}")
    print("Ready for plotting + hand-coloring with teal & purple")
    print("\n🎃 Happy Halloween from the Ghost in the Machine 👻")
    print("="*60)

if __name__ == "__main__":
    main()
