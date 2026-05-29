use ndarray::Array3;

/// Extended cell states including vias
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum CellState {
    Empty = 0,
    FR4 = 1,
    Copper = 2,
    Silicon = 3,
    Pad = 4,
    Body = 5,
    Hole = 6,  // Drilled Via connecting layers
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
            6 => CellState::Hole,
            _ => CellState::Empty,
        }
    }
}

/// Physical dimensions
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

/// Waypoint in 3D space (1-indexed coordinates)
pub type Waypoint = (usize, usize, usize);

/// Route definition
#[derive(Debug, Clone)]
pub struct Route {
    pub name: String,
    pub waypoints: Vec<Waypoint>,
    pub clearance: usize,
}

/// Hardware space with routing capabilities
pub struct HardwareSpace {
    pub name: String,
    pub dimensions: Dimensions,
    pub grid: GridCells,
    pub tensor: Array3<u8>,
}

impl HardwareSpace {
    pub fn new(name: String, dimensions: Dimensions, grid: GridCells) -> Self {
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

    /// Bresenham's line algorithm for 2D trace routing
    /// Returns list of (x, y) coordinates forming a line
    fn bresenham_line(&self, x0: usize, y0: usize, x1: usize, y1: usize) -> Vec<(usize, usize)> {
        let mut points = Vec::new();
        
        let dx = (x1 as i32 - x0 as i32).abs();
        let dy = (y1 as i32 - y0 as i32).abs();
        
        let sx = if x0 < x1 { 1 } else { -1 };
        let sy = if y0 < y1 { 1 } else { -1 };
        
        let mut x = x0 as i32;
        let mut y = y0 as i32;
        let mut err = dx - dy;

        loop {
            points.push((x as usize, y as usize));
            
            if x == x1 as i32 && y == y1 as i32 {
                break;
            }
            
            let e2 = 2 * err;
            
            if e2 > -dy {
                err -= dy;
                x += sx;
            }
            
            if e2 < dx {
                err += dx;
                y += sy;
            }
        }
        
        points
    }

    /// Route copper traces through waypoints
    pub fn route_copper(&mut self, route: &Route) -> Result<(), String> {
        println!("\n🛤️  Routing: '{}'", route.name);

        for i in 0..route.waypoints.len() - 1 {
            let p1 = route.waypoints[i];
            let p2 = route.waypoints[i + 1];

            // Validate waypoints
            if p1.0 == 0 || p1.0 > self.grid.z_layers || p2.0 == 0 || p2.0 > self.grid.z_layers {
                return Err(format!("Waypoint layer out of bounds: {:?} or {:?}", p1, p2));
            }

            // Convert to 0-indexed
            let z1 = p1.0 - 1;
            let x1 = p1.1 - 1;
            let y1 = p1.2 - 1;
            let z2 = p2.0 - 1;
            let x2 = p2.1 - 1;
            let y2 = p2.2 - 1;

            // SCENARIO A: Same layer routing (2D Copper Trace)
            if z1 == z2 {
                println!(
                    "   -> Drawing trace on Layer {} from X:{},Y:{} to X:{},Y:{}",
                    p1.0, p1.1, p1.2, p2.1, p2.2
                );

                let line_cells = self.bresenham_line(x1, y1, x2, y2);

                for (cx, cy) in line_cells {
                    let current_state = CellState::from(self.tensor[[z1, cx, cy]]);

                    // Collision Engine: Copper cannot run through a Component Body!
                    if current_state == CellState::Body {
                        return Err(format!(
                            "Fatal Routing Error: Trace '{}' hit a component body at [Z:{}, X:{}, Y:{}]",
                            route.name,
                            p1.0,
                            cx + 1,
                            cy + 1
                        ));
                    }

                    self.tensor[[z1, cx, cy]] = CellState::Copper as u8;
                }
            }
            // SCENARIO B: Layer Change (Vertical Via)
            else {
                // Via must be vertical (same X,Y coordinates)
                if x1 != x2 || y1 != y2 {
                    return Err(format!(
                        "Fatal Routing Error: Invalid Via from {:?} to {:?}. X and Y must be identical when changing Z-layers!",
                        p1, p2
                    ));
                }

                println!(
                    "   -> Drilling VIA at X:{},Y:{} from Layer {} to {}",
                    p1.1, p1.2, p1.0, p2.0
                );

                // Determine drill direction
                let step: i32 = if z2 > z1 { 1 } else { -1 };
                let mut z_current = z1 as i32;
                let z_end = z2 as i32;

                while z_current != z_end + step {
                    let z_idx = z_current as usize;

                    // Apply clearance if requested (anti-pad for inner layers)
                    if route.clearance > 0 && z_idx != z1 && z_idx != z2 {
                        // Clear a square around the via
                        let clear = route.clearance;
                        for dx in 0..=clear * 2 {
                            for dy in 0..=clear * 2 {
                                let clear_x = x1.saturating_sub(clear) + dx;
                                let clear_y = y1.saturating_sub(clear) + dy;
                                
                                if clear_x < self.grid.x_cols && clear_y < self.grid.y_rows {
                                    self.tensor[[z_idx, clear_x, clear_y]] = CellState::FR4 as u8;
                                }
                            }
                        }
                    }

                    // Drill the via hole
                    self.tensor[[z_idx, x1, y1]] = CellState::Hole as u8;
                    z_current += step;
                }
            }
        }

        println!("   ✅ Route '{}' successfully laid.", route.name);
        Ok(())
    }

    /// Manually place a component body for testing
    pub fn place_body(&mut self, z: usize, x_start: usize, x_end: usize, y_start: usize, y_end: usize) {
        let z_idx = z - 1;
        for x in x_start - 1..x_end {
            for y in y_start - 1..y_end {
                if x < self.grid.x_cols && y < self.grid.y_rows {
                    self.tensor[[z_idx, x, y]] = CellState::Body as u8;
                }
            }
        }
    }
}

/// Demo function for Phase 3
pub fn run_phase3_demo() {
    println!("--- PHASE 3: ROUTING ENGINE & VIA DRILLING ---\n");

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
            z_layers: 4,
        },
    );

    // 2. Manually place a component body to test collision
    println!("📦 Placing test component body at [1, 15-17, 11-13]");
    board.place_body(1, 15, 17, 11, 13);

    // 3. Test valid route with via
    println!("\n✅ Testing Valid Route with Via...");
    let valid_route = Route {
        name: "Power_To_Valve".to_string(),
        waypoints: vec![
            (1, 10, 11),  // Start on layer 1
            (1, 12, 11),  // Move right
            (1, 12, 15),  // Move down (avoiding component body)
            (1, 20, 15),  // Move right past component
            (2, 20, 15),  // Drill via to layer 2
        ],
        clearance: 1,
    };

    match board.route_copper(&valid_route) {
        Ok(_) => println!("   ✅ Route completed successfully"),
        Err(e) => println!("   ❌ {}", e),
    }

    // 4. Test invalid via (diagonal drill)
    println!("\n⚠️  Testing Invalid Via Rule (Diagonal Drill)...");
    let bad_via_route = Route {
        name: "Bad_Via_Test".to_string(),
        waypoints: vec![
            (1, 5, 5),
            (2, 6, 6),  // Cannot change X/Y while changing Z
        ],
        clearance: 0,
    };

    match board.route_copper(&bad_via_route) {
        Ok(_) => println!("   ❌ ERROR: Should have failed!"),
        Err(e) => println!("   ✅ {}", e),
    }

    // 5. Test trace collision with component body
    println!("\n⚠️  Testing Trace Collision with Component Body...");
    let collision_route = Route {
        name: "Collision_Test".to_string(),
        waypoints: vec![
            (1, 10, 12),
            (1, 20, 12),  // Drives straight through component body!
        ],
        clearance: 0,
    };

    match board.route_copper(&collision_route) {
        Ok(_) => println!("   ❌ ERROR: Should have detected collision!"),
        Err(e) => println!("   ✅ {}", e),
    }
}
