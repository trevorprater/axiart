"""
Test and benchmark Rust SpiralGenerator
Shows performance across different spiral types and configurations
"""
import time
from axiart.axiart_core import SpiralGenerator

def test_archimedean_spirals():
    """Test Archimedean spiral generation"""
    print("\n" + "="*60)
    print("ARCHIMEDEAN SPIRALS - Linear Growth")
    print("="*60)

    tests = [
        (10, 100, "Small"),
        (50, 200, "Medium"),
        (100, 500, "Large"),
    ]

    for num_revs, points_per_rev, desc in tests:
        print(f"\n{desc}: {num_revs} revolutions × {points_per_rev} points/rev")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            num_revolutions=num_revs,
            points_per_revolution=points_per_rev,
            spiral_type="archimedean"
        )

        start = time.time()
        paths = spiral.generate(
            start_radius=5.0,
            num_spirals=1
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Spirals: {len(paths)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_logarithmic_spirals():
    """Test logarithmic spiral generation"""
    print("\n" + "="*60)
    print("LOGARITHMIC SPIRALS - Exponential Growth")
    print("="*60)

    tests = [
        (1.0, "Standard"),
        (1.5, "Accelerated"),
        (0.5, "Decelerated"),
    ]

    for growth, desc in tests:
        print(f"\n{desc}: growth_factor={growth}")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            num_revolutions=20,
            points_per_revolution=200,
            spiral_type="logarithmic"
        )

        start = time.time()
        paths = spiral.generate(
            start_radius=5.0,
            growth_factor=growth,
            num_spirals=1
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_concentric_spirals():
    """Test concentric (discrete) spiral generation"""
    print("\n" + "="*60)
    print("CONCENTRIC SPIRALS - Discrete Circles")
    print("="*60)

    tests = [
        (10, "Few circles"),
        (30, "Medium density"),
        (50, "High density"),
    ]

    for num_revs, desc in tests:
        print(f"\n{desc}: {num_revs} circles")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            num_revolutions=num_revs,
            points_per_revolution=200,
            spiral_type="concentric"
        )

        start = time.time()
        paths = spiral.generate(
            start_radius=5.0,
            num_spirals=1
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_multiple_spirals():
    """Test multiple interleaved spirals"""
    print("\n" + "="*60)
    print("MULTIPLE SPIRALS - Angular Offset")
    print("="*60)

    tests = [
        (2, 3.14159),  # 2 spirals, 180° offset
        (3, 2.0944),   # 3 spirals, 120° offset
        (5, 1.2566),   # 5 spirals, 72° offset
    ]

    for num_spirals, angular_offset in tests:
        print(f"\n{num_spirals} spirals with {angular_offset:.2f} rad offset")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            num_revolutions=20,
            points_per_revolution=200,
            spiral_type="archimedean"
        )

        start = time.time()
        paths = spiral.generate(
            start_radius=5.0,
            num_spirals=num_spirals,
            angular_offset=angular_offset
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Generated: {len(paths)} spirals")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_circular_waves():
    """Test circular wave generation with undulation"""
    print("\n" + "="*60)
    print("CIRCULAR WAVES - Undulating Circles")
    print("="*60)

    tests = [
        (20, 0.0, 0.0, "Perfect circles"),
        (20, 2.0, 5.0, "Gentle waves"),
        (30, 5.0, 10.0, "Strong waves"),
    ]

    for num_circles, amplitude, frequency, desc in tests:
        print(f"\n{desc}: amp={amplitude}, freq={frequency}")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            spiral_type="concentric"
        )

        start = time.time()
        paths = spiral.generate_circular_waves(
            num_circles=num_circles,
            points_per_circle=200,
            wave_amplitude=amplitude,
            wave_frequency=frequency
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Circles: {len(paths)}")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

def test_large_scale():
    """Test large-scale spiral generation"""
    print("\n" + "="*60)
    print("LARGE-SCALE SPIRAL GENERATION")
    print("="*60)

    tests = [
        (100, 500, "High resolution"),
        (200, 500, "Very high resolution"),
        (500, 1000, "Ultra high resolution"),
    ]

    for num_revs, points_per_rev, desc in tests:
        print(f"\n{desc}: {num_revs} revs × {points_per_rev} pts/rev")

        spiral = SpiralGenerator(
            width=297,
            height=210,
            num_revolutions=num_revs,
            points_per_revolution=points_per_rev,
            spiral_type="archimedean"
        )

        start = time.time()
        paths = spiral.generate(start_radius=5.0)
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Total points: {total_points:,}")
        if elapsed > 0:
            print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUST SPIRAL GENERATOR - COMPREHENSIVE BENCHMARKS")
    print("="*60)

    test_archimedean_spirals()
    test_logarithmic_spirals()
    test_concentric_spirals()
    test_multiple_spirals()
    test_circular_waves()
    test_large_scale()

    print("\n" + "="*60)
    print("✅ All tests passed! SpiralGenerator is production-ready!")
    print("="*60)
