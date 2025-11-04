#!/usr/bin/env python3
"""Benchmark: Voronoi Pattern Performance"""

import time
from axiart.patterns import VoronoiPattern


def benchmark_voronoi():
    """Benchmark Voronoi diagram generation."""

    print("=" * 60)
    print("VORONOI PATTERN BENCHMARK")
    print("=" * 60)

    # Test 1: Small number of sites
    print("\n[Test 1] 100 sites, no relaxation")
    start = time.time()
    voronoi = VoronoiPattern(
        width=297,
        height=210,
        num_sites=100,
        relaxation_iterations=0,
        seed=42
    )
    voronoi.generate()
    elapsed = time.time() - start

    sites = len(voronoi.get_sites())
    edges = len(voronoi.get_edges())
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Sites: {sites}, Edges: {edges}")
    print(f"  Performance: {sites/elapsed:.0f} sites/sec, {edges/elapsed:.0f} edges/sec")

    # Test 2: Medium number of sites
    print("\n[Test 2] 500 sites, no relaxation")
    start = time.time()
    voronoi = VoronoiPattern(
        width=297,
        height=210,
        num_sites=500,
        relaxation_iterations=0,
        seed=42
    )
    voronoi.generate()
    elapsed = time.time() - start

    sites = len(voronoi.get_sites())
    edges = len(voronoi.get_edges())
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Sites: {sites}, Edges: {edges}")
    print(f"  Performance: {sites/elapsed:.0f} sites/sec, {edges/elapsed:.0f} edges/sec")

    # Test 3: Large number of sites
    print("\n[Test 3] 1000 sites, no relaxation")
    start = time.time()
    voronoi = VoronoiPattern(
        width=297,
        height=210,
        num_sites=1000,
        relaxation_iterations=0,
        seed=42
    )
    voronoi.generate()
    elapsed = time.time() - start

    sites = len(voronoi.get_sites())
    edges = len(voronoi.get_edges())
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Sites: {sites}, Edges: {edges}")
    print(f"  Performance: {sites/elapsed:.0f} sites/sec, {edges/elapsed:.0f} edges/sec")

    # Test 4: With Lloyd's relaxation
    print("\n[Test 4] 200 sites, 5 relaxation iterations")
    start = time.time()
    voronoi = VoronoiPattern(
        width=297,
        height=210,
        num_sites=200,
        relaxation_iterations=5,
        seed=42
    )
    voronoi.generate()
    elapsed = time.time() - start

    sites = len(voronoi.get_sites())
    edges = len(voronoi.get_edges())
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Sites: {sites}, Edges: {edges}")
    print(f"  Performance: {sites/elapsed:.0f} sites/sec (with relaxation)")

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    benchmark_voronoi()
