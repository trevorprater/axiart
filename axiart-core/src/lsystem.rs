//! High-performance L-System (Lindenmayer System) generator
//!
//! Generates fractal patterns and organic structures using string rewriting systems.
//! Supports turtle graphics interpretation for creating complex branching structures.

use pyo3::prelude::*;
use std::collections::HashMap;
use std::f64::consts::PI;

/// Turtle state for interpreting L-System commands
#[derive(Clone, Debug)]
struct TurtleState {
    x: f64,
    y: f64,
    angle: f64,
}

/// Preset L-System configurations
#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum LSystemPreset {
    KochCurve,
    KochSnowflake,
    SierpinskiTriangle,
    DragonCurve,
    HilbertCurve,
    Plant1,
    Plant2,
    BushyPlant,
    Custom,
}

#[pymethods]
impl LSystemPreset {
    #[staticmethod]
    fn from_str(s: &str) -> PyResult<Self> {
        match s.to_lowercase().as_str() {
            "koch_curve" | "koch" => Ok(LSystemPreset::KochCurve),
            "koch_snowflake" | "snowflake" => Ok(LSystemPreset::KochSnowflake),
            "sierpinski" | "sierpinski_triangle" => Ok(LSystemPreset::SierpinskiTriangle),
            "dragon" | "dragon_curve" => Ok(LSystemPreset::DragonCurve),
            "hilbert" | "hilbert_curve" => Ok(LSystemPreset::HilbertCurve),
            "plant1" | "plant" => Ok(LSystemPreset::Plant1),
            "plant2" => Ok(LSystemPreset::Plant2),
            "bushy" | "bushy_plant" => Ok(LSystemPreset::BushyPlant),
            "custom" => Ok(LSystemPreset::Custom),
            _ => Err(pyo3::exceptions::PyValueError::new_err(
                "Invalid preset. Use 'koch', 'snowflake', 'sierpinski', 'dragon', 'hilbert', 'plant1', 'plant2', 'bushy', or 'custom'",
            )),
        }
    }
}

/// High-performance L-System Generator
///
/// Creates fractal patterns using Lindenmayer systems with turtle graphics interpretation.
///
/// # Turtle Commands
/// - F: Move forward drawing a line
/// - f: Move forward without drawing
/// - +: Turn left by angle
/// - -: Turn right by angle
/// - [: Push state onto stack
/// - ]: Pop state from stack
///
/// # Examples
///
/// ```python
/// from axiart_core import LSystemGenerator
///
/// # Koch curve
/// lsys = LSystemGenerator(
///     width=297.0,
///     height=210.0,
///     preset="koch",
///     iterations=4
/// )
/// lines = lsys.generate()
///
/// # Custom L-System
/// lsys = LSystemGenerator.create_custom(
///     width=297.0,
///     height=210.0,
///     axiom="F",
///     rules={"F": "F+F-F-F+F"},
///     angle=90.0,
///     iterations=3
/// )
/// ```
#[pyclass]
pub struct LSystemGenerator {
    width: f64,
    height: f64,
    preset: LSystemPreset,
    axiom: String,
    rules: HashMap<char, String>,
    angle: f64,
    step_length: f64,
    iterations: usize,
    start_x: f64,
    start_y: f64,
    start_angle: f64,
}

