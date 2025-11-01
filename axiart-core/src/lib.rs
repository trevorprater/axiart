//! AxiArt Core - High-performance generative art algorithms in Rust
//!
//! This crate provides optimized implementations of pattern generation algorithms
//! for creating algorithmic artwork optimized for pen plotters like AxiDraw V3.
//!
//! # Performance
//!
//! All algorithms are implemented with performance in mind:
//! - Spatial indexing (KD-trees) for O(n log n) nearest neighbor searches
//! - SIMD-optimized noise generation
//! - Parallel processing using rayon where applicable
//! - Zero-copy NumPy array integration where possible

use pyo3::prelude::*;

mod dendrite;
mod noise_core;
mod flow_field;
mod noise_pattern;
mod spiral;
mod grid;

/// AxiArt Core - Python module for high-performance pattern generation
#[pymodule]
fn axiart_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<dendrite::DendriteGenerator>()?;
    m.add_class::<dendrite::BranchingStyle>()?;
    m.add_class::<noise_core::PerlinNoise>()?;
    m.add_class::<flow_field::FlowFieldGenerator>()?;
    m.add_class::<flow_field::FieldType>()?;
    m.add_class::<noise_pattern::NoisePatternGenerator>()?;
    m.add_class::<spiral::SpiralGenerator>()?;
    m.add_class::<grid::GridGenerator>()?;

    Ok(())
}
