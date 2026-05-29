#!/usr/bin/env python3
"""
Enhanced Materials Database Generator
Combines Materials Project API data with Hardware Script requirements
"""

import json
import yaml
from datetime import datetime

# Materials Project data (from your API call)
MP_DATA = {
    "Cu": {
        "material_id": "mp-1056079",
        "density_g_cm3": 0.187398436304439,  # This seems wrong - should be ~8.96
        "band_gap_eV": 0,
        "is_metal": True
    },
    "Au": {
        "material_id": "mp-1238808", 
        "density_g_cm3": 16.730993180447804,  # This looks correct
        "band_gap_eV": 0.0,
        "is_metal": True
    },
    "Al": {
        "material_id": "mp-1244953",
        "density_g_cm3": 2.532974864040623,  # This looks correct
        "band_gap_eV": 0.0,
        "is_metal": True
    },
    "SiO2": {
        "material_id": "mp-1244945",
        "density_g_cm3": 2.082094202127012,  # This looks correct
        "band_gap_eV": 5.016999999999999,
        "is_metal": False
    },
    "Si": {
        "material_id": "mp-1244933",
        "density_g_cm3": 2.599954373928591,  # This looks correct
        "band_gap_eV": 0.0,  # This seems wrong - should be ~1.12 eV
        "is_metal": False
    }
}

# Engineering constants (from literature/datasheets)
ENGINEERING_DATA = {
    "Cu": {
        "resistivity_ohm_m": 1.68e-8,
        "thermal_conductivity_w_mk": 401,
        "melting_point_c": 1085,
        "max_current_density_a_mm2": 35,
        "density_corrected_g_cm3": 8.96  # Correct copper density
    },
    "Au": {
        "resistivity_ohm_m": 2.44e-8,
        "thermal_conductivity_w_mk": 318,
        "melting_point_c": 1064,
        "max_current_density_a_mm2": 30
    },
    "Al": {
        "resistivity_ohm_m": 2.82e-8,
        "thermal_conductivity_w_mk": 237,
        "melting_point_c": 660,
        "max_current_density_a_mm2": 20
    },
    "SiO2": {
        "dielectric_strength_kv_mm": 10,
        "relative_permittivity": 3.9,
        "thermal_conductivity_w_mk": 1.4
    },
    "Si": {
        "bandgap_corrected_eV": 1.12,  # Correct silicon bandgap
        "electron_mobility_cm2_vs": 1400,
        "hole_mobility_cm2_vs": 450,
        "thermal_conductivity_w_mk": 150
    }
}

