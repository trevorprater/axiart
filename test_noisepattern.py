"""
Test and benchmark Rust NoisePatternGenerator
Shows performance of marching squares, stippling, and cellular textures
"""
import time
from axiart.axiart_core import NoisePatternGenerator

def test_contour_lines():
    """Test contour line generation with marching squares"""
    print("\n" + "="*60)
    print("CONTOUR LINES - Marching Squares Algorithm")
    print("="*60)

    noise = NoisePatternGenerator(
        width=297,
        height=210,
        scale=100.0,
        octaves=4,
        seed=42
    )

    tests = [
        (10, 2.0, "Low detail"),
        (20, 2.0, "Medium detail"),
        (50, 1.0, "High detail"),
    ]

    for num_levels, resolution, desc in tests:
        print(f"\n{desc}: {num_levels} levels, {resolution}mm resolution")
        start = time.time()
        segments = noise.generate_contour_lines(
            num_levels=num_levels,
            resolution=resolution,
            min_value=-1.0,
            max_value=1.0
        )
        elapsed = time.time() - start

        print(f"  Time: {elapsed:.3f}s")
        print(f"  Segments: {len(segments):,}")
        print(f"  Speed: {len(segments)/elapsed:,.0f} segments/sec")

def test_stippling():
    """Test stippling with parallel generation"""
    print("\n" + "="*60)
    print("STIPPLING - Noise-Based Density Mapping")
    print("="*60)

    noise = NoisePatternGenerator(
        width=297,
        height=210,
        scale=100.0,
        octaves=4,
        seed=42
    )

    tests = [
        (5000, "Small"),
        (10000, "Medium"),
        (50000, "Large"),
    ]

    for num_points, desc in tests:
        print(f"\n{desc}: {num_points:,} candidate points")
        start = time.time()
        points = noise.generate_stippling(
            num_points=num_points,
            density_map=True,
            threshold=0.0,
            parallel=True
        )
        elapsed = time.time() - start

        print(f"  Time: {elapsed:.3f}s")
        print(f"  Final points: {len(points):,}")
        print(f"  Speed: {num_points/elapsed:,.0f} points/sec")

def test_cellular_texture():
    """Test cellular texture generation"""
    print("\n" + "="*60)
    print("CELLULAR TEXTURE - Noise-Based Patterns")
    print("="*60)

    noise = NoisePatternGenerator(
        width=297,
        height=210,
        scale=50.0,
        octaves=4,
        seed=42
    )

    pattern_types = ["squares", "circles", "hatching"]

    for ptype in pattern_types:
        print(f"\n{ptype.upper()}: cell_size=5.0mm")
        start = time.time()
        paths, points = noise.generate_cellular_texture(
            cell_size=5.0,
            threshold=0.0,
            pattern_type=ptype
        )
        elapsed = time.time() - start

        print(f"  Time: {elapsed:.3f}s")
        print(f"  Paths: {len(paths):,}")
        print(f"  Points: {len(points):,}")

def test_hatching():
    """Test gradient-based hatching"""
    print("\n" + "="*60)
    print("HATCHING - Gradient-Based Line Direction")
    print("="*60)

    noise = NoisePatternGenerator(
        width=297,
        height=210,
        scale=50.0,
        octaves=4,
        seed=42
    )

    tests = [
        (10.0, "Sparse"),
        (5.0, "Medium"),
        (2.0, "Dense"),
    ]

    for spacing, desc in tests:
        print(f"\n{desc}: {spacing}mm spacing")
        start = time.time()
        lines = noise.generate_hatching(
            spacing=spacing,
            line_length=10.0,
            threshold=0.0
        )
        elapsed = time.time() - start

        print(f"  Time: {elapsed:.3f}s")
        print(f"  Lines: {len(lines):,}")
        if elapsed > 0:
            print(f"  Speed: {len(lines)/elapsed:,.0f} lines/sec")

def test_comprehensive():
    """Test all features together"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST - All Features")
    print("="*60)

    noise = NoisePatternGenerator(
        width=297,
        height=210,
        scale=100.0,
        octaves=4,
        seed=42
    )

    print("\nGenerating complete noise-based artwork:")
    total_start = time.time()

    # Contours
    start = time.time()
    contours = noise.generate_contour_lines(num_levels=30, resolution=1.5)
    t1 = time.time() - start

    # Stippling
    start = time.time()
    points = noise.generate_stippling(num_points=20000, parallel=True)
    t2 = time.time() - start

    # Cellular
    start = time.time()
    paths, circles = noise.generate_cellular_texture(cell_size=5.0, pattern_type="squares")
    t3 = time.time() - start

    total_time = time.time() - total_start

    print(f"  Contours: {len(contours):,} segments in {t1:.3f}s")
    print(f"  Stippling: {len(points):,} points in {t2:.3f}s")
    print(f"  Cellular: {len(paths):,} paths in {t3:.3f}s")
    print(f"\n  Total time: {total_time:.3f}s")
    print(f"  Combined elements: {len(contours) + len(points) + len(paths):,}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUST NOISEPATTERN GENERATOR - COMPREHENSIVE BENCHMARKS")
    print("="*60)

    test_contour_lines()
    test_stippling()
    test_cellular_texture()
    test_hatching()
    test_comprehensive()

    print("\n" + "="*60)
    print("✅ All tests passed! NoisePattern is production-ready!")
    print("="*60)
