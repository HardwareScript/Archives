use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

/// Material properties for conductors
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct ConductorProperties {
    pub name: String,
    pub symbol: String,
    pub resistivity_ohm_m: f64,
    pub max_current_density_a_mm2: f64,
    pub thermal_conductivity_w_mk: f64,
    pub melting_point_c: f64,
    #[serde(default)]
    pub description: String,
}

/// Material properties for insulators
#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct InsulatorProperties {
    pub name: String,
    pub symbol: String,
    pub relative_permittivity: f64,
    pub dielectric_strength_kv_mm: f64,
    pub thermal_conductivity_w_mk: f64,
    #[serde(default)]
    pub description: String,
}

/// Materials database structure matching YAML
#[derive(Debug, Deserialize, Serialize)]
pub struct MaterialsDatabase {
    pub conductors: HashMap<String, ConductorProperties>,
    pub insulators: HashMap<String, InsulatorProperties>,
}

impl MaterialsDatabase {
    /// Load materials database from YAML file
    pub fn load(path: &str) -> Result<Self, String> {
        println!("📚 Loading Materials Database from {}...", path);
        
        let contents = fs::read_to_string(path)
            .map_err(|e| format!("Failed to read file: {}", e))?;
        
        let db: MaterialsDatabase = serde_yaml::from_str(&contents)
            .map_err(|e| format!("Failed to parse YAML: {}", e))?;
        
        println!("   ✅ Loaded {} conductors, {} insulators",
                 db.conductors.len(), db.insulators.len());
        
        Ok(db)
    }

    /// Get conductor properties by name
    pub fn get_conductor(&self, name: &str) -> Result<&ConductorProperties, String> {
        self.conductors.get(name)
            .ok_or_else(|| format!("Conductor '{}' not found in database", name))
    }
}

/// Physics analysis results
#[derive(Debug)]
#[allow(dead_code)]
pub struct TraceAnalysis {
    pub trace_name: String,
    pub length_mm: f64,
    pub width_mm: f64,
    pub thickness_mm: f64,
    pub current_amps: f64,
    pub resistance_ohms: f64,
    pub voltage_drop_v: f64,
    pub power_dissipation_w: f64,
    pub current_density_a_mm2: f64,
    pub is_safe: bool,
}

/// Physics engine for electrical calculations
pub struct PhysicsEngine {
    db: MaterialsDatabase,
}

impl PhysicsEngine {
    /// Create new physics engine with materials database
    pub fn new(db: MaterialsDatabase) -> Self {
        PhysicsEngine { db }
    }

    /// Analyze a copper trace for electrical properties
    /// 
    /// # Five Core Laws Applied:
    /// 1. Resistance: R = ρ × (L/A)
    /// 2. Ohm's Law: V = I × R
    /// 3. Power: P = I² × R
    /// 4. Current Density: J = I / A
    /// 5. Thermal Limit: J < J_max
    pub fn analyze_trace(
        &self,
        trace_name: &str,
        length_mm: f64,
        width_mm: f64,
        thickness_mm: f64,
        current_amps: f64,
    ) -> Result<TraceAnalysis, String> {
        println!("\n⚡ Physics Analysis: Route '{}'", trace_name);
        println!("   Geometry: {:.2}mm(L) x {:.2}mm(W) x {:.3}mm(T)",
                 length_mm, width_mm, thickness_mm);

        // Fetch copper properties from database
        let copper = self.db.get_conductor("copper")?;
        let rho = copper.resistivity_ohm_m;
        let max_density = copper.max_current_density_a_mm2;

        // Convert to meters for SI calculations
        let length_m = length_mm * 1e-3;
        let width_m = width_mm * 1e-3;
        let thickness_m = thickness_mm * 1e-3;
        let area_m2 = width_m * thickness_m;

        // LAW 1: Resistance (R = ρ × L/A)
        let resistance_ohms = rho * (length_m / area_m2);
        println!("   Calculated Resistance : {:.6} Ω", resistance_ohms);

        // LAW 2: Ohm's Law (V = I × R)
        let voltage_drop_v = current_amps * resistance_ohms;
        println!("   Voltage Drop          : {:.6} V (at {:.2}A)", 
                 voltage_drop_v, current_amps);

        // LAW 3: Power Dissipation (P = I² × R)
        let power_dissipation_w = current_amps.powi(2) * resistance_ohms;
        println!("   Power Dissipation     : {:.6} W", power_dissipation_w);

        // LAW 4: Current Density (J = I / A)
        let area_mm2 = width_mm * thickness_mm;
        let current_density_a_mm2 = current_amps / area_mm2;
        println!("   Current Density       : {:.2} A/mm² (Limit: {:.0} A/mm²)",
                 current_density_a_mm2, max_density);

        // LAW 5: Thermal Safety Check
        let is_safe = current_density_a_mm2 <= max_density;
        
        if is_safe {
            println!("   ✅ Thermal Check Passed. Trace is operating safely.");
        } else {
            println!("   ❌ THERMAL FAILURE: Current density {:.2} A/mm² exceeds safe limit of {:.0} A/mm²",
                     current_density_a_mm2, max_density);
            println!("   💡 Suggestion: Increase trace width or reduce current.");
        }

        Ok(TraceAnalysis {
            trace_name: trace_name.to_string(),
            length_mm,
            width_mm,
            thickness_mm,
            current_amps,
            resistance_ohms,
            voltage_drop_v,
            power_dissipation_w,
            current_density_a_mm2,
            is_safe,
        })
    }

