import yaml
import numpy as np

# --- LEVEL 1: MATERIALS LOADER ---
class MaterialsDatabase:
    def __init__(self, yaml_path: str):
        print(f"📚 Loading Materials Database from {yaml_path}...")
        with open(yaml_path, 'r') as f:
            self.data = yaml.safe_load(f)
            
    def get_material_property(self, category: str, material: str, prop: str):
        try:
            return self.data[category][material][prop]
        except KeyError:
            raise Exception(f"❌ Could not find {prop} for {material} in {category}")

# --- LEVEL 2: PHYSICS ENGINE (FIVE CORE LAWS) ---
class PhysicsEngine:
    def __init__(self, materials_db: MaterialsDatabase):
        self.db = materials_db

    def analyze_trace(self, trace_name: str, length_mm: float, width_mm: float, thickness_mm: float, current_amps: float):
        print(f"\n⚡ Physics Analysis: Route '{trace_name}'")
        print(f"   Geometry: {length_mm}mm(L) x {width_mm}mm(W) x {thickness_mm}mm(T)")
        
        # 1. Fetch Material Properties for Copper
        rho = float(self.db.get_material_property('conductors', 'copper', 'resistivity_ohm_m'))
        max_density = float(self.db.get_material_property('conductors', 'copper', 'max_current_density_a_mm2'))
        
        # 2. Apply LAW 1: Resistance ( R = ρ * (L/A) )
        # Convert dimensions to meters for standard physics equations
        length_m = length_mm * 1e-3
        width_m = width_mm * 1e-3
        thickness_m = thickness_mm * 1e-3
        area_m2 = width_m * thickness_m
        
        resistance_ohms = rho * (length_m / area_m2)
        print(f"   Calculated Resistance : {resistance_ohms:.6f} Ω")
        
        # 3. Apply LAW 4: Ohm's Law ( V = I * R )
        voltage_drop = current_amps * resistance_ohms
        print(f"   Voltage Drop          : {voltage_drop:.6f} V (at {current_amps}A)")
        
        # 4. Apply LAW 5: Thermal & Safety Limits
        power_dissipation_watts = (current_amps ** 2) * resistance_ohms
        print(f"   Power Dissipation     : {power_dissipation_watts:.6f} W")
        
        # Calculate Current Density (Amps per mm^2)
        area_mm2 = width_mm * thickness_mm
        current_density = current_amps / area_mm2
        print(f"   Current Density       : {current_density:.2f} A/mm² (Limit: {max_density} A/mm²)")
        
        # Safety Validation
        if current_density > max_density:
            raise Exception(f"❌ FATAL THERMAL ERROR: Trace '{trace_name}' will melt! \n"
                            f"   Current density of {current_density:.2f} A/mm² exceeds Copper's safe limit of {max_density} A/mm².\n"
                            f"   Suggestion: Increase trace width or reduce current.")
        else:
            print(f"   ✅ Thermal Check Passed. Trace is operating safely.")

# --- SIMULATE PHASE 4 TESTING ---
if __name__ == "__main__":
    
    # 1. Initialize Database
    db = MaterialsDatabase('standard-materials.yaml')
    engine = PhysicsEngine(db)
    
    # Trace Specifications
    # Let's assume a 1mm wide, 0.035mm thick (1oz copper), 50mm long trace
    t_length = 50.0  
    t_width = 1.0    
    t_thickness = 0.035 
    
    # Test Scenario 1: A normal, safe current (2 Amps, like powering a small motor)
    try:
        engine.analyze_trace(
            trace_name="Safe_Motor_Power",
            length_mm=t_length,
            width_mm=t_width,
            thickness_mm=t_thickness,
            current_amps=1.0  # 1 Ampere
        )
    except Exception as e:
        print(e)
        
    # Test Scenario 2: Trying to push 50 Amps through a tiny PCB trace!
    try:
        engine.analyze_trace(
            trace_name="Dangerous_Main_Power",
            length_mm=t_length,
            width_mm=t_width,
            thickness_mm=t_thickness,
            current_amps=50.0 # 50 Amperes!
        )
    except Exception as e:
        print(e)