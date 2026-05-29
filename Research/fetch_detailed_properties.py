#!/usr/bin/env python3
"""
Detailed Materials Properties Fetcher
Fetches comprehensive data including thermal, electrical, and mechanical properties
"""

from mp_api.client import MPRester
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MATERIALS_PROJECT_API_KEY")

MATERIALS = {
    "Cu": "Copper",
    "Au": "Gold", 
    "Al": "Aluminum",
    "SiO2": "Silicon Dioxide",
    "Si": "Silicon",
}

def fetch_comprehensive_data(formula, name):
    """Fetch all available properties for a material"""
    print(f"\n{'='*70}")
    print(f"Material: {name} ({formula})")
    print(f"{'='*70}")
    
    with MPRester(API_KEY) as mpr:
        # 1. Summary data
        summary = mpr.materials.summary.search(
            formula=formula,
            fields=["material_id", "formula_pretty", "density", "band_gap", 
                    "is_metal", "is_stable", "energy_per_atom"]
        )
        
        if not summary:
            print(f"❌ No data found")
            return None
        
        mat = summary[0]
        mat_id = mat.material_id
        
        result = {
            "material_id": mat_id,
            "formula": mat.formula_pretty,
            "density_g_cm3": mat.density,
            "band_gap_eV": mat.band_gap,
            "is_metal": mat.is_metal,
        }
        
        print(f"✓ Material ID: {mat_id}")
        print(f"  Density: {mat.density:.3f} g/cm³")
        print(f"  Band gap: {mat.band_gap:.3f} eV")
        
        # 2. Dielectric properties
        try:
            diel = mpr.materials.dielectric.search(material_ids=[mat_id])
            if diel:
                result["dielectric_constant"] = diel[0].e_total
                print(f"  Dielectric constant: {diel[0].e_total:.2f}")
        except:
            print(f"  ⚠ No dielectric data")
        
        # 3. Elasticity
        try:
            elast = mpr.materials.elasticity.search(material_ids=[mat_id])
            if elast:
                result["bulk_modulus_GPa"] = elast[0].k_vrh
                result["shear_modulus_GPa"] = elast[0].g_vrh
                print(f"  Bulk modulus: {elast[0].k_vrh:.1f} GPa")
        except:
            print(f"  ⚠ No elasticity data")
        
        # 4. Electronic structure
        try:
            elec = mpr.materials.electronic_structure.search(material_ids=[mat_id])
            if elec:
                result["has_electronic_structure"] = True
                print(f"  ✓ Electronic structure available")
        except:
            print(f"  ⚠ No electronic structure")
        
        return result

def main():
    results = {}
    
    for formula, name in MATERIALS.items():
        try:
            data = fetch_comprehensive_data(formula, name)
            if data:
                results[formula] = {"name": name, "properties": data}
        except Exception as e:
            print(f"❌ Error: {e}")
    
    with open("Research/mp_detailed_data.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✓ Saved to: Research/mp_detailed_data.json")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
