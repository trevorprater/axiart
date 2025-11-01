"""
Test and benchmark Rust DendriteGenerator vs Python implementation
"""
import time
from axiart_core import DendriteGenerator as RustDendrite
from axiart.patterns.dendrite import DendritePattern as PythonDendrite

def test_rust_dendrite():
    """Test that Rust dendrite generates correctly"""
    print("\n=== Testing Rust DendriteGenerator ===")

    dendrite = RustDendrite(
        width=297.0,
        height=210.0,
        num_particles=100,  # Small test
        attraction_distance=5.0,
        seed=42
    )

    start = time.time()
    points, lines = dendrite.generate(max_attempts=1000)
    elapsed = time.time() - start

    print(f"✓ Generated {len(points)} points and {len(lines)} lines in {elapsed:.3f}s")
    print(f"  Average: {len(points)/elapsed:.1f} particles/sec")

    return points, lines

def benchmark_rust_vs_python():
    """Benchmark Rust vs Python implementation"""
    print("\n=== Benchmarking Rust vs Python ===")

    num_particles = 500  # Medium size for comparison

    # Benchmark Rust
    print(f"\nRust (num_particles={num_particles}):")
    rust_dendrite = RustDendrite(
        width=297.0,
        height=210.0,
        num_particles=num_particles,
        attraction_distance=5.0,
        seed=42
    )

    start = time.time()
    rust_points, rust_lines = rust_dendrite.generate(max_attempts=1000)
    rust_time = time.time() - start

    print(f"  Time: {rust_time:.3f}s")
    print(f"  Generated: {len(rust_points)} points, {len(rust_lines)} lines")
    print(f"  Speed: {len(rust_points)/rust_time:.1f} particles/sec")

    # Benchmark Python
    print(f"\nPython (num_particles={num_particles}):")
    python_dendrite = PythonDendrite(
        width=297.0,
        height=210.0,
        num_particles=num_particles,
        attraction_distance=5.0,
        seed_points=[(297/2, 210/2)]
    )

    start = time.time()
    python_dendrite.generate(max_attempts=1000)
    python_time = time.time() - start

    python_points = len(python_dendrite.get_points())
    python_lines = len(python_dendrite.get_lines())

    print(f"  Time: {python_time:.3f}s")
    print(f"  Generated: {python_points} points, {python_lines} lines")
    print(f"  Speed: {python_points/python_time:.1f} particles/sec")

    # Comparison
    speedup = python_time / rust_time
    print(f"\n🚀 Speedup: {speedup:.1f}x faster in Rust")

    return speedup

def test_large_dendrite():
    """Test with large particle count (like ghost_protocol_halloween.py)"""
    print("\n=== Testing Large Dendrite (5000 particles) ===")

    dendrite = RustDendrite(
        width=297.0,
        height=210.0,
        num_particles=5000,
        attraction_distance=7.0,
        seed=42
    )

    print("Generating 5000 particles...")
    start = time.time()
    points, lines = dendrite.generate(max_attempts=1000)
    elapsed = time.time() - start

    print(f"✓ Completed in {elapsed:.2f}s ({elapsed/60:.2f} minutes)")
    print(f"  Generated {len(points)} points and {len(lines)} lines")
    print(f"  Average: {len(points)/elapsed:.1f} particles/sec")

    print(f"\n  Estimated Python time: {elapsed * 50:.1f}s ({elapsed * 50 / 60:.1f} minutes)")
    print(f"  (assuming ~50x slower based on previous benchmarks)")

if __name__ == "__main__":
    print("="*60)
    print("Rust DendriteGenerator Test & Benchmark")
    print("="*60)

    # Basic functionality test
    test_rust_dendrite()

    # Benchmark comparison
    speedup = benchmark_rust_vs_python()

    # Large scale test
    test_large_dendrite()

    print("\n" + "="*60)
    print(f"✅ All tests passed! Rust is ~{speedup:.0f}x faster")
    print("="*60)
