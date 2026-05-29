use ndarray::Array3;
use std::collections::HashMap;

/// Extended cell states for component placement
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum CellState {
    Empty = 0,
    FR4 = 1,
    Copper = 2,
    Silicon = 3,
    Pad = 4,     // Component connection point (routeable)
    Body = 5,    // Component keep-out zone (blocks routing)
}

impl From<u8> for CellState {
    fn from(value: u8) -> Self {
        match value {
            0 => CellState::Empty,
            1 => CellState::FR4,
            2 => CellState::Copper,
            3 => CellState::Silicon,
            4 => CellState::Pad,
            5 => CellState::Body,
            _ => CellState::Empty,
        }
    }
}

/// Pin definition with local coordinates
#[derive(Debug, Clone)]
pub struct Pin {
    pub name: String,
    pub local_x: usize,
    pub local_y: usize,
}

/// Component definition from standard library
#[derive(Debug, Clone)]
pub struct ComponentDef {
    pub name: String,
    pub width: usize,   // Grid cells
    pub height: usize,  // Grid cells
    pub pins: Vec<Pin>,
}

impl ComponentDef {
    pub fn new(name: String, width: usize, height: usize) -> Self {
        ComponentDef {
            name,
            width,
            height,
            pins: Vec::new(),
        }
    }

    pub fn add_pin(&mut self, name: String, local_x: usize, local_y: usize) {
        self.pins.push(Pin { name, local_x, local_y });
    }
}

/// Rotation directions
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Rotation {
    North,  // 0°   - Default
    East,   // 90°  - Clockwise
    South,  // 180°
    West,   // 270° - Counter-clockwise
}

impl Rotation {
    pub fn from_str(s: &str) -> Result<Self, String> {
        match s {
            "North" => Ok(Rotation::North),
            "East" => Ok(Rotation::East),
            "South" => Ok(Rotation::South),
            "West" => Ok(Rotation::West),
            _ => Err(format!("Invalid rotation direction: {}", s)),
        }
    }
}

/// Physical dimensions and grid
#[derive(Debug, Clone, Copy)]
pub struct Dimensions {
    pub width_mm: f64,
    pub height_mm: f64,
    pub depth_mm: f64,
}

#[derive(Debug, Clone, Copy)]
pub struct GridCells {
    pub x_cols: usize,
    pub y_rows: usize,
    pub z_layers: usize,
}

/// Hardware space with component placement capabilities
pub struct HardwareSpace {
    pub name: String,
    pub dimensions: Dimensions,
    pub grid: GridCells,
    pub tensor: Array3<u8>,
}

impl HardwareSpace {
    pub fn new(name: String, dimensions: Dimensions, grid: GridCells) -> Self {
        // Initialize with FR4 substrate
        let tensor = Array3::<u8>::from_elem(
            (grid.z_layers, grid.x_cols, grid.y_rows),
            CellState::FR4 as u8,
        );

        HardwareSpace {
            name,
            dimensions,
            grid,
            tensor,
        }
    }

    /// Rotate local component coordinates based on direction
    /// Assumes [0,0] is Top-Left
    fn rotate_coords(
        &self,
        local_x: usize,
        local_y: usize,
        comp_width: usize,
        comp_height: usize,
        rotation: Rotation,
    ) -> (usize, usize) {
        match rotation {
            Rotation::North => (local_x, local_y),
            Rotation::East => (comp_height - 1 - local_y, local_x),
            Rotation::South => (comp_width - 1 - local_x, comp_height - 1 - local_y),
            Rotation::West => (local_y, comp_width - 1 - local_x),
        }
    }

    /// Calculate bounding box dimensions after rotation
    fn rotated_dimensions(&self, width: usize, height: usize, rotation: Rotation) -> (usize, usize) {
        match rotation {
            Rotation::North | Rotation::South => (width, height),
            Rotation::East | Rotation::West => (height, width), // Swap dimensions
        }
    }

