#!/usr/bin/env python3
"""
Materials Project API Data Fetcher
Purpose: Fetch physical properties for Hardware Script materials database
"""

from mp_api.client import MPRester
import json
import yaml
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MATERIALS_PROJECT_API_KEY")

# Materials we need to fetch
MATERIALS = {
    # Conductors
    "Cu": {"name": "Copper", "group": "conductor"},
    "Au": {"name": "Gold", "group": "conductor"},
    "Al": {"name": "Aluminum", "group": "conductor"},
    
    # Insulators
    "SiO2": {"name": "Silicon Dioxide", "group": "insulator"},
    
    # Semiconductors
    "Si": {"name": "Silicon", "group": "semiconductor"},
}

def fetch_material_properties(formula, material_name):
    """
    Fetch material properties from Materials Project API
    """
    print(f"\n{'='*60}")
    print(f"Fetching data for: {material_name} ({formula})")
    print(f"{'='*60}")
    
    with MPRester(API_KEY) as mpr:
        # Search for materials by formula
        docs = mpr.materials.summary.search(
            formula=formula,
            fields=[
                "material_id",
                "formula_pretty",
                "structure",
                "symmetry",
                "density",
                "volume",
                "energy_per_atom",
                "formation_energy_per_atom",
                "band_gap",
                "is_metal",
                "is_stable",
                "theoretical",
            ]
        )
        
        if not docs:
            print(f"❌ No results found for {formula}")
            return None
        
        # Get the most stable material
        stable_doc = None
        for doc in docs:
            if doc.is_stable:
                stable_doc = doc
                break
        
        if not stable_doc and docs:
            stable_doc = docs[0]
        
        print(f"✓ Found material: {stable_doc.material_id}")
        print(f"  Formula: {stable_doc.formula_pretty}")
        print(f"  Density: {stable_doc.density:.2f} g/cm³")
        print(f"  Band Gap: {stable_doc.band_gap:.3f} eV")
        print(f"  Is Metal: {stable_doc.is_metal}")
        print(f"  Is Stable: {stable_doc.is_stable}")
        
        # Try to fetch additional properties
        material_id = stable_doc.material_id
        
        # Fetch dielectric properties
        try:
            dielectric_docs = mpr.materials.dielectric.search(material_ids=[material_id])
            if dielectric_docs:
                dielectric = dielectric_docs[0]
                print(f"  Dielectric constant (ε_r): {dielectric.e_total:.2f}")
        except Exception as e:
            print(f"  ⚠ Dielectric data not available")
        
        # Fetch elasticity properties
        try:
            elastic_docs = mpr.materials.elasticity.search(material_ids=[material_id])
            if elastic_docs:
                elastic = elastic_docs[0]
                print(f"  Bulk modulus: {elastic.k_vrh:.2f} GPa")
                print(f"  Shear modulus: {elastic.g_vrh:.2f} GPa")
        except Exception as e:
            print(f"  ⚠ Elasticity data not available")
        
        # Fetch electronic structure
        try:
            elec_docs = mpr.materials.electronic_structure.search(material_ids=[material_id])
            if elec_docs:
                elec = elec_docs[0]
                print(f"  Electronic structure available")
        except Exception as e:
            print(f"  ⚠ Electronic structure not available")
        
        return {
            "material_id": stable_doc.material_id,
            "formula": stable_doc.formula_pretty,
            "density": stable_doc.density,
            "band_gap": stable_doc.band_gap,
            "is_metal": stable_doc.is_metal,
            "is_stable": stable_doc.is_stable,
            "energy_per_atom": stable_doc.energy_per_atom,
            "formation_energy_per_atom": stable_doc.formation_energy_per_atom,
        }

def main():
    """
    Main function to fetch all materials
    """
    print("="*60)
    print("Materials Project API - Hardware Script Data Fetcher")
    print("="*60)
    
    results = {}
    
    for formula, info in MATERIALS.items():
        try:
            data = fetch_material_properties(formula, info["name"])
            if data:
                results[formula] = {
                    "name": info["name"],
                    "group": info["group"],
                    "mp_data": data
                }
        except Exception as e:
            print(f"❌ Error fetching {formula}: {str(e)}")
    
    # Save results to JSON
    output_file = "Research/materials_project_data.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✓ Data saved to: {output_file}")
    print(f"{'='*60}")
    
    # Print summary
    print("\nSummary:")
    print(f"  Total materials fetched: {len(results)}")
    for formula, data in results.items():
        print(f"  - {data['name']} ({formula}): {data['mp_data']['material_id']}")

if __name__ == "__main__":
    main()
