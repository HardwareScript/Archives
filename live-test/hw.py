import sys
import os
import re
import yaml
import numpy as np

# =====================================================================
# PHASE 5: THE LEXER & PARSER
# =====================================================================
TOKEN_TYPES =[
    ('KEYWORD',   r'\b(define|Space|dimensions|grid|add|named|at|rotated|by|route|to|path)\b'),
    ('STRING',    r'"[^"]*"'),
    ('COORD',     r'\[\d+,\s*\d+,\s*\d+\]'),
    ('MEASURE',   r'\b\d+(?:\.\d+)?(?:mm|cm|V|A)\b'),
    ('NUMBER',    r'\b\d+\b'),
    ('IDENTIFIER',r'[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)?'),
    ('COLON',     r':'),
    ('LIST_ITEM', r'-\s*\[\d+,\s*\d+,\s*\d+\]'), # e.g. - [1, 5, 6]
    ('SKIP',      r'[ \t\n\r]+'),
    ('MISMATCH',  r'.'),
]

def parse_hw_file(filepath):
    print(f"📖 Reading {filepath}...")
    with open(filepath, 'r') as f:
        code = f.read()

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_TYPES)
    tokens =[mo for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']
    
    ast = {"Space": None, "Components": [], "Routes":[]}
    i = 0
    while i < len(tokens):
        kind, val = tokens[i].lastgroup, tokens[i].group()
        
        # Parse Space
        if val == 'define' and tokens[i+1].group() == 'Space':
            ast["Space"] = {"name": tokens[i+2].group().strip('"')}
        elif val == 'dimensions':
            ast["Space"]["dim"] = (float(tokens[i+2].group().replace('mm','')), 
                                   float(tokens[i+4].group().replace('mm','')), 
                                   float(tokens[i+6].group().replace('mm','')))
        elif val == 'grid':
            ast["Space"]["grid"] = (int(tokens[i+2].group()), int(tokens[i+4].group()), int(tokens[i+6].group()))
        
        # Parse Components
        elif val == 'add':
            ast["Components"].append({
                "type": tokens[i+1].group(), "name": tokens[i+3].group(),
                "coords": eval(tokens[i+5].group()), "rotation": tokens[i+7].group()
            })
            
        # Parse Routes (BUG FIXED: Dynamically find waypoints)
        elif val == 'route':
            route_name = f"{tokens[i+1].group()}_to_{tokens[i+3].group()}"
            waypoints =[]
            j = i + 1
            # Fast forward to the first waypoint
            while j < len(tokens) and tokens[j].lastgroup != 'LIST_ITEM':
                j += 1
            # Collect all waypoints
            while j < len(tokens) and tokens[j].lastgroup == 'LIST_ITEM':
                clean_coord = tokens[j].group().replace('-', '').strip()
                waypoints.append(eval(clean_coord))
                j += 1
            ast["Routes"].append({"name": route_name, "waypoints": waypoints})
            i = j - 1
        i += 1
    return ast

# =====================================================================
# PHASE 1-4: THE PHYSICS ENGINE & 3D TENSOR GRID
# =====================================================================
class HardwareCompiler:
    def __init__(self, ast):
        self.ast = ast
        self.grid = ast["Space"]["grid"]
        self.dim = ast["Space"]["dim"]
        self.voxel_size = self.dim[0] / self.grid[0]
        self.tensor = np.ones((self.grid[2], self.grid[0], self.grid[1]), dtype=np.int8)
        
        print("📚 Loading Materials Database...")
        with open('standard-materials.yaml', 'r') as f:
            self.db = yaml.safe_load(f)

    def draw_line(self, p1, p2):
        z1, x1, y1 = p1[0]-1, p1[1]-1, p1[2]-1
        z2, x2, y2 = p2[0]-1, p2[1]-1, p2[2]-1
        points =[]
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        x, y = x1, y1
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                points.append((z1, x, y))
                err -= dy
                if err < 0:
                    y += sy; err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                points.append((z1, x, y))
                err -= dx
                if err < 0:
                    x += sx; err += dy
                y += sy
        points.append((z1, x, y))
        return points

    def compile(self):
        print(f"\n⚙️  Compiling Space: {self.ast['Space']['name']}")
        for route in self.ast["Routes"]:
            print(f"   🛤️ Routing: {route['name']}")
            waypoints = route["waypoints"]
            trace_voxels = 0
            
            for i in range(len(waypoints)-1):
                path = self.draw_line(waypoints[i], waypoints[i+1])
                for z, x, y in path:
                    self.tensor[z, x, y] = 2 # COPPER
                    trace_voxels += 1
            
            # Physics Calculation
            rho = float(self.db['conductors']['copper']['resistivity_ohm_m'])
            length_m = (trace_voxels * self.voxel_size) * 1e-3
            area_m2 = (self.voxel_size * 1e-3) * (0.035 * 1e-3)
            resistance = rho * (length_m / area_m2)
            print(f"      ✅ Physics Check: Trace Resistance = {resistance:.4f} Ω")

# =====================================================================
# PHASE 6: UNIVERSAL EXPORTERS
# =====================================================================
    def export(self):
        os.makedirs("build", exist_ok=True)
        
        # 1. GERBER EXPORT (FIXED)
        with open("build/board.gtl", "w") as f:
            # FIXED: Changed X26Y26 to X24Y24 to match the * 10000 multiplier.
            # FIXED: Changed ADD10C (Circle) to ADD10R (Rectangle) for better voxel representation.
            f.write(f"%FSLAX24Y24*%\n%MOMM*%\n%ADD10R,{self.voxel_size:.4f}X{self.voxel_size:.4f}*%\nD10*\n")
            for x in range(self.grid[0]):
                for y in range(self.grid[1]):
                    if self.tensor[0, x, y] == 2:
                        # FIXED: Center the voxel coordinates
                        real_x = x * self.voxel_size + (self.voxel_size / 2)
                        real_y = y * self.voxel_size + (self.voxel_size / 2)
                        gx, gy = int(real_x * 10000), int(real_y * 10000)
                        # FIXED: Use D03 (Flash Pad) instead of D01 (Draw Line)
                        f.write(f"X{gx:06d}Y{gy:06d}D03*\n")
            f.write("M02*\n")
        print("   ✅ Exported: build/board.gtl")

        # 2. BLENDER PYTHON EXPORT
        with open("build/sim.py", "w") as f:
            f.write("import bpy\nbpy.ops.wm.read_factory_settings(use_empty=True)\n")
            w, h = self.dim[0], self.dim[1]
            f.write(f"bpy.ops.mesh.primitive_cube_add(size=1, location=({w/2}, {h/2}, -0.5), scale=({w}, {h}, 1))\n")
            f.write("bpy.context.scene.objects[-1].name = 'FR4_Substrate'\n")
            for x in range(self.grid[0]):
                for y in range(self.grid[1]):
                    if self.tensor[0, x, y] == 2:
                        rx, ry = x * self.voxel_size, y * self.voxel_size
                        f.write(f"bpy.ops.mesh.primitive_cube_add(size={self.voxel_size}, location=({rx}, {ry}, 0.5))\n")
                        f.write("bpy.context.scene.objects[-1].name = 'Copper'\n")
        print("   ✅ Exported: build/sim.py")

        # 3. UNIVERSAL OBJ EXPORT (BUG FIXED: Now includes Copper Traces!)
        with open("build/board.obj", "w") as f:
            f.write("# Hardware Script Universal 3D Export\n")
            w, h = self.dim[0], self.dim[1]
            v_idx = 1
            
            # Draw FR4 Base
            f.write("o FR4_Substrate\n")
            f.write(f"v 0 0 -1\nv {w} 0 -1\nv {w} {h} -1\nv 0 {h} -1\n")
            f.write(f"v 0 0 0\nv {w} 0 0\nv {w} {h} 0\nv 0 {h} 0\n")
            f.write(f"f {v_idx} {v_idx+1} {v_idx+2} {v_idx+3}\nf {v_idx+4} {v_idx+5} {v_idx+6} {v_idx+7}\nf {v_idx} {v_idx+1} {v_idx+5} {v_idx+4}\nf {v_idx+1} {v_idx+2} {v_idx+6} {v_idx+5}\nf {v_idx+2} {v_idx+3} {v_idx+7} {v_idx+6}\nf {v_idx+3} {v_idx} {v_idx+4} {v_idx+7}\n")
            v_idx += 8
            
            # Draw Copper Voxels
            f.write("o Copper_Traces\n")
            vs = self.voxel_size
            for x in range(self.grid[0]):
                for y in range(self.grid[1]):
                    if self.tensor[0, x, y] == 2:
                        rx, ry = x * vs, y * vs
                        f.write(f"v {rx} {ry} 0\nv {rx+vs} {ry} 0\nv {rx+vs} {ry+vs} 0\nv {rx} {ry+vs} 0\n")
                        f.write(f"v {rx} {ry} 0.5\nv {rx+vs} {ry} 0.5\nv {rx+vs} {ry+vs} 0.5\nv {rx} {ry+vs} 0.5\n")
                        f.write(f"f {v_idx} {v_idx+1} {v_idx+2} {v_idx+3}\nf {v_idx+4} {v_idx+5} {v_idx+6} {v_idx+7}\nf {v_idx} {v_idx+1} {v_idx+5} {v_idx+4}\nf {v_idx+1} {v_idx+2} {v_idx+6} {v_idx+5}\nf {v_idx+2} {v_idx+3} {v_idx+7} {v_idx+6}\nf {v_idx+3} {v_idx} {v_idx+4} {v_idx+7}\n")
                        v_idx += 8
        print("   ✅ Exported: build/board.obj")

# =====================================================================
# CLI ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    print("==================================================")
    print("🔥 HARDWARE SCRIPT COMPILER (v0.1 MVP)")
    print("==================================================\n")
    
    if len(sys.argv) < 3 or sys.argv[1] != "generate":
        print("Usage: python hw.py generate <filename.hw>")
        sys.exit(1)
        
    filepath = sys.argv[2]
    ast = parse_hw_file(filepath)
    compiler = HardwareCompiler(ast)
    compiler.compile()
    compiler.export()
    
    print("\n🎉 COMPILATION COMPLETE! All target files are in the 'build' folder.")