    /// Place a component at specified position with rotation
    /// Position is 1-indexed: (Z_layer, X_col, Y_row)
    pub fn place_component(
        &mut self,
        comp: &ComponentDef,
        instance_name: &str,
        pos: (usize, usize, usize),
        rotation: Rotation,
    ) -> Result<(), String> {
        let (z_layer, x_pos, y_pos) = pos;

        // Validate layer bounds
        if z_layer == 0 || z_layer > self.grid.z_layers {
            return Err(format!(
                "Layer {} out of bounds (1-{})",
                z_layer, self.grid.z_layers
            ));
        }

        // Convert to 0-indexed
        let z_idx = z_layer - 1;
        let x_origin = x_pos - 1;
        let y_origin = y_pos - 1;

        // Calculate rotated bounding box
        let (new_width, new_height) = self.rotated_dimensions(comp.width, comp.height, rotation);

        // Validate position bounds
        if x_origin + new_width > self.grid.x_cols || y_origin + new_height > self.grid.y_rows {
            return Err(format!(
                "Component '{}' at position {:?} exceeds board boundaries",
                instance_name, pos
            ));
        }

        // COLLISION DETECTION: Check if target area is clear
        for x in x_origin..x_origin + new_width {
            for y in y_origin..y_origin + new_height {
                let cell_state = CellState::from(self.tensor[[z_idx, x, y]]);
                if cell_state == CellState::Body || cell_state == CellState::Pad {
                    return Err(format!(
                        "Collision detected when placing '{}' at {:?}",
                        instance_name, pos
                    ));
                }
            }
        }

        // CLAIM THE BODY (Keep-out zone)
        for x in x_origin..x_origin + new_width {
            for y in y_origin..y_origin + new_height {
                self.tensor[[z_idx, x, y]] = CellState::Body as u8;
            }
        }

        println!("\n📦 Component Placed: '{}' ({})", instance_name, comp.name);
        println!("   Orientation : {:?}", rotation);
        println!(
            "   Global Bounding Box : X[{} to {}], Y[{} to {}]",
            x_origin,
            x_origin + new_width - 1,
            y_origin,
            y_origin + new_height - 1
        );

        // MAP AND PLACE THE PINS
        println!("   Pin Global Coordinates:");
        for pin in &comp.pins {
            // Apply rotation math
            let (rot_x, rot_y) = self.rotate_coords(
                pin.local_x,
                pin.local_y,
                comp.width,
                comp.height,
                rotation,
            );

            // Translate to global coordinates
            let global_x = x_origin + rot_x;
            let global_y = y_origin + rot_y;

            // Mark the specific cell as a PAD (routeable)
            self.tensor[[z_idx, global_x, global_y]] = CellState::Pad as u8;

            // Print output (+1 to match Hardware Script 1-index)
            println!(
                "      - {}: [Z:{}, X:{}, Y:{}]",
                pin.name,
                z_layer,
                global_x + 1,
                global_y + 1
            );
        }

        Ok(())
    }
}

/// Demo function for Phase 2
pub fn run_phase2_demo() {
    println!("--- PHASE 2: COMPONENT PLACEMENT & COLLISION DETECTION ---\n");

    // 1. Initialize Space
    let mut board = HardwareSpace::new(
        "SprinklerController".to_string(),
        Dimensions {
            width_mm: 50.0,
            height_mm: 50.0,
            depth_mm: 2.0,
        },
        GridCells {
            x_cols: 50,
            y_rows: 50,
            z_layers: 2,
        },
    );

    // 2. Load Standard Library Component: Transistor_NPN (3x3 grid footprint)
    let mut transistor_def = ComponentDef::new("Transistor_NPN".to_string(), 3, 3);
    transistor_def.add_pin("Collector".to_string(), 0, 1);
    transistor_def.add_pin("Base".to_string(), 1, 0);
    transistor_def.add_pin("Emitter".to_string(), 2, 1);

    // 3. Execute Hardware Script Commands
    board
        .place_component(&transistor_def, "Switch1", (1, 10, 10), Rotation::North)
        .unwrap();

    board
        .place_component(&transistor_def, "Switch2", (1, 20, 20), Rotation::East)
        .unwrap();

    board
        .place_component(&transistor_def, "Switch3", (1, 30, 30), Rotation::South)
        .unwrap();

    // 4. Test collision detection
    println!("\n⚠️  Testing Collision Engine...");
    match board.place_component(&transistor_def, "CrashTransistor", (1, 11, 10), Rotation::North) {
        Ok(_) => println!("❌ ERROR: Collision detection failed!"),
        Err(e) => println!("✅ {}", e),
    }
}
