use ndarray::Array3;

/// Material state representation using enum for type safety
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum MaterialState {
    Empty = 0,
    FR4 = 1,      // Fiberglass Substrate
    Copper = 2,   // Conductive Routing/Planes
    Silicon = 3,  // Semiconductor Base
}

impl From<u8> for MaterialState {
    fn from(value: u8) -> Self {
        match value {
            0 => MaterialState::Empty,
            1 => MaterialState::FR4,
            2 => MaterialState::Copper,
            3 => MaterialState::Silicon,
            _ => MaterialState::Empty,
        }
    }
}

/// Physical dimensions in millimeters
#[derive(Debug, Clone, Copy)]
pub struct Dimensions {
    pub width_mm: f64,
    pub height_mm: f64,
    pub depth_mm: f64,
}

/// Grid resolution (number of cells)
#[derive(Debug, Clone, Copy)]
pub struct GridCells {
    pub x_cols: usize,
    pub y_rows: usize,
    pub z_layers: usize,
}

/// Voxel resolution (size of each cell in mm)
#[derive(Debug, Clone, Copy)]
pub struct VoxelSize {
    pub x_mm: f64,
    pub y_mm: f64,
    pub z_mm: f64,
}

/// The main 3D hardware space representation
pub struct HardwareSpace {
    pub name: String,
    pub dimensions: Dimensions,
    pub grid: GridCells,
    pub voxel_size: VoxelSize,
    /// 3D tensor grid using [Z, X, Y] ordering to match Hardware Script syntax
    /// Using ndarray for efficient multi-dimensional operations
    pub tensor: Array3<u8>,
}

impl HardwareSpace {
    /// Creates a new hardware space with calculated voxel resolution
    pub fn new(name: String, dimensions: Dimensions, grid: GridCells) -> Self {
        // Calculate voxel resolution
        let voxel_size = VoxelSize {
            x_mm: dimensions.width_mm / grid.x_cols as f64,
            y_mm: dimensions.height_mm / grid.y_rows as f64,
            z_mm: dimensions.depth_mm / grid.z_layers as f64,
        };

        // Create 3D tensor filled with Empty (air)
        let tensor = Array3::<u8>::zeros((grid.z_layers, grid.x_cols, grid.y_rows));

        println!("✅ Space '{}' initialized.", name);
        println!("   Dimensions : {:.1}x{:.1}x{:.1} mm", 
                 dimensions.width_mm, dimensions.height_mm, dimensions.depth_mm);
        println!("   Grid       : {}x{}x{} cells", 
                 grid.x_cols, grid.y_rows, grid.z_layers);
        println!("   Voxel Size : {:.3}x{:.3}x{:.3} mm per cell\n", 
                 voxel_size.x_mm, voxel_size.y_mm, voxel_size.z_mm);

        HardwareSpace {
            name,
            dimensions,
            grid,
            voxel_size,
            tensor,
        }
    }

    /// Fills the entire 3D space with a material
    pub fn add_spanning_all(&mut self, material: MaterialState) {
        self.tensor.fill(material as u8);
        println!("🔧 Action: Filled 'all' layers with Material {:?}", material);
    }

    /// Fills a specific Z-layer with a material
    /// Note: layer is 1-indexed (Hardware Script convention)
    pub fn add_spanning_layer(&mut self, material: MaterialState, layer: usize) {
        if layer == 0 || layer > self.grid.z_layers {
            panic!("❌ Fatal Error: Layer {} out of bounds (1-{})", 
                   layer, self.grid.z_layers);
        }

        let z_index = layer - 1; // Convert to 0-indexed
        let mut layer_slice = self.tensor.slice_mut(ndarray::s![z_index, .., ..]);
        layer_slice.fill(material as u8);
        
        println!("🔧 Action: Filled 'layer {}' with Material {:?}", layer, material);
    }

    /// Inspects a layer and reports its material composition
    pub fn inspect_layer(&self, layer: usize) {
        if layer == 0 || layer > self.grid.z_layers {
            println!("❌ Error: Layer {} out of bounds", layer);
            return;
        }

        let z_index = layer - 1;
        let layer_slice = self.tensor.slice(ndarray::s![z_index, .., ..]);
        
        // Find unique materials in this layer
        let mut materials = std::collections::HashSet::new();
        for &value in layer_slice.iter() {
            materials.insert(value);
        }

        println!("\n🔍 Inspection of Layer {}:", layer);
        print!("   Materials present: ");
        for mat in &materials {
            print!("{:?} ", MaterialState::from(*mat));
        }
        println!();

        // Check for solid copper plane
        if materials.len() == 1 && materials.contains(&(MaterialState::Copper as u8)) {
            println!("   Status: Solid Copper Plane (Warning: Vias require explicit clearance!)");
        }
    }
}

/// Demo function simulating the parsed .hw file
pub fn run_phase1_demo() {
    println!("--- PHASE 1: MATERIAL DEFINITIONS & 3D TENSOR GRID ---\n");
    
    /*
    Simulating this Hardware Script:
    
    define Space "SprinklerController":
        dimensions: 50mm by 50mm by 2mm
        grid: 50 by 50 by 4  # 4-layer PCB
        
        # Base fiberglass board
        add Substrate(FR4) spanning all
        
        # Inner sandwich Ground and Power planes
        add Copper named GroundPlane spanning layer 2
        add Copper named PowerPlane spanning layer 3
    */

    // 1. Instantiate the Space
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

    // 2. Add the base fiberglass (spanning all)
    board.add_spanning_all(MaterialState::FR4);

    // 3. Add the explicit internal Copper Planes
    board.add_spanning_layer(MaterialState::Copper, 2);
    board.add_spanning_layer(MaterialState::Copper, 3);

    // 4. Verify the physical reality in memory
    board.inspect_layer(1); // Should be just FR4
    board.inspect_layer(2); // Should be solid Copper
}
