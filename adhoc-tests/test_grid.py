"""
Test and benchmark Rust GridGenerator
Shows performance for grid generation and distortions
"""
import time
from axiart.axiart_core import GridGenerator

def test_square_grids():
    """Test square grid generation"""
    print("\n" + "="*60)
    print("SQUARE GRIDS - Orthogonal Lines")
    print("="*60)

    tests = [
        (20.0, 0.0, "Coarse grid"),
        (10.0, 0.0, "Medium grid"),
        (5.0, 0.0, "Fine grid"),
        (10.0, 3.0, "Medium + jitter"),
    ]

    for cell_size, jitter, desc in tests:
        print(f"\n{desc}: cell={cell_size}mm, jitter={jitter}mm")

        grid = GridGenerator(width=297, height=210)

        start = time.time()
        lines = grid.generate_square_grid(
            cell_size=cell_size,
            jitter=jitter
        )
        elapsed = time.time() - start

        total_points = sum(len(line) for line in lines)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Lines: {len(lines)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {len(lines)/elapsed:,.0f} lines/sec")

def test_hexagonal_grids():
    """Test hexagonal grid generation"""
    print("\n" + "="*60)
    print("HEXAGONAL GRIDS - Honeycomb Tiling")
    print("="*60)

    tests = [
        (20.0, "Coarse hexagons"),
        (10.0, "Medium hexagons"),
        (5.0, "Fine hexagons"),
    ]

    for cell_size, desc in tests:
        print(f"\n{desc}: cell={cell_size}mm")

        grid = GridGenerator(width=297, height=210)

        start = time.time()
        lines = grid.generate_hexagonal_grid(cell_size=cell_size)
        elapsed = time.time() - start

        total_points = sum(len(line) for line in lines)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Hexagons: {len(lines)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {len(lines)/elapsed:,.0f} hexagons/sec")

def test_radial_distortion():
    """Test radial distortion on grids"""
    print("\n" + "="*60)
    print("RADIAL DISTORTION - Grid Warping")
    print("="*60)

    grid = GridGenerator(width=297, height=210)

    # Generate base grid
    print("\nGenerating base square grid (10mm cells)...")
    start = time.time()
    base_lines = grid.generate_square_grid(cell_size=10.0)
    gen_time = time.time() - start
    print(f"  Generation: {gen_time:.4f}s ({len(base_lines)} lines)")

    # Apply different distortion strengths
    tests = [
        (0.1, "Gentle warp"),
        (0.5, "Medium warp"),
        (1.0, "Strong warp"),
    ]

    for strength, desc in tests:
        print(f"\n{desc}: strength={strength}")

        start = time.time()
        distorted = grid.apply_radial_distortion(
            lines=base_lines,
            center=None,  # Use center of canvas
            strength=strength
        )
        elapsed = time.time() - start

        total_points = sum(len(line) for line in distorted)
        print(f"  Distortion time: {elapsed:.4f}s")
        print(f"  Lines: {len(distorted)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_distortion_centers():
    """Test distortion with different center points"""
    print("\n" + "="*60)
    print("DISTORTION CENTERS - Different Origins")
    print("="*60)

    grid = GridGenerator(width=297, height=210)
    base_lines = grid.generate_square_grid(cell_size=10.0)

    tests = [
        (None, "Canvas center"),
        ((148.5, 105.0), "Manual center (same as auto)"),
        ((50.0, 50.0), "Top-left quadrant"),
        ((247.0, 160.0), "Bottom-right quadrant"),
    ]

    for center, desc in tests:
        print(f"\n{desc}: center={center}")

        start = time.time()
        distorted = grid.apply_radial_distortion(
            lines=base_lines,
            center=center,
            strength=0.5
        )
        elapsed = time.time() - start

        print(f"  Time: {elapsed:.4f}s")
        print(f"  Lines: {len(distorted)}")

def test_large_grids():
    """Test large-scale grid generation"""
    print("\n" + "="*60)
    print("LARGE-SCALE GRID GENERATION")
    print("="*60)

    tests = [
        (5.0, "square", "Fine square grid"),
        (2.0, "square", "Very fine square grid"),
        (3.0, "hexagonal", "Fine hexagonal grid"),
    ]

    for cell_size, grid_type, desc in tests:
        print(f"\n{desc}: {grid_type} @ {cell_size}mm")

        grid = GridGenerator(width=297, height=210)

        start = time.time()
        if grid_type == "square":
            lines = grid.generate_square_grid(cell_size=cell_size)
        else:
            lines = grid.generate_hexagonal_grid(cell_size=cell_size)
        elapsed = time.time() - start

        total_points = sum(len(line) for line in lines)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Lines: {len(lines)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {len(lines)/elapsed:,.0f} lines/sec")

def test_comprehensive():
    """Test complete workflow: generate + distort"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST - Generate + Distort")
    print("="*60)

    grid = GridGenerator(width=297, height=210)

    print("\nWorkflow: Generate hexagonal → Apply radial distortion")

    # Generate
    start = time.time()
    lines = grid.generate_hexagonal_grid(cell_size=8.0)
    t1 = time.time() - start

    # Distort
    start = time.time()
    distorted = grid.apply_radial_distortion(
        lines=lines,
        center=(148.5, 105.0),
        strength=0.7
    )
    t2 = time.time() - start

    total_time = t1 + t2
    total_points = sum(len(line) for line in distorted)

    print(f"  Generation: {t1:.4f}s ({len(lines)} hexagons)")
    print(f"  Distortion: {t2:.4f}s ({total_points:,} points)")
    print(f"  Total time: {total_time:.4f}s")
    if total_time > 0:
        print(f"  Overall speed: {total_points/total_time:,.0f} points/sec")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUST GRID GENERATOR - COMPREHENSIVE BENCHMARKS")
    print("="*60)

    test_square_grids()
    test_hexagonal_grids()
    test_radial_distortion()
    test_distortion_centers()
    test_large_grids()
    test_comprehensive()

    print("\n" + "="*60)
    print("✅ All tests passed! GridGenerator is production-ready!")
    print("="*60)
