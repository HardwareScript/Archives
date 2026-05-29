import numpy as np

# --- LEVEL 1: MATERIAL & STATE DEFINITIONS ---
class CellState:
    EMPTY = 0
    FR4 = 1       
    COPPER = 2    
    SILICON = 3   
    PAD = 4          
    BODY = 5         
    HOLE = 6         # Drilled Via connecting layers

class HardwareSpace:
    def __init__(self, name: str, dimensions_mm: tuple, grid_cells: tuple):
        self.name = name
        self.grid_cells = grid_cells
        self.tensor = np.ones(
            (self.grid_cells[2], self.grid_cells[0], self.grid_cells[1]), 
            dtype=np.int8
        ) * CellState.FR4

    def _bresenham_line(self, x0, y0, x1, y1):
        """Mathematical interpolation of a straight line on a discrete 2D grid."""
        points =[]
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points.append((x, y))
        return points

    def route_copper(self, route_name: str, waypoints: list, clearance: int = 0):
        """
        Executes explicit waypoint routing.
        waypoints format: [(Z, X, Y), (Z, X, Y), ...] (1-indexed)
        """
        print(f"\n🛤️  Routing: '{route_name}'")
        
        for i in range(len(waypoints) - 1):
            p1 = waypoints[i]
            p2 = waypoints[i+1]
            
            # Convert to 0-indexed for Python arrays
            z1, x1, y1 = p1[0]-1, p1[1]-1, p1[2]-1
            z2, x2, y2 = p2[0]-1, p2[1]-1, p2[2]-1
            
            # SCENARIO A: Routing on the same layer (2D Copper Trace)
            if z1 == z2:
                print(f"   -> Drawing trace on Layer {p1[0]} from X:{p1[1]},Y:{p1[2]} to X:{p2[1]},Y:{p2[2]}")
                line_cells = self._bresenham_line(x1, y1, x2, y2)
                
                for (cx, cy) in line_cells:
                    current_state = self.tensor[z1, cx, cy]
                    
                    # Collision Engine: Copper cannot run through a Component Body!
                    if current_state == CellState.BODY:
                        raise Exception(f"❌ Fatal Routing Error: Trace '{route_name}' hit a component body at [Z:{p1[0]}, X:{cx+1}, Y:{cy+1}]!")
                    
                    self.tensor[z1, cx, cy] = CellState.COPPER

            # SCENARIO B: Layer Change (Vertical Via)
            else:
                if x1 == x2 and y1 == y2:
                    print(f"   -> Drilling VIA at X:{p1[1]},Y:{p1[2]} from Layer {p1[0]} to {p2[0]}")
                    
                    # Determine drill direction (up or down)
                    step = 1 if z2 > z1 else -1
                    for z_drill in range(z1, z2 + step, step):
                        # Apply explicit clearance logic if passing through an inner layer
                        if clearance > 0:
                            # User explicitly requested an Anti-Pad (clearance)
                            # (For MVP: We clear a 3x3 square around the via)
                            self.tensor[z_drill, x1-1:x1+2, y1-1:y1+2] = CellState.FR4
                            
                        self.tensor[z_drill, x1, y1] = CellState.HOLE
                else:
                    raise Exception(f"❌ Fatal Routing Error: Invalid Via from {p1} to {p2}. X and Y must be identical when changing Z-layers!")

        print(f"   ✅ Route '{route_name}' successfully laid.")

# --- SIMULATING THE PARSED .hw FILE ---
if __name__ == "__main__":
    
    # 1. Initialize Space
    board = HardwareSpace("SprinklerController", (50,50,2), (50,50,4))
    
    # Let's pretend a component BODY exists at [1, 15, 11] to[1, 17, 13]
    # We manually place a component body to test the trace collision engine
    board.tensor[0, 14:17, 10:13] = CellState.BODY

    # 2. Execute Hardware Script Routing
    print("Testing Valid Route...")
    board.route_copper(
        route_name="Power_To_Valve",
        waypoints=[
            (1, 10, 11),  # Start
            (1, 12, 11),  # Move right
            (1, 12, 15),  # Move down (avoiding the component body at Y=11..13)
            (1, 20, 15),  # Move right past the component
            (2, 20, 15)   # Drill via to layer 2
        ],
        clearance=1
    )

    # 3. Test Invalid Via (Diagonal Drill)
    print("\n⚠️ Testing Invalid Via Rule...")
    try:
        board.route_copper(
            route_name="Bad_Via_Test",
            waypoints=[(1, 5, 5), (2, 6, 6)] # Cannot change X/Y while changing Z
        )
    except Exception as e:
        print(e)
        
    # 4. Test Trace Collision (Hitting the Body)
    print("\n⚠️ Testing Trace Collision Rule...")
    try:
        board.route_copper(
            route_name="Collision_Test",
            waypoints=[(1, 10, 12), (1, 20, 12)] # Drives straight through the component body we placed!
        )
    except Exception as e:
        print(e)