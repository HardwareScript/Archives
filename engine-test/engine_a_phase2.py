import numpy as np

# --- LEVEL 1: MATERIAL & STATE DEFINITIONS ---
class CellState:
    EMPTY = 0
    FR4 = 1       
    COPPER = 2    
    SILICON = 3   
    PAD = 4          # Component connection point (routeable)
    BODY = 5         # Component keep-out zone (blocks routing)

# --- LEVEL 4: STANDARD LIBRARY COMPONENT DEFINITION ---
class ComponentDef:
    def __init__(self, name: str, grid_w: int, grid_h: int):
        self.name = name
        self.width = grid_w
        self.height = grid_h
        self.pins = {}  # Format: {"PinName": (local_x, local_y)}
        
    def add_pin(self, name: str, lx: int, ly: int):
        self.pins[name] = (lx, ly)

# --- ENGINE A: THE 3D SPATIAL TENSOR ---
class HardwareSpace:
    def __init__(self, name: str, dimensions_mm: tuple, grid_cells: tuple):
        self.name = name
        self.dim_mm = dimensions_mm
        self.grid_cells = grid_cells
        self.tensor = np.ones(
            (self.grid_cells[2], self.grid_cells[0], self.grid_cells[1]), 
            dtype=np.int8
        ) * CellState.FR4  # Assume starting with solid FR4 for simplicity

    def rotate_local_coords(self, lx, ly, width, height, direction):
        """
        Mathematically maps local component coordinates to the requested orientation.
        Assuming [0,0] is Top-Left. 
        North = Default, East = 90 deg clockwise, South = 180, West = 270.
        """
        if direction == "North":
            return lx, ly
        elif direction == "East":
            return height - 1 - ly, lx
        elif direction == "South":
            return width - 1 - lx, height - 1 - ly
        elif direction == "West":
            return ly, width - 1 - lx
        else:
            raise ValueError(f"❌ Invalid rotation direction: {direction}")

    def place_component(self, comp: ComponentDef, instance_name: str, pos: tuple, rotation: str = "North"):
        """
        Executes: add <Component> named <Name> at [Z, X, Y] rotated <Direction>
        pos = (Z_layer, X_col, Y_row) - 1-indexed from hardware script
        """
        z_idx = pos[0] - 1
        x_origin = pos[1] - 1
        y_origin = pos[2] - 1
        
        # Calculate the new bounding box based on rotation
        if rotation in ["North", "South"]:
            new_w, new_h = comp.width, comp.height
        else: # East or West flips width and height
            new_w, new_h = comp.height, comp.width

        # 1. COLLISION DETECTION (O(1) Time Complexity)
        # Check if the target area is completely clear of other components
        target_area = self.tensor[z_idx, x_origin : x_origin+new_w, y_origin : y_origin+new_h]
        if np.any((target_area == CellState.BODY) | (target_area == CellState.PAD)):
            raise Exception(f"❌ Fatal Error: Collision detected when placing '{instance_name}' at {pos}!")

        # 2. CLAIM THE BODY (Keep-out zone)
        self.tensor[z_idx, x_origin : x_origin+new_w, y_origin : y_origin+new_h] = CellState.BODY
        print(f"\n📦 Component Placed: '{instance_name}' ({comp.name})")
        print(f"   Orientation : {rotation}")
        print(f"   Global Bounding Box : X[{x_origin} to {x_origin+new_w-1}], Y[{y_origin} to {y_origin+new_h-1}]")

        # 3. MAP AND PLACE THE PINS
        print(f"   Pin Global Coordinates:")
        for pin_name, (lx, ly) in comp.pins.items():
            # Apply rotation math
            rot_x, rot_y = self.rotate_local_coords(lx, ly, comp.width, comp.height, rotation)
            
            # Translate to Global Coordinates
            global_x = x_origin + rot_x
            global_y = y_origin + rot_y
            
            # Mark the specific cell as a PAD (Routeable)
            self.tensor[z_idx, global_x, global_y] = CellState.PAD
            
            # Print output (+1 to match Hardware Script 1-index)
            print(f"      - {pin_name}: [Z:{pos[0]}, X:{global_x+1}, Y:{global_y+1}]")


# --- SIMULATING THE PARSED .hw FILE ---
if __name__ == "__main__":
    
    # 1. Initialize Space
    board = HardwareSpace("SprinklerController", (50,50,2), (50,50,2))
    
    # 2. Load Standard Library Component: Transistor_NPN (3x3 grid footprint)
    transistor_def = ComponentDef("Transistor_NPN", grid_w=3, grid_h=3)
    transistor_def.add_pin("Collector", lx=0, ly=1)
    transistor_def.add_pin("Base", lx=1, ly=0)
    transistor_def.add_pin("Emitter", lx=2, ly=1)
    
    # 3. Execute Hardware Script Commands:
    # add Transistor_NPN named Switch1 at [1, 10, 10] rotated North
    board.place_component(transistor_def, "Switch1", pos=(1, 10, 10), rotation="North")
    
    # add Transistor_NPN named Switch2 at[1, 20, 20] rotated East
    board.place_component(transistor_def, "Switch2", pos=(1, 20, 20), rotation="East")
    
    # add Transistor_NPN named Switch3 at [1, 30, 30] rotated South
    board.place_component(transistor_def, "Switch3", pos=(1, 30, 30), rotation="South")

    # Let's force a collision error to prove the physics engine works!
    print("\n⚠️  Testing Collision Engine...")
    try:
        # Trying to place a new component overlapping Switch1
        board.place_component(transistor_def, "CrashTransistor", pos=(1, 11, 10), rotation="North")
    except Exception as e:
        print(e)