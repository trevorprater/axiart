#!/usr/bin/env python3
"""Benchmark: L-System Pattern Performance"""

import time
from axiart.patterns import LSystemPattern


def benchmark_lsystem():
    """Benchmark L-System pattern generation."""

    print("=" * 60)
    print("L-SYSTEM PATTERN BENCHMARK")
    print("=" * 60)

    # Test 1: Koch Curve (exponential growth)
    print("\n[Test 1] Koch Curve")
    for iterations in [3, 4, 5, 6]:
        start = time.time()
        pattern = LSystemPattern(
            width=297,
            height=210,
            preset="koch",
            iterations=iterations
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        print(f"  Iterations: {iterations}, Time: {elapsed:.3f}s, Lines: {lines}, "
              f"Rate: {lines/elapsed:.0f} lines/sec")

    # Test 2: Dragon Curve
    print("\n[Test 2] Dragon Curve")
    for iterations in [8, 10, 12, 14]:
        start = time.time()
        pattern = LSystemPattern(
            width=297,
            height=210,
            preset="dragon",
            iterations=iterations
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        print(f"  Iterations: {iterations}, Time: {elapsed:.3f}s, Lines: {lines}, "
              f"Rate: {lines/elapsed:.0f} lines/sec")

    # Test 3: Plant (with branching)
    print("\n[Test 3] Plant Pattern")
    for iterations in [3, 4, 5, 6]:
        start = time.time()
        pattern = LSystemPattern(
            width=297,
            height=210,
            preset="plant1",
            iterations=iterations
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        print(f"  Iterations: {iterations}, Time: {elapsed:.3f}s, Lines: {lines}, "
              f"Rate: {lines/elapsed:.0f} lines/sec")

    # Test 4: Hilbert Curve
    print("\n[Test 4] Hilbert Curve")
    for iterations in [3, 4, 5, 6]:
        start = time.time()
        pattern = LSystemPattern(
            width=297,
            height=210,
            preset="hilbert",
            iterations=iterations
        )
        pattern.generate()
        elapsed = time.time() - start

        lines = len(pattern.get_lines())
        print(f"  Iterations: {iterations}, Time: {elapsed:.3f}s, Lines: {lines}, "
              f"Rate: {lines/elapsed:.0f} lines/sec")

    # Test 5: Custom L-System (complex rules)
    print("\n[Test 5] Custom Complex Pattern")
    start = time.time()
    pattern = LSystemPattern.create_custom(
        width=297,
        height=210,
        axiom="F",
        rules={"F": "FF+[+F-F-F]-[-F+F+F]"},
        angle=25.0,
        iterations=5,
        step_length=2.0
    )
    pattern.generate()
    elapsed = time.time() - start

    lines = len(pattern.get_lines())
    print(f"  Time: {elapsed:.3f}s, Lines: {lines}, Rate: {lines/elapsed:.0f} lines/sec")

    print("\n" + "=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    benchmark_lsystem()
