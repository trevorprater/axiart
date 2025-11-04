//! High-performance Voronoi diagram generator
//!
//! Generates Voronoi diagrams using a sampling-based approach optimized for pen plotting.
//! Supports Lloyd's relaxation for more uniform cell distribution.

use pyo3::prelude::*;
use rand::prelude::*;
use rand_chacha::ChaCha8Rng;
use std::collections::HashSet;

/// High-performance Voronoi Diagram Generator
///
/// Creates cellular patterns by dividing space into regions based on distance to sites.
/// Optimized for pen plotting with clean edge detection.
///
/// # Examples
///
/// ```python
/// from axiart_core import VoronoiGenerator
///
/// voronoi = VoronoiGenerator(
///     width=297.0,
///     height=210.0,
///     num_sites=100,
///     relaxation_iterations=2
/// )
/// sites, edges = voronoi.generate()
/// ```
#[pyclass]
pub struct VoronoiGenerator {
    width: f64,
    height: f64,
    num_sites: usize,
    relaxation_iterations: usize,
    clip_to_bounds: bool,
    sampling_resolution: usize,
    rng: ChaCha8Rng,
}

#[pymethods]
impl VoronoiGenerator {
    #[new]
    #[pyo3(signature = (
        width=297.0,
        height=210.0,
        num_sites=100,
        relaxation_iterations=0,
        clip_to_bounds=true,
        sampling_resolution=800,
        seed=None
    ))]
    fn new(
        width: f64,
        height: f64,
        num_sites: usize,
        relaxation_iterations: usize,
        clip_to_bounds: bool,
        sampling_resolution: usize,
        seed: Option<u64>,
    ) -> PyResult<Self> {
        let rng = if let Some(s) = seed {
            ChaCha8Rng::seed_from_u64(s)
        } else {
            ChaCha8Rng::from_entropy()
        };

        Ok(VoronoiGenerator {
            width,
            height,
            num_sites,
            relaxation_iterations,
            clip_to_bounds,
            sampling_resolution,
            rng,
        })
    }

    /// Generate the Voronoi diagram
    ///
    /// Returns a tuple of (sites, edges) where:
    /// - sites: List of (x, y) coordinates for Voronoi sites
    /// - edges: List of ((x1, y1), (x2, y2)) tuples representing cell boundaries
    ///
    /// Uses sampling-based edge detection for clean pen-plotter output.
    fn generate(&mut self) -> PyResult<(Vec<(f64, f64)>, Vec<((f64, f64), (f64, f64))>)> {
        // Generate initial random sites
        let mut sites: Vec<(f64, f64)> = (0..self.num_sites)
            .map(|_| {
                (
                    self.rng.gen::<f64>() * self.width,
                    self.rng.gen::<f64>() * self.height,
                )
            })
            .collect();

        // Apply Lloyd's relaxation if requested
        for _ in 0..self.relaxation_iterations {
            sites = self.lloyd_relaxation(&sites);
        }

        // Generate edges using sampling-based approach
        let edges = self.detect_edges(&sites);

        Ok((sites, edges))
    }

    /// Get the width of the canvas
    #[getter]
    fn width(&self) -> f64 {
        self.width
    }

    /// Get the height of the canvas
    #[getter]
    fn height(&self) -> f64 {
        self.height
    }
}

impl VoronoiGenerator {
    /// Find the nearest site to a given point
    fn nearest_site(&self, x: f64, y: f64, sites: &[(f64, f64)]) -> usize {
        sites
            .iter()
            .enumerate()
            .map(|(idx, &(sx, sy))| {
                let dist_sq = (x - sx).powi(2) + (y - sy).powi(2);
                (idx, dist_sq)
            })
            .min_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
            .unwrap()
            .0
    }

