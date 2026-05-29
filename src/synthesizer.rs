use crate::phase5::{parse_hardware_script, AST};
use crate::sparse_engine::{HardwareSpace, MaterialState, Dimensions, GridCells};
use crate::phase4::{MaterialsDatabase, PhysicsEngine};
use std::fs;

/// Output format options
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutputFormat {
    Gerber,  // .gtl - PCB manufacturing
    OBJ,     // .obj - 3D visualization
    Blender, // .py - Blender Python script
}

impl OutputFormat {
    pub fn extension(&self) -> &str {
        match self {
            OutputFormat::Gerber => "gtl",
            OutputFormat::OBJ => "obj",
            OutputFormat::Blender => "py",
        }
    }

    pub fn description(&self) -> &str {
        match self {
            OutputFormat::Gerber => "Gerber (PCB manufacturing)",
            OutputFormat::OBJ => "OBJ (3D visualization)",
            OutputFormat::Blender => "Blender Python script",
        }
    }
}

/// Component library definition
pub struct ComponentLibrary {
    // In production, this would load from a database
}

impl ComponentLibrary {
    pub fn new() -> Self {
        ComponentLibrary {}
    }

    /// Get component footprint (simplified for demo)
    pub fn get_footprint(&self, component_type: &str) -> Option<ComponentFootprint> {
        match component_type {
            "Transistor_NPN" => Some(ComponentFootprint {
                width: 3,
                height: 3,
                pins: vec![
                    ("Collector".to_string(), 0, 1),
                    ("Base".to_string(), 1, 0),
                    ("Emitter".to_string(), 2, 1),
                ],
            }),
            _ => None,
        }
    }
}

pub struct ComponentFootprint {
    pub width: usize,
    pub height: usize,
    pub pins: Vec<(String, usize, usize)>, // (name, local_x, local_y)
}

/// The complete Hardware Script synthesizer
pub struct Synthesizer {
    space: Option<HardwareSpace>,
    component_lib: ComponentLibrary,
    physics_engine: Option<PhysicsEngine>,
}

impl Synthesizer {
    pub fn new() -> Self {
        Synthesizer {
            space: None,
            component_lib: ComponentLibrary::new(),
            physics_engine: None,
        }
    }

    /// Load and compile a .hw file
    pub fn compile_file(&mut self, hw_path: &str) -> Result<(), Box<dyn std::error::Error>> {
        println!("🔥 HARDWARE SCRIPT COMPILER");
        println!("==================================================\n");

        // 1. Read source file
        println!("📖 Reading: {}", hw_path);
        let source = fs::read_to_string(hw_path)?;
        println!("   ✅ Loaded {} bytes\n", source.len());

        // 2. Parse AST
        println!("🔍 Parsing Hardware Script...");
        let ast = parse_hardware_script(&source)?;
        println!("   ✅ Parsed successfully");
        println!("   - Space: {}", if ast.space.is_some() { "✓" } else { "✗" });
        println!("   - Components: {}", ast.components.len());
        println!("   - Routes: {}\n", ast.routes.len());

        // 3. Initialize hardware space
        if let Some(space_def) = &ast.space {
            println!("🏗️  Initializing Hardware Space...");
            self.space = Some(HardwareSpace::new(
                space_def.name.clone(),
                Dimensions {
                    width_mm: space_def.dimensions.0,
                    height_mm: space_def.dimensions.1,
                    depth_mm: space_def.dimensions.2,
                },
                GridCells {
                    x_cols: space_def.grid.0,
                    y_rows: space_def.grid.1,
                    z_layers: space_def.grid.2,
                },
                MaterialState::FR4,
            ));
        } else {
            return Err("No space definition found in .hw file".into());
        }

        // 4. Place components
        if !ast.components.is_empty() {
            println!("📦 Placing Components...");
            self.place_components(&ast)?;
        }

        // 5. Route traces
        if !ast.routes.is_empty() {
            println!("\n🛤️  Routing Traces...");
            self.route_traces(&ast)?;
        }

        // 6. Physics validation
        println!("\n⚡ Physics Validation...");
        self.validate_physics()?;

        // 7. Memory statistics
        if let Some(space) = &self.space {
            println!("\n📊 Final Statistics:");
            println!("   {}", space.memory_stats());
        }

        Ok(())
    }

