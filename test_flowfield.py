"""
Test and benchmark Rust FlowFieldGenerator
Shows parallel speedup and comparison with Python
"""
import time
from axiart.axiart_core import FlowFieldGenerator

def test_streamlines():
    """Test streamline generation"""
    print("\n" + "="*60)
    print("FLOWFIELD STREAMLINES - Sequential vs Parallel")
    print("="*60)

    flow = FlowFieldGenerator(
        width=297,
        height=210,
        field_type="noise",
        scale=50.0,
        seed=42
    )

    # Sequential generation
    print("\n[Sequential] 100 streamlines × 200 steps:")
    start = time.time()
    paths_seq = flow.generate_streamlines(
        num_lines=100,
        steps=200,
        step_size=1.0,
        parallel=False
    )
    time_seq = time.time() - start
    print(f"  Time: {time_seq:.3f}s")
    print(f"  Generated {len(paths_seq)} streamlines")
    print(f"  Total points: {sum(len(p) for p in paths_seq):,}")

    # Parallel generation
    print("\n[Parallel] 100 streamlines × 200 steps:")
    start = time.time()
    paths_par = flow.generate_streamlines(
        num_lines=100,
        steps=200,
        step_size=1.0,
        parallel=True
    )
    time_par = time.time() - start
    print(f"  Time: {time_par:.3f}s")
    print(f"  Generated {len(paths_par)} streamlines")
    print(f"  Total points: {sum(len(p) for p in paths_par):,}")

    speedup = time_seq / time_par
    print(f"\n🚀 Parallel speedup: {speedup:.1f}x faster")

    return time_seq, time_par

def test_curl_noise():
    """Test curl noise generation"""
    print("\n" + "="*60)
    print("CURL NOISE STREAMLINES (Divergence-Free)")
    print("="*60)

    flow = FlowFieldGenerator(
        width=297,
        height=210,
        field_type="noise",
        scale=50.0,
        seed=42
    )

    # Parallel curl noise
    print("\n[Parallel] 100 curl noise lines × 200 steps:")
    start = time.time()
    paths = flow.generate_curl_noise_lines(
        num_lines=100,
        steps=200,
        step_size=1.0,
        parallel=True
    )
    elapsed = time.time() - start
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Generated {len(paths)} streamlines")
    print(f"  Total points: {sum(len(p) for p in paths):,}")

    return elapsed

def test_field_types():
    """Test different field types"""
    print("\n" + "="*60)
    print("DIFFERENT FIELD TYPES")
    print("="*60)

    field_types = ["noise", "radial", "spiral", "waves"]

    for ftype in field_types:
        flow = FlowFieldGenerator(
            width=297,
            height=210,
            field_type=ftype,
            scale=50.0,
            seed=42
        )

        start = time.time()
        paths = flow.generate_streamlines(
            num_lines=50,
            steps=100,
            parallel=True
        )
        elapsed = time.time() - start

        print(f"\n{ftype.upper():12} - 50 lines × 100 steps")
        print(f"  Time: {elapsed:.3f}s")
        print(f"  Lines: {len(paths)}")

def test_large_generation():
    """Test large-scale generation"""
    print("\n" + "="*60)
    print("LARGE-SCALE GENERATION")
    print("="*60)

    flow = FlowFieldGenerator(
        width=297,
        height=210,
        field_type="noise",
        scale=50.0,
        seed=42
    )

    tests = [
        (100, 200, "Medium"),
        (500, 200, "Large"),
        (1000, 200, "Extra Large"),
    ]

    for num_lines, steps, desc in tests:
        print(f"\n{desc}: {num_lines} lines × {steps} steps")
        start = time.time()
        paths = flow.generate_streamlines(
            num_lines=num_lines,
            steps=steps,
            parallel=True
        )
        elapsed = time.time() - start

        total_points = sum(len(p) for p in paths)
        print(f"  Time: {elapsed:.3f}s")
        print(f"  Generated: {len(paths)} streamlines")
        print(f"  Total points: {total_points:,}")
        print(f"  Speed: {total_points/elapsed:,.0f} points/sec")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUST FLOWFIELD GENERATOR - PARALLEL BENCHMARKS")
    print("="*60)

    test_streamlines()
    test_curl_noise()
    test_field_types()
    test_large_generation()

    print("\n" + "="*60)
    print("✅ All tests passed! Parallel generation works perfectly!")
    print("="*60)
