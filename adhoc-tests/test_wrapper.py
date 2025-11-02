"""Quick test of the Rust-accelerated dendrite wrapper"""

import time
from axiart.patterns.dendrite import DendritePattern

print("Testing Rust-accelerated DendritePattern wrapper...")
print("=" * 60)

dendrite = DendritePattern(
    width=297,
    height=210,
    num_particles=1000,
    attraction_distance=5.0
)

start = time.time()
dendrite.generate()
elapsed = time.time() - start

points = dendrite.get_points()
lines = dendrite.get_lines()

print(f"✅ Generated {len(points)} points and {len(lines)} lines")
print(f"⏱️  Time: {elapsed:.3f}s ({len(points)/elapsed:.0f} particles/sec)")
print(f"🚀 Using Rust: {dendrite._use_rust}")
print("=" * 60)
