//! High-performance Truchet Tiles generator
//!
//! Generates geometric patterns using rotated tiles arranged on a grid.
//! Supports various tile types including diagonal lines, arcs, and multi-arc patterns.

use pyo3::prelude::*;
use rand::prelude::*;
use rand_chacha::ChaCha8Rng;
use std::f64::consts::PI;

/// Tile type for Truchet pattern
#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum TileType {
    Diagonal,
    Arc,
    DoubleArc,
    Triangle,
    Maze,
}

#[pymethods]
impl TileType {
    #[staticmethod]
    fn from_str(s: &str) -> PyResult<Self> {
        match s.to_lowercase().as_str() {
            "diagonal" => Ok(TileType::Diagonal),
            "arc" => Ok(TileType::Arc),
            "double_arc" | "doublearc" => Ok(TileType::DoubleArc),
            "triangle" => Ok(TileType::Triangle),
            "maze" => Ok(TileType::Maze),
            _ => Err(pyo3::exceptions::PyValueError::new_err(
                "Invalid tile type. Use 'diagonal', 'arc', 'double_arc', 'triangle', or 'maze'",
            )),
        }
    }
}

/// High-performance Truchet Tiles Generator
///
/// Creates geometric patterns by arranging rotated tiles on a grid.
/// Each tile can be rotated in 0°, 90°, 180°, or 270° orientations.
///
/// # Examples
///
/// ```python
/// from axiart_core import TruchetGenerator
///
/// # Arc-based Truchet pattern
/// truchet = TruchetGenerator(
///     width=297.0,
///     height=210.0,
///     tile_type="arc",
///     grid_size=20,
///     randomness=0.5
/// )
/// lines, curves = truchet.generate()
/// ```
#[pyclass]
pub struct TruchetGenerator {
    width: f64,
    height: f64,
    tile_type: TileType,
    grid_size: usize,
    tile_size: f64,
    randomness: f64,
    arc_segments: usize,
    rng: ChaCha8Rng,
}

