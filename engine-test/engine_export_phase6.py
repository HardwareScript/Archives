import os
import numpy as np

# --- 1. MOCKING THE 3D TENSOR GRID ---
# Let's pretend Engine A just finished routing a 10mm x 10mm board
# with a 1mm voxel resolution.
voxel_size_mm = 1.0
board_tensor = np.zeros((1, 10, 10), dtype=np.int8)

# We draw a copper trace from X:2, Y:2 to X:8, Y:2
for x in range(2, 9):
    board_tensor[0, x, 2] = 2  # 2 represents COPPER in our CellState

# Create build directory
os.makedirs("build", exist_ok=True)

# --- 2. ENGINE B: BLENDER 3D EXPORT ---
def export_to_blender(tensor, voxel_size):
    print("🎬 EXPORTING TO BLENDER 3D...")
    filepath = "build/sim.py"
    
    with open(filepath, "w") as f:
        f.write("import bpy\n\n")
        f.write("# Clear existing objects\n")
        f.write("bpy.ops.wm.read_factory_settings(use_empty=True)\n\n")
        
        # 1. Generate the FR4 Substrate (The Board)
        f.write("# Generate FR4 Substrate\n")
        width = tensor.shape[1] * voxel_size
        height = tensor.shape[2] * voxel_size
        f.write(f"bpy.ops.mesh.primitive_cube_add(size=1, location=({width/2}, {height/2}, -0.5), scale=({width}, {height}, 1))\n")
        f.write("board = bpy.context.scene.objects[-1]\n")
        f.write("board.name = 'FR4_Substrate'\n\n")
        
        # 2. Generate the Copper Traces
        f.write("# Generate Copper Voxels\n")
        for x in range(tensor.shape[1]):
            for y in range(tensor.shape[2]):
                if tensor[0, x, y] == 2: # If Copper
                    # Map tensor grid coordinates to real-world millimeters
                    real_x = x * voxel_size
                    real_y = y * voxel_size
                    f.write(f"bpy.ops.mesh.primitive_cube_add(size={voxel_size}, location=({real_x}, {real_y}, 0.5))\n")
                    f.write("bpy.context.scene.objects[-1].name = 'Copper_Trace'\n")
                    
    print(f"   ✅ Generated Blender Script: {filepath}")

# --- 3. ENGINE C: GERBER MANUFACTURING EXPORT ---
def export_to_gerber(tensor, voxel_size):
    print("\n🏭 EXPORTING TO GERBER (PCB FACTORY FORMAT)...")
    filepath = "build/top_copper.gtl"
    
    with open(filepath, "w") as f:
        # Standard Gerber X2 Header
        f.write("%FSLAX26Y26*%\n")  # Format specification (2.6)
        f.write("%MOMM*%\n")        # Units: Millimeters
        f.write(f"%ADD10C,{voxel_size:.4f}*%\n")  # Define circular aperture size (trace width)
        f.write("D10*\n")           # Select aperture 10
        
        # Scan the tensor for contiguous copper traces
        # (Simplified for MVP: just plots every copper voxel)
        for x in range(tensor.shape[1]):
            for y in range(tensor.shape[2]):
                if tensor[0, x, y] == 2:
                    # Gerber coordinates require shifting decimals (e.g., 2.5mm -> 025000)
                    gerber_x = int((x * voxel_size) * 10000)
                    gerber_y = int((y * voxel_size) * 10000)
                    
                    # D02 = Move to location without drawing
                    # D01 = Draw/Flash at location
                    f.write(f"X{gerber_x:06d}Y{gerber_y:06d}D01*\n")
                    
        f.write("M02*\n") # End of File
    print(f"   ✅ Generated Gerber File: {filepath}")

# --- EXECUTE EXPORTS ---
if __name__ == "__main__":
    print("==================================================")
    print("🏭 HARDWARE SCRIPT EXPORT ENGINES (PHASE 6)")
    print("==================================================\n")
    
    export_to_blender(board_tensor, voxel_size_mm)
    export_to_gerber(board_tensor, voxel_size_mm)
    
    print("\n✅ EXPORT COMPLETE! Check the 'build' folder.")