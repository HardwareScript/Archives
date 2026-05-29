import numpy as np

# --- LEVEL 1: MATERIAL DEFINITIONS ---
class MaterialState:
    EMPTY = 0
    FR4 = 1       # Fiberglass Substrate
    COPPER = 2    # Conductive Routing/Planes
    SILICON = 3   # Semiconductor Base

class HardwareSpace:
    def __init__(self, name: str, dimensions_mm: tuple, grid_cells: tuple):
        """
        Initializes the physical space and mathematically calculates the 3D tensor grid.
        dimensions_mm = (X_width, Y_height, Z_depth)
        grid_cells = (X_cols, Y_rows, Z_layers)
        """
        self.name = name
        self.dim_mm = dimensions_mm
        self.grid_cells = grid_cells
        
        # Calculate the mathematical truth: Voxel Resolution
        self.voxel_size_mm = (
            self.dim_mm[0] / self.grid_cells[0],  # X resolution
            self.dim_mm[1] / self.grid_cells[1],  # Y resolution
            self.dim_mm[2] / self.grid_cells[2]   # Z resolution
        )
        
        # Create the 3D Tensor Grid. 
        # Using[Z, X, Y] ordering to match Hardware Script syntax.
        # np.zeros fills the entire space with MaterialState.EMPTY (Air)
        self.tensor = np.zeros(
            (self.grid_cells[2], self.grid_cells[0], self.grid_cells[1]), 
            dtype=np.int8
        )
        
        print(f"✅ Space '{self.name}' initialized.")
        print(f"   Dimensions : {self.dim_mm[0]}x{self.dim_mm[1]}x{self.dim_mm[2]} mm")
        print(f"   Grid       : {self.grid_cells[0]}x{self.grid_cells[1]}x{self.grid_cells[2]} cells")
        print(f"   Voxel Size : {self.voxel_size_mm[0]:.3f}x{self.voxel_size_mm[1]:.3f}x{self.voxel_size_mm[2]:.3f} mm per cell\n")

    def add_spanning(self, material_code: int, span_type: str, layer: int = None):
        """
        Executes the explicit syntactic shortcuts for 'spanning all' or 'spanning layer Z'
        Note: Hardware Script uses 1-indexed coordinates (e.g., Layer 1).
        Python uses 0-indexed arrays, so we subtract 1 internally.
        """
        if span_type == "all":
            # Explicitly fill the entire 3D tensor with the material
            self.tensor[:, :, :] = material_code
            print(f"🔧 Action: Filled 'all' layers with Material {material_code}")
            
        elif span_type == "layer" and layer is not None:
            # Explicitly fill ONLY the specific Z-layer with the material
            z_index = layer - 1  # Convert to Python 0-index
            self.tensor[z_index, :, :] = material_code
            print(f"🔧 Action: Filled 'layer {layer}' with Material {material_code}")
            
        else:
            raise ValueError("❌ Fatal Error: Invalid spanning parameters.")

    def inspect_layer(self, layer: int):
        """Helper function to visualize a cross-section of the 3D Grid"""
        z_index = layer - 1
        unique_materials = np.unique(self.tensor[z_index])
        print(f"\n🔍 Inspection of Layer {layer}:")
        print(f"   Materials present in this layer: {unique_materials}")
        
        # Check if the layer is solid copper
        if len(unique_materials) == 1 and unique_materials[0] == MaterialState.COPPER:
            print("   Status: Solid Copper Plane (Warning: Vias require explicit clearance!)")


# --- SIMULATING THE PARSED .hw FILE ---
if __name__ == "__main__":
    """
    Simulating the parsing of this Hardware Script:
    
    define Space "SprinklerController":
        dimensions: 50mm by 50mm by 2mm
        grid: 50 by 50 by 4  # 4-layer PCB
        
        # Base fiberglass board
        add Substrate(FR4) spanning all
        
        # Inner sandwich Ground and Power planes
        add Copper named GroundPlane spanning layer 2
        add Copper named PowerPlane spanning layer 3
    """
    
    # 1. Instantiate the Space
    board = HardwareSpace(
        name="SprinklerController",
        dimensions_mm=(50.0, 50.0, 2.0),
        grid_cells=(50, 50, 4)
    )
    
    # 2. Add the base fiberglass (spanning all)
    board.add_spanning(MaterialState.FR4, span_type="all")
    
    # 3. Add the explicit internal Copper Planes
    board.add_spanning(MaterialState.COPPER, span_type="layer", layer=2)
    board.add_spanning(MaterialState.COPPER, span_type="layer", layer=3)
    
    # 4. Verify the physical reality in memory
    board.inspect_layer(layer=1) # Should be just FR4
    board.inspect_layer(layer=2) # Should be solid Copper