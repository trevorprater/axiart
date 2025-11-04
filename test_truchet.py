#!/usr/bin/env python3
"""Benchmark: Truchet Tiles Pattern Performance"""

import time
from axiart.patterns import TruchetPattern


def benchmark_truchet():
    """Benchmark Truchet tile pattern generation."""

    print("=" * 60)
    print("TRUCHET TILES PATTERN BENCHMARK")
    print("=" * 60)

    # Test 1: Diagonal tiles (varying grid sizes)
    print("\n[Test 1] Diagonal Tiles")
    for grid_size in [20, 40, 60, 80]:
        start = time.time()
        pattern = TruchetPattern(
            width=297,
            height=210,
            tile_type="diagonal",
            grid_size=grid_size,
            randomness=0.5,
            seed=42
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        total_tiles = grid_size * grid_size
        print(f"  Grid: {grid_size}x{grid_size} ({total_tiles} tiles), Time: {elapsed:.3f}s, "
              f"Lines: {lines}, Rate: {total_tiles/elapsed:.0f} tiles/sec")

    # Test 2: Arc tiles
    print("\n[Test 2] Arc Tiles")
    for grid_size in [20, 30, 40, 50]:
        start = time.time()
        pattern = TruchetPattern(
            width=297,
            height=210,
            tile_type="arc",
            grid_size=grid_size,
            randomness=0.5,
            arc_segments=16,
            seed=42
        )
        pattern.generate()
        elapsed = time.time() - start

        curves = len(pattern.get_curves())
        total_tiles = grid_size * grid_size
        print(f"  Grid: {grid_size}x{grid_size} ({total_tiles} tiles), Time: {elapsed:.3f}s, "
              f"Curves: {curves}, Rate: {total_tiles/elapsed:.0f} tiles/sec")

    # Test 3: Double arc tiles
    print("\n[Test 3] Double Arc Tiles")
    for grid_size in [20, 30, 40, 50]:
        start = time.time()
        pattern = TruchetPattern(
            width=297,
            height=210,
            tile_type="double_arc",
            grid_size=grid_size,
            randomness=0.5,
            arc_segments=16,
            seed=42
        )
        pattern.generate()
        elapsed = time.time() - start

        curves = len(pattern.get_curves())
        total_tiles = grid_size * grid_size
        print(f"  Grid: {grid_size}x{grid_size} ({total_tiles} tiles), Time: {elapsed:.3f}s, "
              f"Curves: {curves}, Rate: {total_tiles/elapsed:.0f} tiles/sec")

    # Test 4: Arc segment quality test
    print("\n[Test 4] Arc Segment Quality (30x30 grid)")
    for segments in [8, 12, 16, 24, 32]:
        start = time.time()
        pattern = TruchetPattern(
            width=297,
            height=210,
            tile_type="arc",
            grid_size=30,
            randomness=0.5,
            arc_segments=segments,
            seed=42
        )
        pattern.generate()
        elapsed = time.time() - start

        curves = len(pattern.get_curves())
        print(f"  Segments: {segments}, Time: {elapsed:.3f}s, "
              f"Curves: {curves}, Rate: {curves/elapsed:.0f} curves/sec")

    # Test 5: Large grid stress test
    print("\n[Test 5] Large Grid Stress Test")
    for grid_size in [100, 150, 200]:
        start = time.time()
        pattern = TruchetPattern(
            width=297,
            height=210,
            tile_type="diagonal",
            grid_size=grid_size,
            randomness=1.0,
            seed=42
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        total_tiles = grid_size * grid_size
        print(f"  Grid: {grid_size}x{grid_size} ({total_tiles} tiles), Time: {elapsed:.3f}s, "
              f"Lines: {lines}, Rate: {total_tiles/elapsed:.0f} tiles/sec")

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    benchmark_truchet()
