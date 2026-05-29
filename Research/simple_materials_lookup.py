#!/usr/bin/env python3
"""
Simple Materials Lookup - Direct API calls without heavy dependencies
Uses requests library to make direct HTTP calls to Materials Project API
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MATERIALS_PROJECT_API_KEY")
BASE_URL = "https://api.materialsproject.org"

def search_material(formula):
    """Search for material by formula using direct API call"""
    
    headers = {"X-API-KEY": API_KEY}
    
    # Search endpoint
    url = f"{BASE_URL}/materials/summary/"
    params = {
        "formula": formula,
        "_fields": "material_id,formula_pretty,density,band_gap,is_metal,is_stable"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get("data"):
            return data["data"][0]  # Return first result
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def main():
    """Fetch basic data for our materials"""
    
    materials = ["Cu", "Au", "Al", "SiO2", "Si"]
    results = {}
    
    print("Fetching materials data via direct API calls...")
    print("="*50)
    
    for formula in materials:
        print(f"Searching: {formula}")
        data = search_material(formula)
        
        if data:
            results[formula] = data
            print(f"  ✓ Found: {data['material_id']}")
            print(f"    Density: {data.get('density', 'N/A')} g/cm³")
            print(f"    Band gap: {data.get('band_gap', 'N/A')} eV")
        else:
            print(f"  ❌ Not found")
        print()
    
    # Save results
    with open("simple_materials_data.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Saved to: simple_materials_data.json")

if __name__ == "__main__":
    main()