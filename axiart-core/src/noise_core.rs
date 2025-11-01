//! High-performance Perlin noise implementation
//!
//! Shared noise generation core used by FlowFieldPattern and NoisePattern

use noise::{NoiseFn, Perlin};
use numpy::{PyArray1, PyArray2, PyArrayMethods, PyReadonlyArray1};
use pyo3::prelude::*;

/// High-performance Perlin Noise generator with octave support
///
/// This provides native Rust Perlin noise with batch evaluation support
/// for efficient grid-based noise generation. Supports multiple octaves
/// for fractal noise generation (Fractional Brownian Motion).
#[pyclass]
pub struct PerlinNoise {
    noise: Perlin,
    scale: f64,
    octaves: usize,
    persistence: f64,
    lacunarity: f64,
}

#[pymethods]
impl PerlinNoise {
    #[new]
    #[pyo3(signature = (scale=100.0, octaves=4, persistence=0.5, lacunarity=2.0, seed=0))]
    fn new(scale: f64, octaves: usize, persistence: f64, lacunarity: f64, seed: u32) -> Self {
        let noise = Perlin::new(seed);
        PerlinNoise {
            noise,
            scale,
            octaves,
            persistence,
            lacunarity,
        }
    }

    /// Evaluate noise at a single 2D point with octaves
    ///
    /// Uses Fractional Brownian Motion (fBm) to combine multiple octaves
    /// of Perlin noise for more detailed, natural-looking results.
    fn noise_2d(&self, x: f64, y: f64) -> f64 {
        self.fbm_2d(x, y)
    }

    /// Batch evaluate noise at multiple 2D points (returns NumPy array)
    fn noise_2d_batch<'py>(
        &self,
        py: Python<'py>,
        x: PyReadonlyArray1<f64>,
        y: PyReadonlyArray1<f64>,
    ) -> Bound<'py, PyArray1<f64>> {
        let x_slice = x.as_slice().unwrap();
        let y_slice = y.as_slice().unwrap();

        let result: Vec<f64> = x_slice
            .iter()
            .zip(y_slice.iter())
            .map(|(&xi, &yi)| self.fbm_2d(xi, yi))
            .collect();

        PyArray1::from_vec_bound(py, result)
    }

    /// Evaluate noise on a 2D grid (returns 2D NumPy array)
    ///
    /// This is optimized for generating contour maps and other grid-based patterns.
    fn noise_2d_grid<'py>(
        &self,
        py: Python<'py>,
        width: usize,
        height: usize,
        resolution: f64,
    ) -> Bound<'py, PyArray2<f64>> {
        let mut grid = Vec::with_capacity(height * width);

        for j in 0..height {
            for i in 0..width {
                let x = i as f64 * resolution;
                let y = j as f64 * resolution;
                grid.push(self.fbm_2d(x, y));
            }
        }

        // Create 2D array from flat vector
        let array = PyArray1::from_vec_bound(py, grid);
        array.reshape([height, width]).unwrap()
    }

    /// Get the current scale
    #[getter]
    fn scale(&self) -> f64 {
        self.scale
    }

    /// Get the number of octaves
    #[getter]
    fn octaves(&self) -> usize {
        self.octaves
    }

    /// Get the persistence value
    #[getter]
    fn persistence(&self) -> f64 {
        self.persistence
    }

    /// Get the lacunarity value
    #[getter]
    fn lacunarity(&self) -> f64 {
        self.lacunarity
    }
}

impl PerlinNoise {
    /// Fractional Brownian Motion (fBm) - combines multiple octaves of noise
    ///
    /// This creates more natural-looking, fractal noise by layering
    /// multiple frequencies (octaves) of Perlin noise with decreasing amplitude.
    fn fbm_2d(&self, x: f64, y: f64) -> f64 {
        let mut value = 0.0;
        let mut amplitude = 1.0;
        let mut frequency = 1.0;
        let mut max_value = 0.0;

        for _ in 0..self.octaves {
            let sample_x = (x / self.scale) * frequency;
            let sample_y = (y / self.scale) * frequency;

            value += self.noise.get([sample_x, sample_y]) * amplitude;
            max_value += amplitude;

            amplitude *= self.persistence;
            frequency *= self.lacunarity;
        }

        // Normalize to [-1, 1] range
        value / max_value
    }
}