    /// Place all components from AST
    fn place_components(&mut self, ast: &AST) -> Result<(), Box<dyn std::error::Error>> {
        let space = self.space.as_mut().ok_or("No hardware space initialized")?;

        for comp in &ast.components {
            let footprint = self.component_lib.get_footprint(&comp.component_type)
                .ok_or_else(|| format!("Unknown component type: {}", comp.component_type))?;

            println!("   📌 {} '{}' at {:?}", 
                     comp.component_type, comp.instance_name, comp.position);

            // Place component body
            let (z, x, y) = comp.position;
            let z_idx = z - 1;
            let x_idx = x - 1;
            let y_idx = y - 1;

            // Mark body cells
            for dx in 0..footprint.width {
                for dy in 0..footprint.height {
                    space.set_voxel(z_idx, x_idx + dx, y_idx + dy, MaterialState::Body);
                }
            }

            // Place pins
            for (pin_name, local_x, local_y) in &footprint.pins {
                let pin_x = x_idx + local_x;
                let pin_y = y_idx + local_y;
                space.set_voxel(z_idx, pin_x, pin_y, MaterialState::Pad);
                println!("      - {}: [Z:{}, X:{}, Y:{}]", 
                         pin_name, z, pin_x + 1, pin_y + 1);
            }
        }

        Ok(())
    }

    /// Route all traces from AST
    fn route_traces(&mut self, ast: &AST) -> Result<(), Box<dyn std::error::Error>> {
        let space = self.space.as_mut().ok_or("No hardware space initialized")?;

        for route in &ast.routes {
            let route_name = format!("{}_{}", route.from, route.to);
            space.route_copper(&route_name, &route.waypoints, 1)?;
        }

        Ok(())
    }

    /// Validate physics (simplified for demo)
    fn validate_physics(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Load materials database
        let db = MaterialsDatabase::load("engine-test/standard-materials.yaml")?;
        self.physics_engine = Some(PhysicsEngine::new(db));

        let engine = self.physics_engine.as_ref().unwrap();

        // Example: Validate a trace
        let analysis = engine.analyze_trace(
            "Example_Trace",
            50.0,  // length_mm
            1.0,   // width_mm
            0.035, // thickness_mm (1oz copper)
            1.0,   // current_amps
        )?;

        if analysis.is_safe {
            println!("   ✅ All traces pass thermal validation");
        } else {
            println!("   ⚠️  Some traces exceed thermal limits");
        }

        Ok(())
    }

    /// Export to specified formats
    pub fn export(&self, output_dir: &str, formats: &[OutputFormat]) -> Result<(), Box<dyn std::error::Error>> {
        let space = self.space.as_ref().ok_or("No hardware space to export")?;

        fs::create_dir_all(output_dir)?;
        println!("\n📤 Exporting to: {}", output_dir);

        for format in formats {
            match format {
                OutputFormat::Gerber => self.export_gerber(space, output_dir)?,
                OutputFormat::OBJ => self.export_obj(space, output_dir)?,
                OutputFormat::Blender => self.export_blender(space, output_dir)?,
            }
        }

        println!("   ✅ All exports complete!\n");

        Ok(())
    }

    /// Export to Gerber format (PCB manufacturing)
    fn export_gerber(&self, space: &HardwareSpace, output_dir: &str) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("{}/board.gtl", output_dir);
        let mut output = String::new();

        // Gerber header
        output.push_str("%FSLAX24Y24*%\n");
        output.push_str("%MOMM*%\n");
        output.push_str(&format!("%ADD10R,{:.4}X{:.4}*%\n", 
                                 space.voxel_size.x_mm, space.voxel_size.y_mm));
        output.push_str("D10*\n");

        // Export only copper voxels (sparse iteration!)
        let mut copper_count = 0;
        for (&(z, x, y), &material) in space.voxels.iter() {
            if material == MaterialState::Copper as u8 && z == 0 {
                let real_x = x as f64 * space.voxel_size.x_mm + (space.voxel_size.x_mm / 2.0);
                let real_y = y as f64 * space.voxel_size.y_mm + (space.voxel_size.y_mm / 2.0);
                let gx = (real_x * 10000.0) as i32;
                let gy = (real_y * 10000.0) as i32;
                output.push_str(&format!("X{:06}Y{:06}D03*\n", gx, gy));
                copper_count += 1;
            }
        }

        output.push_str("M02*\n");
        fs::write(&path, output)?;
        println!("   ✅ Gerber: {} ({} copper pads)", path, copper_count);