    /// Validate if a trace is safe for given current
    pub fn validate_trace_safety(
        &self,
        trace_name: &str,
        length_mm: f64,
        width_mm: f64,
        thickness_mm: f64,
        current_amps: f64,
    ) -> Result<(), String> {
        let analysis = self.analyze_trace(trace_name, length_mm, width_mm, thickness_mm, current_amps)?;
        
        if !analysis.is_safe {
            return Err(format!(
                "FATAL THERMAL ERROR: Trace '{}' will melt! Current density of {:.2} A/mm² exceeds safe limit.",
                trace_name, analysis.current_density_a_mm2
            ));
        }
        
        Ok(())
    }
}

/// Demo function for Phase 4
pub fn run_phase4_demo() {
    println!("--- PHASE 4: PHYSICS ENGINE & MATERIALS DATABASE ---\n");

    // 1. Load materials database
    let db = match MaterialsDatabase::load("engine-test/standard-materials.yaml") {
        Ok(db) => db,
        Err(e) => {
            println!("❌ Error loading database: {}", e);
            return;
        }
    };

    // 2. Create physics engine
    let engine = PhysicsEngine::new(db);

    // Trace specifications
    // Standard 1oz copper: 0.035mm thick
    // 1mm wide trace, 50mm long
    let trace_length = 50.0;
    let trace_width = 1.0;
    let trace_thickness = 0.035;

    // Test Scenario 1: Safe current (1 Amp - typical for small motor)
    println!("\n✅ Test 1: Safe Operating Current");
    match engine.analyze_trace(
        "Safe_Motor_Power",
        trace_length,
        trace_width,
        trace_thickness,
        1.0,
    ) {
        Ok(analysis) => {
            if analysis.is_safe {
                println!("   ✅ Test PASSED: Trace is safe");
            } else {
                println!("   ❌ Test FAILED: Trace should be safe");
            }
        }
        Err(e) => println!("   ❌ Error: {}", e),
    }

    // Test Scenario 2: Dangerous current (50 Amps through tiny trace!)
    println!("\n⚠️  Test 2: Dangerous Overcurrent");
    match engine.validate_trace_safety(
        "Dangerous_Main_Power",
        trace_length,
        trace_width,
        trace_thickness,
        50.0,
    ) {
        Ok(_) => println!("   ❌ Test FAILED: Should have detected thermal failure"),
        Err(e) => {
            println!("   ✅ Test PASSED: Correctly detected thermal failure");
            println!("   {}", e);
        }
    }

    // Test Scenario 3: Edge case - exactly at limit
    println!("\n⚙️  Test 3: Operating at Maximum Safe Current");
    let area_mm2 = trace_width * trace_thickness;
    let max_safe_current = 35.0 * area_mm2; // 35 A/mm² is copper's limit
    
    match engine.analyze_trace(
        "Edge_Case_Max_Current",
        trace_length,
        trace_width,
        trace_thickness,
        max_safe_current,
    ) {
        Ok(analysis) => {
            println!("   Max safe current for this trace: {:.4} A", max_safe_current);
            if analysis.is_safe {
                println!("   ✅ Operating at thermal limit (safe)");
            }
        }
        Err(e) => println!("   ❌ Error: {}", e),
    }
}