#[pymethods]
impl TruchetGenerator {
    #[new]
    #[pyo3(signature = (
        width=297.0,
        height=210.0,
        tile_type="arc",
        grid_size=20,
        randomness=0.5,
        arc_segments=16,
        seed=None
    ))]
    fn new(
        width: f64,
        height: f64,
        tile_type: &str,
        grid_size: usize,
        randomness: f64,
        arc_segments: usize,
        seed: Option<u64>,
    ) -> PyResult<Self> {
        let tile_type_enum = TileType::from_str(tile_type)?;
        let tile_size = width.min(height) / grid_size as f64;

        let rng = if let Some(s) = seed {
            ChaCha8Rng::seed_from_u64(s)
        } else {
            ChaCha8Rng::from_entropy()
        };

        Ok(TruchetGenerator {
            width,
            height,
            tile_type: tile_type_enum,
            grid_size,
            tile_size,
            randomness: randomness.clamp(0.0, 1.0),
            arc_segments,
            rng,
        })
    }

    /// Generate the Truchet tile pattern
    ///
    /// Returns a tuple of (lines, curves) where:
    /// - lines: List of ((x1, y1), (x2, y2)) tuples for straight line segments
    /// - curves: List of polylines (list of (x, y) points) for curved segments
    ///
    /// For arc-based tiles, curves will contain the arc polylines.
    /// For diagonal tiles, lines will contain the diagonal segments.
    fn generate(&mut self) -> PyResult<(Vec<((f64, f64), (f64, f64))>, Vec<Vec<(f64, f64)>>)> {
        let mut lines = Vec::new();
        let mut curves = Vec::new();

        let cols = (self.width / self.tile_size).ceil() as usize;
        let rows = (self.height / self.tile_size).ceil() as usize;

        for row in 0..rows {
            for col in 0..cols {
                let x = col as f64 * self.tile_size;
                let y = row as f64 * self.tile_size;

                // Determine rotation (0, 1, 2, 3 for 0°, 90°, 180°, 270°)
                let rotation = if self.rng.gen::<f64>() < self.randomness {
                    self.rng.gen_range(0..4)
                } else {
                    // Use pattern based on position
                    (col + row) % 2
                };

                match self.tile_type {
                    TileType::Diagonal => {
                        self.generate_diagonal_tile(x, y, rotation, &mut lines);
                    }
                    TileType::Arc => {
                        self.generate_arc_tile(x, y, rotation, &mut curves);
                    }
                    TileType::DoubleArc => {
                        self.generate_double_arc_tile(x, y, rotation, &mut curves);
                    }
                    TileType::Triangle => {
                        self.generate_triangle_tile(x, y, rotation, &mut lines);
                    }
                    TileType::Maze => {
                        self.generate_maze_tile(x, y, rotation, &mut lines);
                    }
                }
            }
        }

        Ok((lines, curves))
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

impl TruchetGenerator {
    /// Generate a diagonal tile (line from one corner to opposite corner)
    fn generate_diagonal_tile(
        &self,
        x: f64,
        y: f64,
        rotation: usize,
        lines: &mut Vec<((f64, f64), (f64, f64))>,
    ) {
        let s = self.tile_size;
        let (p1, p2) = match rotation % 2 {
            0 => ((x, y), (x + s, y + s)), // Top-left to bottom-right
            _ => ((x + s, y), (x, y + s)), // Top-right to bottom-left
        };
        lines.push((p1, p2));
    }

    /// Generate an arc tile (quarter circle from one edge to adjacent edge)
    fn generate_arc_tile(
        &self,
        x: f64,
        y: f64,
        rotation: usize,
        curves: &mut Vec<Vec<(f64, f64)>>,
    ) {
        let s = self.tile_size;
        let mut points = Vec::new();

        // Generate arc based on rotation
        // Rotation determines which corner the arc curves around
        for i in 0..=self.arc_segments {
            let t = i as f64 / self.arc_segments as f64;
            let angle = t * PI / 2.0; // Quarter circle

            let (px, py) = match rotation {
                0 => {
                    // Arc from left edge to bottom edge, curved around bottom-left
                    (x + s * (1.0 - angle.cos()), y + s * angle.sin())
                }
                1 => {
                    // Arc from bottom edge to right edge, curved around bottom-right
                    (x + s * angle.sin(), y + s * (1.0 - angle.cos()))
                }
                2 => {
                    // Arc from right edge to top edge, curved around top-right
                    (x + s * angle.cos(), y + s * (1.0 - angle.sin()))
                }
                _ => {
                    // Arc from top edge to left edge, curved around top-left
                    (x + s * (1.0 - angle.sin()), y + s * angle.cos())
                }
            };

            points.push((px, py));
        }

        curves.push(points);
    }

    /// Generate a double arc tile (two quarter circles)
    fn generate_double_arc_tile(
        &self,
        x: f64,
        y: f64,
        rotation: usize,
        curves: &mut Vec<Vec<(f64, f64)>>,
    ) {
        let s = self.tile_size;

        // Two arcs per tile
        for arc_idx in 0..2 {
            let mut points = Vec::new();

            for i in 0..=self.arc_segments {
                let t = i as f64 / self.arc_segments as f64;
                let angle = t * PI / 2.0;

                let (px, py) = match (rotation, arc_idx) {
                    (0, 0) => (x + s * (1.0 - angle.cos()), y + s * angle.sin()),
                    (0, _) => (x + s * angle.cos(), y + s * (1.0 - angle.sin())),
                    (1, 0) => (x + s * angle.sin(), y + s * (1.0 - angle.cos())),
                    (1, _) => (x + s * (1.0 - angle.sin()), y + s * angle.cos()),
                    (2, 0) => (x + s * angle.cos(), y + s * (1.0 - angle.sin())),
                    (2, _) => (x + s * (1.0 - angle.cos()), y + s * angle.sin()),
                    _ => {
                        if arc_idx == 0 {
                            (x + s * (1.0 - angle.sin()), y + s * angle.cos())
                        } else {
                            (x + s * angle.sin(), y + s * (1.0 - angle.cos()))
                        }
                    }
                };

                points.push((px, py));
            }

            curves.push(points);
        }
    }

    /// Generate a triangle tile
    fn generate_triangle_tile(
        &self,
        x: f64,
        y: f64,
        rotation: usize,
        lines: &mut Vec<((f64, f64), (f64, f64))>,
    ) {
        let s = self.tile_size;

        let points = match rotation {
            0 => vec![(x, y), (x + s, y), (x, y + s)],
            1 => vec![(x + s, y), (x + s, y + s), (x, y + s)],
            2 => vec![(x + s, y + s), (x, y + s), (x + s, y)],
            _ => vec![(x, y + s), (x, y), (x + s, y + s)],
        };

        // Draw triangle edges
        for i in 0..points.len() {
            let p1 = points[i];
            let p2 = points[(i + 1) % points.len()];
            lines.push((p1, p2));
        }
    }

    /// Generate a maze-like tile (lines from center to edges)
    fn generate_maze_tile(
        &self,
        x: f64,
        y: f64,
        rotation: usize,
        lines: &mut Vec<((f64, f64), (f64, f64))>,
    ) {
        let s = self.tile_size;
        let cx = x + s / 2.0;
        let cy = y + s / 2.0;

        // Draw lines from center to specific edges based on rotation
        match rotation {
            0 => {
                lines.push(((cx, cy), (x, cy))); // Left
                lines.push(((cx, cy), (cx, y))); // Top
            }
            1 => {
                lines.push(((cx, cy), (cx, y))); // Top
                lines.push(((cx, cy), (x + s, cy))); // Right
            }
            2 => {
                lines.push(((cx, cy), (x + s, cy))); // Right
                lines.push(((cx, cy), (cx, y + s))); // Bottom
            }
            _ => {
                lines.push(((cx, cy), (cx, y + s))); // Bottom
                lines.push(((cx, cy), (x, cy))); // Left
            }
        }
    }
}