    /// Perform one iteration of Lloyd's relaxation
    ///
    /// Moves each site to the centroid of its Voronoi cell
    fn lloyd_relaxation(&self, sites: &[(f64, f64)]) -> Vec<(f64, f64)> {
        let sample_points = 50; // samples per site for centroid calculation

        let mut new_sites = vec![(0.0, 0.0); sites.len()];
        let mut counts = vec![0; sites.len()];

        // Sample the space uniformly
        let step = (self.width.max(self.height)
            / (sample_points as f64 * (sites.len() as f64).sqrt()))
        .max(1.0);
        let mut x = 0.0;
        while x < self.width {
            let mut y = 0.0;
            while y < self.height {
                let nearest = self.nearest_site(x, y, sites);
                new_sites[nearest].0 += x;
                new_sites[nearest].1 += y;
                counts[nearest] += 1;
                y += step;
            }
            x += step;
        }

        // Calculate centroids
        for i in 0..sites.len() {
            if counts[i] > 0 {
                new_sites[i].0 /= counts[i] as f64;
                new_sites[i].1 /= counts[i] as f64;

                // Keep within bounds
                new_sites[i].0 = new_sites[i].0.clamp(0.0, self.width);
                new_sites[i].1 = new_sites[i].1.clamp(0.0, self.height);
            } else {
                new_sites[i] = sites[i]; // Keep original if no samples
            }
        }

        new_sites
    }

    /// Detect Voronoi edges using sampling approach
    ///
    /// Samples the space at high resolution and detects boundaries where
    /// the nearest site changes.
    fn detect_edges(&self, sites: &[(f64, f64)]) -> Vec<((f64, f64), (f64, f64))> {
        let mut edges = Vec::new();
        let step = self.width.max(self.height) / self.sampling_resolution as f64;

        // Create a grid to store which site owns each cell
        let grid_w = (self.width / step).ceil() as usize + 1;
        let grid_h = (self.height / step).ceil() as usize + 1;
        let mut grid = vec![vec![None; grid_h]; grid_w];

        // Fill grid with nearest site indices
        for i in 0..grid_w {
            for j in 0..grid_h {
                let x = (i as f64 * step).min(self.width);
                let y = (j as f64 * step).min(self.height);
                grid[i][j] = Some(self.nearest_site(x, y, sites));
            }
        }

        // Detect edges by looking for neighboring cells with different sites
        let mut edge_set = HashSet::new();

        for i in 0..grid_w - 1 {
            for j in 0..grid_h - 1 {
                let current = grid[i][j].unwrap();

                // Check right neighbor
                if i < grid_w - 1 {
                    let right = grid[i + 1][j].unwrap();
                    if current != right {
                        let x = (i as f64 + 0.5) * step;
                        let y1 = j as f64 * step;
                        let y2 = ((j + 1) as f64 * step).min(self.height);

                        if !self.clip_to_bounds
                            || (x <= self.width && y1 >= 0.0 && y2 <= self.height)
                        {
                            // Create canonical edge representation (ordered points)
                            let edge = if (x, y1) < (x, y2) {
                                ((x, y1), (x, y2))
                            } else {
                                ((x, y2), (x, y1))
                            };
                            edge_set.insert((
                                (edge.0 .0 * 1000.0) as i64,
                                (edge.0 .1 * 1000.0) as i64,
                                (edge.1 .0 * 1000.0) as i64,
                                (edge.1 .1 * 1000.0) as i64,
                            ));
                        }
                    }
                }

                // Check bottom neighbor
                if j < grid_h - 1 {
                    let bottom = grid[i][j + 1].unwrap();
                    if current != bottom {
                        let x1 = i as f64 * step;
                        let x2 = ((i + 1) as f64 * step).min(self.width);
                        let y = (j as f64 + 0.5) * step;

                        if !self.clip_to_bounds
                            || (y <= self.height && x1 >= 0.0 && x2 <= self.width)
                        {
                            // Create canonical edge representation (ordered points)
                            let edge = if (x1, y) < (x2, y) {
                                ((x1, y), (x2, y))
                            } else {
                                ((x2, y), (x1, y))
                            };
                            edge_set.insert((
                                (edge.0 .0 * 1000.0) as i64,
                                (edge.0 .1 * 1000.0) as i64,
                                (edge.1 .0 * 1000.0) as i64,
                                (edge.1 .1 * 1000.0) as i64,
                            ));
                        }
                    }
                }
            }
        }

        // Convert back to float edges
        for &(x1i, y1i, x2i, y2i) in edge_set.iter() {
            edges.push((
                (x1i as f64 / 1000.0, y1i as f64 / 1000.0),
                (x2i as f64 / 1000.0, y2i as f64 / 1000.0),
            ));
        }

        edges
    }
}