#[pymethods]
impl LSystemGenerator {
    #[new]
    #[pyo3(signature = (
        width=297.0,
        height=210.0,
        preset="plant1",
        iterations=4,
        step_length=None,
        start_x=None,
        start_y=None,
        start_angle=None
    ))]
    fn new(
        width: f64,
        height: f64,
        preset: &str,
        iterations: usize,
        step_length: Option<f64>,
        start_x: Option<f64>,
        start_y: Option<f64>,
        start_angle: Option<f64>,
    ) -> PyResult<Self> {
        let preset_enum = LSystemPreset::from_str(preset)?;
        let (axiom, rules, angle, default_step, default_x, default_y, default_angle) =
            Self::get_preset_params(preset_enum, width, height);

        Ok(LSystemGenerator {
            width,
            height,
            preset: preset_enum,
            axiom,
            rules,
            angle,
            step_length: step_length.unwrap_or(default_step),
            iterations,
            start_x: start_x.unwrap_or(default_x),
            start_y: start_y.unwrap_or(default_y),
            start_angle: start_angle.unwrap_or(default_angle),
        })
    }

    /// Create a custom L-System
    #[staticmethod]
    #[pyo3(signature = (
        width=297.0,
        height=210.0,
        axiom="F",
        rules=None,
        angle=25.0,
        iterations=4,
        step_length=5.0,
        start_x=None,
        start_y=None,
        start_angle=90.0
    ))]
    fn create_custom(
        width: f64,
        height: f64,
        axiom: &str,
        rules: Option<HashMap<String, String>>,
        angle: f64,
        iterations: usize,
        step_length: f64,
        start_x: Option<f64>,
        start_y: Option<f64>,
        start_angle: f64,
    ) -> PyResult<Self> {
        let rules_map: HashMap<char, String> = rules
            .unwrap_or_default()
            .into_iter()
            .map(|(k, v)| (k.chars().next().unwrap(), v))
            .collect();

        Ok(LSystemGenerator {
            width,
            height,
            preset: LSystemPreset::Custom,
            axiom: axiom.to_string(),
            rules: rules_map,
            angle,
            step_length,
            iterations,
            start_x: start_x.unwrap_or(width / 2.0),
            start_y: start_y.unwrap_or(height / 2.0),
            start_angle,
        })
    }

    /// Generate the L-System pattern
    ///
    /// Returns a list of ((x1, y1), (x2, y2)) tuples representing line segments
    fn generate(&self) -> PyResult<Vec<((f64, f64), (f64, f64))>> {
        // Expand the L-System string
        let mut current = self.axiom.clone();
        for _ in 0..self.iterations {
            current = self.expand(&current);
        }

        // Interpret as turtle graphics
        let lines = self.interpret_turtle(&current);

        Ok(lines)
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

impl LSystemGenerator {
    /// Get preset parameters for known L-Systems
    fn get_preset_params(
        preset: LSystemPreset,
        width: f64,
        height: f64,
    ) -> (String, HashMap<char, String>, f64, f64, f64, f64, f64) {
        match preset {
            LSystemPreset::KochCurve => (
                "F".to_string(),
                [('F', "F+F-F-F+F".to_string())].iter().cloned().collect(),
                90.0,
                width / 100.0,
                width * 0.1,
                height / 2.0,
                0.0,
            ),
            LSystemPreset::KochSnowflake => (
                "F++F++F".to_string(),
                [('F', "F-F++F-F".to_string())].iter().cloned().collect(),
                60.0,
                width / 80.0,
                width * 0.2,
                height * 0.7,
                0.0,
            ),
            LSystemPreset::SierpinskiTriangle => (
                "F-G-G".to_string(),
                [('F', "F-G+F+G-F".to_string()), ('G', "GG".to_string())]
                    .iter()
                    .cloned()
                    .collect(),
                120.0,
                width / 100.0,
                width * 0.2,
                height * 0.8,
                0.0,
            ),
            LSystemPreset::DragonCurve => (
                "FX".to_string(),
                [('X', "X+YF+".to_string()), ('Y', "-FX-Y".to_string())]
                    .iter()
                    .cloned()
                    .collect(),
                90.0,
                width / 150.0,
                width * 0.4,
                height * 0.5,
                0.0,
            ),
            LSystemPreset::HilbertCurve => (
                "A".to_string(),
                [
                    ('A', "-BF+AFA+FB-".to_string()),
                    ('B', "+AF-BFB-FA+".to_string()),
                ]
                .iter()
                .cloned()
                .collect(),
                90.0,
                width / 100.0,
                width * 0.1,
                height * 0.9,
                0.0,
            ),
            LSystemPreset::Plant1 => (
                "X".to_string(),
                [
                    ('X', "F+[[X]-X]-F[-FX]+X".to_string()),
                    ('F', "FF".to_string()),
                ]
                .iter()
                .cloned()
                .collect(),
                25.0,
                width / 100.0,
                width / 2.0,
                height * 0.95,
                90.0,
            ),
            LSystemPreset::Plant2 => (
                "X".to_string(),
                [
                    ('X', "F-[[X]+X]+F[+FX]-X".to_string()),
                    ('F', "FF".to_string()),
                ]
                .iter()
                .cloned()
                .collect(),
                22.5,
                width / 120.0,
                width / 2.0,
                height,
                90.0,
            ),
            LSystemPreset::BushyPlant => (
                "F".to_string(),
                [('F', "FF+[+F-F-F]-[-F+F+F]".to_string())]
                    .iter()
                    .cloned()
                    .collect(),
                22.5,
                width / 120.0,
                width / 2.0,
                height,
                90.0,
            ),
            LSystemPreset::Custom => (
                "F".to_string(),
                HashMap::new(),
                25.0,
                5.0,
                width / 2.0,
                height / 2.0,
                90.0,
            ),
        }
    }

    /// Expand the L-System string by one iteration
    fn expand(&self, input: &str) -> String {
        let mut result = String::new();
        for c in input.chars() {
            if let Some(replacement) = self.rules.get(&c) {
                result.push_str(replacement);
            } else {
                result.push(c);
            }
        }
        result
    }

    /// Interpret L-System string as turtle graphics
    fn interpret_turtle(&self, commands: &str) -> Vec<((f64, f64), (f64, f64))> {
        let mut lines = Vec::new();
        let mut state = TurtleState {
            x: self.start_x,
            y: self.start_y,
            angle: self.start_angle,
        };
        let mut stack: Vec<TurtleState> = Vec::new();

        for c in commands.chars() {
            match c {
                'F' | 'G' => {
                    // Move forward and draw
                    let rad = state.angle * PI / 180.0;
                    let new_x = state.x + self.step_length * rad.cos();
                    let new_y = state.y - self.step_length * rad.sin(); // Negative because SVG y-axis goes down

                    lines.push(((state.x, state.y), (new_x, new_y)));

                    state.x = new_x;
                    state.y = new_y;
                }
                'f' => {
                    // Move forward without drawing
                    let rad = state.angle * PI / 180.0;
                    state.x += self.step_length * rad.cos();
                    state.y -= self.step_length * rad.sin();
                }
                '+' => {
                    // Turn left
                    state.angle += self.angle;
                }
                '-' => {
                    // Turn right
                    state.angle -= self.angle;
                }
                '[' => {
                    // Push state
                    stack.push(state.clone());
                }
                ']' => {
                    // Pop state
                    if let Some(prev_state) = stack.pop() {
                        state = prev_state;
                    }
                }
                _ => {
                    // Ignore other characters (like X, Y used in rules)
                }
            }
        }

        lines
    }
}
