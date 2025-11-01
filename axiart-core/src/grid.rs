//! High-performance Grid pattern generation
//!
//! Fast geometric grid generation with distortions.
//! Pure geometric calculations - blazing fast in Rust.

use pyo3::prelude::*;
use std::f64::consts::PI;

/// Grid types
#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum GridType {
    Square,
    Hexagonal,
    Triangular,
}

#[pymethods]
impl GridType {
    #[staticmethod]
    fn from_str(s: &str) -> PyResult<Self> {
        match s.to_lowercase().as_str() {
            "square" => Ok(GridType::Square),
            "hexagonal" => Ok(GridType::Hexagonal),
            "triangular" => Ok(GridType::Triangular),
            _ => Err(pyo3::exceptions::PyValueError::new_err("Invalid grid type")),
        }
    }
}

/// High-performance Grid Generator
///
/// Fast geometric grid generation with optional distortions
#[pyclass]
pub struct GridGenerator {
    width: f64,
    height: f64,
}

#[pymethods]
impl GridGenerator {
    #[new]
    fn new(width: f64, height: f64) -> Self {
        GridGenerator { width, height }
    }

    /// Generate square grid
    #[pyo3(signature = (cell_size=10.0, jitter=0.0))]
    fn generate_square_grid(
        &self,
        cell_size: f64,
        jitter: f64,
    ) -> PyResult<Vec<Vec<(f64, f64)>>> {
        let mut lines = Vec::new();

        // Vertical lines
        let mut x = 0.0;
        while x <= self.width {
            let x_offset = if jitter > 0.0 {
                (rand::random::<f64>() - 0.5) * jitter
            } else {
                0.0
            };
            lines.push(vec![(x + x_offset, 0.0), (x + x_offset, self.height)]);
            x += cell_size;
        }

        // Horizontal lines
        let mut y = 0.0;
        while y <= self.height {
            let y_offset = if jitter > 0.0 {
                (rand::random::<f64>() - 0.5) * jitter
            } else {
                0.0
            };
            lines.push(vec![(0.0, y + y_offset), (self.width, y + y_offset)]);
            y += cell_size;
        }

        Ok(lines)
    }

    /// Generate hexagonal grid
    #[pyo3(signature = (cell_size=10.0))]
    fn generate_hexagonal_grid(&self, cell_size: f64) -> PyResult<Vec<Vec<(f64, f64)>>> {
        let mut lines = Vec::new();
        let h = cell_size * (3.0_f64.sqrt() / 2.0);

        let mut row = 0;
        let mut y = 0.0;
        while y < self.height + h {
            let x_offset = if row % 2 == 0 { 0.0 } else { cell_size / 2.0 };
            let mut x = x_offset;

            while x < self.width + cell_size {
                // Draw hexagon
                let hex_points = self.hexagon_points(x, y, cell_size / 2.0);
                lines.push(hex_points);
                x += cell_size;
            }

            y += h;
            row += 1;
        }

        Ok(lines)
    }

    /// Apply radial distortion to grid
    #[pyo3(signature = (lines, center=None, strength=0.5))]
    fn apply_radial_distortion(
        &self,
        lines: Vec<Vec<(f64, f64)>>,
        center: Option<(f64, f64)>,
        strength: f64,
    ) -> PyResult<Vec<Vec<(f64, f64)>>> {
        let cx = center.map(|c| c.0).unwrap_or(self.width / 2.0);
        let cy = center.map(|c| c.1).unwrap_or(self.height / 2.0);

        Ok(lines
            .into_iter()
            .map(|line| {
                line.into_iter()
                    .map(|(x, y)| {
                        let dx = x - cx;
                        let dy = y - cy;
                        let dist = (dx * dx + dy * dy).sqrt();
                        let factor = 1.0 + strength * (dist / 100.0);

                        (cx + dx * factor, cy + dy * factor)
                    })
                    .collect()
            })
            .collect())
    }
}

impl GridGenerator {
    /// Generate hexagon vertices
    fn hexagon_points(&self, cx: f64, cy: f64, radius: f64) -> Vec<(f64, f64)> {
        let mut points = Vec::with_capacity(7);

        for i in 0..=6 {
            let angle = PI / 3.0 * i as f64;
            let x = cx + radius * angle.cos();
            let y = cy + radius * angle.sin();
            points.push((x, y));
        }

        points
    }
}