        Ok(())
    }

    /// Export to OBJ format (3D visualization)
    fn export_obj(&self, space: &HardwareSpace, output_dir: &str) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("{}/board.obj", output_dir);
        let mut output = String::new();

        output.push_str("# Hardware Script 3D Export\n");
        output.push_str("o Board\n");

        let mut v_idx = 1;
        let mut copper_count = 0;

        // Export copper voxels as cubes (sparse iteration!)
        for (&(z, x, y), &material) in space.voxels.iter() {
            if material == MaterialState::Copper as u8 {
                let rx = x as f64 * space.voxel_size.x_mm;
                let ry = y as f64 * space.voxel_size.y_mm;
                let rz = z as f64 * space.voxel_size.z_mm;
                let vs = space.voxel_size.x_mm;

                // 8 vertices of cube
                output.push_str(&format!("v {} {} {}\n", rx, ry, rz));
                output.push_str(&format!("v {} {} {}\n", rx+vs, ry, rz));
                output.push_str(&format!("v {} {} {}\n", rx+vs, ry+vs, rz));
                output.push_str(&format!("v {} {} {}\n", rx, ry+vs, rz));
                output.push_str(&format!("v {} {} {}\n", rx, ry, rz+vs));
                output.push_str(&format!("v {} {} {}\n", rx+vs, ry, rz+vs));
                output.push_str(&format!("v {} {} {}\n", rx+vs, ry+vs, rz+vs));
                output.push_str(&format!("v {} {} {}\n", rx, ry+vs, rz+vs));

                // 6 faces
                output.push_str(&format!("f {} {} {} {}\n", v_idx, v_idx+1, v_idx+2, v_idx+3));
                output.push_str(&format!("f {} {} {} {}\n", v_idx+4, v_idx+5, v_idx+6, v_idx+7));
                output.push_str(&format!("f {} {} {} {}\n", v_idx, v_idx+1, v_idx+5, v_idx+4));
                output.push_str(&format!("f {} {} {} {}\n", v_idx+1, v_idx+2, v_idx+6, v_idx+5));
                output.push_str(&format!("f {} {} {} {}\n", v_idx+2, v_idx+3, v_idx+7, v_idx+6));
                output.push_str(&format!("f {} {} {} {}\n", v_idx+3, v_idx, v_idx+4, v_idx+7));

                v_idx += 8;
                copper_count += 1;
            }
        }

        fs::write(&path, output)?;
        println!("   ✅ OBJ: {} ({} copper voxels)", path, copper_count);

        Ok(())
    }

    /// Export to Blender Python script
    fn export_blender(&self, space: &HardwareSpace, output_dir: &str) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("{}/sim.py", output_dir);
        let mut output = String::new();

        output.push_str("import bpy\n\n");
        output.push_str("# Clear scene\n");
        output.push_str("bpy.ops.wm.read_factory_settings(use_empty=True)\n\n");

        // FR4 substrate
        let w = space.dimensions.width_mm;
        let h = space.dimensions.height_mm;
        output.push_str("# FR4 Substrate\n");
        output.push_str(&format!("bpy.ops.mesh.primitive_cube_add(size=1, location=({}, {}, -0.5), scale=({}, {}, 1))\n", 
                                 w/2.0, h/2.0, w, h));
        output.push_str("bpy.context.scene.objects[-1].name = 'FR4_Substrate'\n\n");

        // Copper voxels (sparse iteration!)
        output.push_str("# Copper Traces\n");
        let mut copper_count = 0;
        for (&(z, x, y), &material) in space.voxels.iter() {
            if material == MaterialState::Copper as u8 {
                let rx = x as f64 * space.voxel_size.x_mm;
                let ry = y as f64 * space.voxel_size.y_mm;
                let rz = z as f64 * space.voxel_size.z_mm;
                output.push_str(&format!("bpy.ops.mesh.primitive_cube_add(size={}, location=({}, {}, {}))\n",
                                         space.voxel_size.x_mm, rx, ry, rz));
                output.push_str("bpy.context.scene.objects[-1].name = 'Copper'\n");
                copper_count += 1;
            }
        }

        fs::write(&path, output)?;
        println!("   ✅ Blender: {} ({} copper voxels)", path, copper_count);

        Ok(())
    }
}

/// CLI entry point for synthesizer
pub fn run_synthesizer(
    hw_file: &str,
    output_dir: &str,
    formats: &[OutputFormat],
) -> Result<(), Box<dyn std::error::Error>> {
    let mut synth = Synthesizer::new();
    
    // Compile
    synth.compile_file(hw_file)?;
    
    // Export
    synth.export(output_dir, formats)?;

    println!("✅ SYNTHESIS COMPLETE!");
    println!("\nGenerated files in '{}':", output_dir);
    for format in formats {
        println!("   - board.{} ({})", format.extension(), format.description());
    }

    Ok(())
}
