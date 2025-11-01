//! High-performance Spiral pattern generation
//!
//! Fast geometric calculations for spirals and concentric circles.
//! Already fast in Python (using numpy), but Rust eliminates all overhead.

use pyo3::prelude::*;
use std::f64::consts::PI;

/// Spiral types
#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum SpiralType {
    Archimedean,  // Linear growth
    Logarithmic,  // Exponential growth
    Concentric,   // Discrete circles
}

#[pymethods]
impl SpiralType {
    #[staticmethod]
    fn from_str(s: &str) -> PyResult<Self> {
        match s.to_lowercase().as_str() {
            "archimedean" => Ok(SpiralType::Archimedean),
            "logarithmic" => Ok(SpiralType::Logarithmic),
            "concentric" => Ok(SpiralType::Concentric),
            _ => Err(pyo3::exceptions::PyValueError::new_err(
                "Invalid spiral type",
            )),
        }
    }
}

/// High-performance Spiral Generator
///
/// Fast geometric spiral generation - already efficient in Python,
/// but Rust eliminates all interpreter overhead.
#[pyclass]
pub struct SpiralGenerator {
    width: f64,
    height: f64,
    center: (f64, f64),
    num_revolutions: usize,
    points_per_revolution: usize,
    spiral_type: SpiralType,
}

#[pymethods]
impl SpiralGenerator {
    #[new]
    #[pyo3(signature = (
        width=297.0,
        height=210.0,
        center=None,
        num_revolutions=20,
        points_per_revolution=100,
        spiral_type="archimedean"
    ))]
    fn new(
        width: f64,
        height: f64,
        center: Option<(f64, f64)>,
        num_revolutions: usize,
        points_per_revolution: usize,
        spiral_type: &str,
    ) -> PyResult<Self> {
        let stype = SpiralType::from_str(spiral_type)?;
        let actual_center = center.unwrap_or((width / 2.0, height / 2.0));

        Ok(SpiralGenerator {
            width,
            height,
            center: actual_center,
            num_revolutions,
            points_per_revolution,
            spiral_type: stype,
        })
    }

    /// Generate spiral pattern(s)
    ///
    /// Returns list of spiral paths
    #[pyo3(signature = (
        start_radius=5.0,
        end_radius=None,
        rotation_offset=0.0,
        growth_factor=1.0,
        num_spirals=1,
        angular_offset=0.0
    ))]
    fn generate(
        &self,
        start_radius: f64,
        end_radius: Option<f64>,
        rotation_offset: f64,
        growth_factor: f64,
        num_spirals: usize,
        angular_offset: f64,
    ) -> PyResult<Vec<Vec<(f64, f64)>>> {
        // Calculate max radius if not provided
        let max_radius = end_radius.unwrap_or_else(|| {
            let dx = [self.center.0, self.width - self.center.0];
            let dy = [self.center.1, self.height - self.center.1];
            dx.iter().chain(dy.iter()).fold(f64::INFINITY, |a, &b| a.min(b)) * 0.9
        });

        let total_points = self.num_revolutions * self.points_per_revolution;
        let mut spirals = Vec::new();

        for spiral_idx in 0..num_spirals {
            let mut points = Vec::with_capacity(total_points);
            let offset_angle = angular_offset * spiral_idx as f64;

            for i in 0..total_points {
                let theta = (i as f64 / self.points_per_revolution as f64) * 2.0 * PI
                    + rotation_offset
                    + offset_angle;
                let t = i as f64 / total_points as f64;

                let r = match self.spiral_type {
                    SpiralType::Archimedean => {
                        start_radius + (max_radius - start_radius) * t * growth_factor
                    }
                    SpiralType::Logarithmic => {
                        let b = (max_radius / start_radius).ln()
                            / (self.num_revolutions as f64 * 2.0 * PI);
                        start_radius * (b * theta * growth_factor).exp()
                    }
                    SpiralType::Concentric => {
                        let revolution = i / self.points_per_revolution;
                        start_radius
                            + (max_radius - start_radius)
                                * (revolution as f64 / self.num_revolutions as f64)
                                * growth_factor
                    }
                };

                let x = self.center.0 + r * theta.cos();
                let y = self.center.1 + r * theta.sin();
                points.push((x, y));
            }

            spirals.push(points);
        }

        Ok(spirals)
    }

    /// Generate circular waves with optional undulation
    #[pyo3(signature = (
        num_circles=20,
        start_radius=10.0,
        end_radius=None,
        points_per_circle=100,
        wave_amplitude=0.0,
        wave_frequency=5.0
    ))]
    fn generate_circular_waves(
        &self,
        num_circles: usize,
        start_radius: f64,
        end_radius: Option<f64>,
        points_per_circle: usize,
        wave_amplitude: f64,
        wave_frequency: f64,
    ) -> PyResult<Vec<Vec<(f64, f64)>>> {
        let max_radius = end_radius.unwrap_or_else(|| {
            let dx = [self.center.0, self.width - self.center.0];
            let dy = [self.center.1, self.height - self.center.1];
            dx.iter().chain(dy.iter()).fold(f64::INFINITY, |a, &b| a.min(b)) * 0.9
        });

        let mut circles = Vec::new();

        for circle_idx in 0..num_circles {
            let mut points = Vec::with_capacity(points_per_circle + 1);
            let base_radius = start_radius
                + (max_radius - start_radius) * (circle_idx as f64 / num_circles as f64);

            for i in 0..=points_per_circle {
                let theta = (i as f64 / points_per_circle as f64) * 2.0 * PI;
                let r = base_radius + wave_amplitude * (wave_frequency * theta).sin();

                let x = self.center.0 + r * theta.cos();
                let y = self.center.1 + r * theta.sin();
                points.push((x, y));
            }

            circles.push(points);
        }

        Ok(circles)
    }
}