def generate_enhanced_database():
    """Generate enhanced materials database"""
    
    database = {
        "metadata": {
            "version": "0.2",
            "status": "Enhanced with Materials Project data",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "sources": [
                "Materials Project API",
                "Engineering handbooks",
                "Manufacturer datasheets"
            ]
        },
        "conductors": {},
        "insulators": {},
        "semiconductors": {}
    }
    
    # Copper
    database["conductors"]["copper"] = {
        "name": "Copper",
        "symbol": "Cu",
        "materials_project_id": MP_DATA["Cu"]["material_id"],
        "description": "Universal PCB trace material",
        
        # Physical properties
        "density_g_cm3": ENGINEERING_DATA["Cu"]["density_corrected_g_cm3"],
        "density_kg_m3": ENGINEERING_DATA["Cu"]["density_corrected_g_cm3"] * 1000,
        
        # Electrical properties
        "resistivity_ohm_m": ENGINEERING_DATA["Cu"]["resistivity_ohm_m"],
        "is_metal": MP_DATA["Cu"]["is_metal"],
        "band_gap_eV": MP_DATA["Cu"]["band_gap_eV"],
        
        # Thermal properties
        "thermal_conductivity_w_mk": ENGINEERING_DATA["Cu"]["thermal_conductivity_w_mk"],
        "melting_point_c": ENGINEERING_DATA["Cu"]["melting_point_c"],
        
        # Current handling
        "max_current_density_a_mm2": ENGINEERING_DATA["Cu"]["max_current_density_a_mm2"],
        
        # Visual
        "color_hex": "#B87333"
    }
    
    # Gold
    database["conductors"]["gold"] = {
        "name": "Gold",
        "symbol": "Au", 
        "materials_project_id": MP_DATA["Au"]["material_id"],
        "description": "Contact pads, wire bonding, corrosion-resistant",
        
        "density_g_cm3": MP_DATA["Au"]["density_g_cm3"],
        "density_kg_m3": MP_DATA["Au"]["density_g_cm3"] * 1000,
        
        "resistivity_ohm_m": ENGINEERING_DATA["Au"]["resistivity_ohm_m"],
        "is_metal": MP_DATA["Au"]["is_metal"],
        "band_gap_eV": MP_DATA["Au"]["band_gap_eV"],
        
        "thermal_conductivity_w_mk": ENGINEERING_DATA["Au"]["thermal_conductivity_w_mk"],
        "melting_point_c": ENGINEERING_DATA["Au"]["melting_point_c"],
        
        "max_current_density_a_mm2": ENGINEERING_DATA["Au"]["max_current_density_a_mm2"],
        
        "color_hex": "#FFD700"
    }
    
    # Aluminum
    database["conductors"]["aluminum"] = {
        "name": "Aluminum",
        "symbol": "Al",
        "materials_project_id": MP_DATA["Al"]["material_id"],
        "description": "Chip-level routing, heat sinks",
        
        "density_g_cm3": MP_DATA["Al"]["density_g_cm3"],
        "density_kg_m3": MP_DATA["Al"]["density_g_cm3"] * 1000,
        
        "resistivity_ohm_m": ENGINEERING_DATA["Al"]["resistivity_ohm_m"],
        "is_metal": MP_DATA["Al"]["is_metal"],
        "band_gap_eV": MP_DATA["Al"]["band_gap_eV"],
        
        "thermal_conductivity_w_mk": ENGINEERING_DATA["Al"]["thermal_conductivity_w_mk"],
        "melting_point_c": ENGINEERING_DATA["Al"]["melting_point_c"],
        
        "max_current_density_a_mm2": ENGINEERING_DATA["Al"]["max_current_density_a_mm2"],
        
        "color_hex": "#C0C0C0"
    }
    
    # Silicon Dioxide (Insulator)
    database["insulators"]["silicon_dioxide"] = {
        "name": "Silicon Dioxide",
        "symbol": "SiO2",
        "materials_project_id": MP_DATA["SiO2"]["material_id"],
        "description": "Microchip insulator, glass substrate",
        
        "density_g_cm3": MP_DATA["SiO2"]["density_g_cm3"],
        "density_kg_m3": MP_DATA["SiO2"]["density_g_cm3"] * 1000,
        
        "band_gap_eV": MP_DATA["SiO2"]["band_gap_eV"],
        "is_metal": MP_DATA["SiO2"]["is_metal"],
        
        "dielectric_strength_kv_mm": ENGINEERING_DATA["SiO2"]["dielectric_strength_kv_mm"],
        "relative_permittivity": ENGINEERING_DATA["SiO2"]["relative_permittivity"],
        "thermal_conductivity_w_mk": ENGINEERING_DATA["SiO2"]["thermal_conductivity_w_mk"],
        
        "color_hex": "#F0F0F0"
    }
    
    # FR4 Fiberglass (PCB Substrate)
    database["insulators"]["fr4"] = {
        "name": "FR4 Fiberglass",
        "symbol": "FR4",
        "materials_project_id": None,  # Not in Materials Project (composite material)
        "description": "Standard PCB substrate material (flame retardant fiberglass epoxy)",
        
        "density_g_cm3": 1.85,
        "density_kg_m3": 1850,
        
        "dielectric_strength_kv_mm": 20,
        "relative_permittivity": 4.5,
        "dissipation_factor": 0.02,
        "thermal_conductivity_w_mk": 0.3,
        "glass_transition_temp_c": 130,
        "max_operating_temp_c": 130,
        
        "color_hex": "#2E7D32"
    }
    
    # Air (Ambient Environment)
    database["insulators"]["air"] = {
        "name": "Air",
        "symbol": "Air",
        "materials_project_id": None,  # Not applicable (gas mixture)
        "description": "Ambient environment, spark gap calculations",
        
        "density_g_cm3": 0.001225,  # 1.225 kg/m³ at sea level
        "density_kg_m3": 1.225,
        
        "dielectric_strength_kv_mm": 3.0,
        "dielectric_strength_note": "At sea level, 50% humidity. Decreases at altitude.",
        "relative_permittivity": 1.00059,
        "thermal_conductivity_w_mk": 0.026,
        
        "color_hex": "#00000000"  # Transparent
    }
    
    # Silicon (Semiconductor)
    database["semiconductors"]["silicon"] = {
        "name": "Silicon (Doped)",
        "symbol": "Si",
        "materials_project_id": MP_DATA["Si"]["material_id"],
        "description": "Transistors, diodes, semiconductor devices",
        
        "density_g_cm3": MP_DATA["Si"]["density_g_cm3"],
        "density_kg_m3": MP_DATA["Si"]["density_g_cm3"] * 1000,
        
        # Use corrected bandgap
        "band_gap_eV": ENGINEERING_DATA["Si"]["bandgap_corrected_eV"],
        "band_gap_note": "Intrinsic silicon at 300K (MP data shows 0.0, corrected to 1.12)",
        "is_metal": MP_DATA["Si"]["is_metal"],
        
        "electron_mobility_cm2_vs": ENGINEERING_DATA["Si"]["electron_mobility_cm2_vs"],
        "hole_mobility_cm2_vs": ENGINEERING_DATA["Si"]["hole_mobility_cm2_vs"],
        "thermal_conductivity_w_mk": ENGINEERING_DATA["Si"]["thermal_conductivity_w_mk"],
        
        "color_hex": "#808080"
    }
    
    # Add resistive materials section
    database["resistive_materials"] = {}
    
    # Carbon Film (Resistors)
    database["resistive_materials"]["carbon_film"] = {
        "name": "Carbon Film",
        "symbol": "C",
        "materials_project_id": None,  # Not in MP (engineered composite)
        "description": "Standard resistor material, stable and inexpensive",
        
        "density_g_cm3": 2.0,
        "density_kg_m3": 2000,
        
        "resistivity_ohm_m": 3.5e-5,
        "resistivity_note": "Typical value for thin film resistors",
        "temp_coefficient_ppm_c": 200,
        "temp_coefficient_note": "Resistance changes ~200 ppm per °C",
        
        "thermal_conductivity_w_mk": 1.7,
        "max_operating_temp_c": 155,
        "max_power_density_w_cm2": 50,
        
        "color_hex": "#000000"
    }
    
    return database

def save_database():
    """Save enhanced database to YAML and JSON"""
    
    db = generate_enhanced_database()
    
    # Save as YAML (human readable)
    with open("enhanced_materials.yaml", "w") as f:
        yaml.dump(db, f, default_flow_style=False, indent=2)
    
    # Save as JSON (machine readable)
    with open("enhanced_materials.json", "w") as f:
        json.dump(db, f, indent=2)
    
    print("✓ Enhanced materials database created:")
    print("  - enhanced_materials.yaml (human readable)")
    print("  - enhanced_materials.json (machine readable)")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Conductors: {len(db['conductors'])}")
    print(f"  Insulators: {len(db['insulators'])}")
    print(f"  Semiconductors: {len(db['semiconductors'])}")
    print(f"  Resistive Materials: {len(db['resistive_materials'])}")
    print(f"  Total Materials: {len(db['conductors']) + len(db['insulators']) + len(db['semiconductors']) + len(db['resistive_materials'])}")
    
    return db

if __name__ == "__main__":
    save_database()