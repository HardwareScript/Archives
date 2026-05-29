# Python MVP Implementation Roadmap

**Hardware Script Engine A - Development Plan**  
**Target**: Functional Python prototype demonstrating core physics engine  
**Timeline**: 4-6 weeks for complete MVP  
**Architecture**: Based on locked Level 0-5 specification

---

## MVP Scope Definition

### What the MVP Will Demonstrate
1. **Parse .hw files** with explicit syntax (no magic keywords)
2. **3D tensor grid** with component placement and rotation
3. **Explicit waypoint routing** with via generation
4. **Basic physics simulation** using Level 1 materials + Level 2 laws
5. **Safety validation** with thermal and electrical limits
6. **Manufacturing output** (Gerber files for PCB fabrication)

### What the MVP Will NOT Include
- Advanced 3D simulation (Blender export)
- Complete standard library (just basic components)
- Package management system
- IDE integration
- Silicon manufacturing (GDSII output)

---

## Development Phases

### Phase 1: Core Infrastructure (Week 1)

#### 1.1 Project Setup
```bash
mkdir hardware-script-mvp
cd hardware-script-mvp
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install numpy scipy matplotlib pyyaml
```

#### 1.2 Basic Data Structures
**File**: `src/core/space.py`
```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional

@dataclass
class Dimensions:
    width_mm: float
    height_mm: float
    depth_mm: float

@dataclass
class Grid:
    x_cells: int
    y_cells: int
    z_cells: int

class CellState:
    EMPTY = 0
    COPPER = 1
    PAD = 2
    HOLE = 3
    COMPONENT = 4

class Space:
    def __init__(self, name: str, dimensions: Dimensions, grid: Grid):
        self.name = name
        self.dimensions = dimensions
        self.grid = grid
        
        # Calculate voxel size
        self.voxel_size = (
            dimensions.width_mm / grid.x_cells,
            dimensions.height_mm / grid.y_cells,
            dimensions.depth_mm / grid.z_cells
        )
        
        # Initialize 3D tensor
        self.cells = np.zeros((grid.z_cells, grid.x_cells, grid.y_cells), dtype=int)
        
        # Component and route tracking
        self.components = []
        self.routes = []
```

#### 1.3 Materials Database Integration
**File**: `src/materials/database.py`
```python
import yaml
from pathlib import Path

class MaterialsDatabase:
    def __init__(self, yaml_path: str = "data/standard-materials.yaml"):
        with open(yaml_path, 'r') as f:
            self.data = yaml.safe_load(f)
    
    def get_conductor(self, name: str) -> dict:
        return self.data['conductors'][name]
    
    def get_insulator(self, name: str) -> dict:
        return self.data['insulators'][name]
    
    def get_semiconductor(self, name: str) -> dict:
        return self.data['semiconductors'][name]
    
    def get_resistive_material(self, name: str) -> dict:
        return self.data['resistive_materials'][name]
```

### Phase 2: Lexer and Parser (Week 2)

#### 2.1 Lexer Implementation
**File**: `src/parser/lexer.py`
```python
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Iterator

class TokenType(Enum):
    # Keywords
    IMPORT = "import"
    FROM = "from"
    DEFINE = "define"
    ADD = "add"
    ROUTE = "route"
    
    # Types
    SPACE = "Space"
    COMPONENT = "Component"
    MATERIAL = "Material"
    
    # Identifiers and literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    COORDINATE = "COORDINATE"
    
    # Symbols
    COLON = ":"
    COMMA = ","
    DOT = "."
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        
    def tokenize(self) -> List[Token]:
        tokens = []
        while self.pos < len(self.text):
            token = self.next_token()
            if token:
                tokens.append(token)
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
```

#### 2.2 Parser Implementation  
**File**: `src/parser/parser.py`
```python
from typing import List, Optional, Dict, Any
from .lexer import Token, TokenType, Lexer

class ASTNode:
    pass

@dataclass
class ImportNode(ASTNode):
    component: str
    package: str

@dataclass
class SpaceNode(ASTNode):
    name: str
    dimensions: tuple
    grid: tuple
    components: List['ComponentNode']
    routes: List['RouteNode']

@dataclass
class ComponentNode(ASTNode):
    type: str
    name: str
    position: Optional[tuple]
    rotation: Optional[str]
    spanning: Optional[str]  # "all", "layer 2", "layers 2 to 4"
    parameters: Dict[str, Any]

@dataclass
class RouteNode(ASTNode):
    source: str
    destination: str
    waypoints: List[tuple]
    clearance: Optional[float]  # Clearance in mm
    trace_width: Optional[float]
    max_current: Optional[float]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        
    def parse(self) -> List[ASTNode]:
        nodes = []
        while not self.is_at_end():
            node = self.parse_statement()
            if node:
                nodes.append(node)
        return nodes
    
    def parse_spanning_clause(self) -> Optional[str]:
        """Parse spanning shortcuts: all, layer N, layers N to M"""
        if self.match(TokenType.IDENTIFIER, "spanning"):
            if self.match(TokenType.IDENTIFIER, "all"):
                return "all"
            elif self.match(TokenType.IDENTIFIER, "layer"):
                layer_num = self.consume(TokenType.NUMBER).value
                return f"layer {layer_num}"
            elif self.match(TokenType.IDENTIFIER, "layers"):
                start = self.consume(TokenType.NUMBER).value
                self.consume(TokenType.IDENTIFIER, "to")
                end = self.consume(TokenType.NUMBER).value
                return f"layers {start} to {end}"
        return None
```

### Phase 3: Component System (Week 3)

#### 3.1 Component Definitions
**File**: `src/components/base.py`
```python
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class Pin:
    name: str
    local_pos: Tuple[int, int]  # Local coordinates within component
    
@dataclass
class ComponentDefinition:
    name: str
    grid_size: Tuple[int, int]  # Local grid dimensions
    body_cells: List[Tuple[int, int]]  # Cells occupied by component body
    pins: List[Pin]
    material: str
    render_mesh: Optional[str] = None

class ComponentInstance:
    def __init__(self, definition: ComponentDefinition, name: str, 
                 global_pos: Tuple[int, int, int], rotation: str = "North"):
        self.definition = definition
        self.name = name
        self.global_pos = global_pos
        self.rotation = rotation
        
        # Calculate global pin positions
        self.global_pins = self._calculate_global_pins()
    
    def _calculate_global_pins(self) -> Dict[str, Tuple[int, int, int]]:
        """Apply rotation matrix and translate to global coordinates"""
        rotation_matrix = self._get_rotation_matrix(self.rotation)
        global_pins = {}
        
        for pin in self.definition.pins:
            # Apply rotation
            rotated_pos = self._apply_rotation(pin.local_pos, rotation_matrix)
            
            # Translate to global coordinates
            global_pos = (
                self.global_pos[0],  # Z unchanged
                self.global_pos[1] + rotated_pos[0],
                self.global_pos[2] + rotated_pos[1]
            )
            global_pins[pin.name] = global_pos
            
        return global_pins
```

#### 3.2 Standard Component Library
**File**: `src/components/standard.py`
```python
from .base import ComponentDefinition, Pin

# Basic components for MVP
TRANSISTOR_NPN = ComponentDefinition(
    name="Transistor_NPN",
    grid_size=(3, 3),
    body_cells=[(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)],
    pins=[
        Pin("Collector", (0, 1)),
        Pin("Base", (1, 0)),
        Pin("Emitter", (2, 1))
    ],
    material="Silicon"
)

RESISTOR = ComponentDefinition(
    name="Resistor",
    grid_size=(1, 3),
    body_cells=[(0,0), (0,1), (0,2)],
    pins=[
        Pin("in", (0, 0)),
        Pin("out", (0, 2))
    ],
    material="Carbon_Film"
)

BATTERY = ComponentDefinition(
    name="Battery",
    grid_size=(2, 2),
    body_cells=[(0,0), (0,1), (1,0), (1,1)],
    pins=[
        Pin("VCC", (0, 0)),
        Pin("GND", (1, 1))
    ],
    material="Lithium"
)
```

### Phase 4: Routing Engine (Week 4)

#### 4.1 Waypoint Router with Clearance Support
**File**: `src/routing/router.py`
```python
import numpy as np
from typing import List, Tuple, Optional
from ..core.space import Space, CellState

class Router:
    def __init__(self, space: Space):
        self.space = space
    
    def route_connection(self, waypoints: List[Tuple[int, int, int]], 
                        trace_width: int = 1, clearance_mm: Optional[float] = None) -> bool:
        """Route copper trace through waypoints with optional clearance"""
        
        via_positions = []  # Track vias for clearance application
        
        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            
            if start[0] == end[0]:  # Same layer - draw trace
                self._draw_trace(start, end, trace_width)
            else:  # Layer change - create via
                if start[1] == end[1] and start[2] == end[2]:
                    via_pos = self._create_via(start, end)
                    via_positions.append(via_pos)
                else:
                    raise ValueError(f"Invalid via: {start} -> {end}. "
                                   "Via requires same X,Y coordinates")
        
        # Apply clearance around vias if specified
        if clearance_mm and via_positions:
            self._apply_clearances(via_positions, clearance_mm)
        
        return True
    
    def _apply_clearances(self, via_positions: List[Tuple[int, int, int]], 
                         clearance_mm: float):
        """Remove copper around vias for specified clearance"""
        clearance_voxels = int(clearance_mm / self.space.voxel_size[0])
        
        for via_z, via_x, via_y in via_positions:
            # Find layers with solid copper that need clearance
            for z in range(self.space.grid.z_cells):
                if z != via_z:  # Don't clear the via layer itself
                    # Check if this layer has copper at via position
                    if (self.space.cells[z, via_x, via_y] == CellState.COPPER):
                        # Clear circular area around via
                        self._clear_circular_area(z, via_x, via_y, clearance_voxels)
    
    def _clear_circular_area(self, layer: int, center_x: int, center_y: int, 
                           radius_voxels: int):
        """Clear circular area of copper around a point"""
        for dx in range(-radius_voxels, radius_voxels + 1):
            for dy in range(-radius_voxels, radius_voxels + 1):
                if dx*dx + dy*dy <= radius_voxels*radius_voxels:
                    clear_x, clear_y = center_x + dx, center_y + dy
                    
                    if self._is_valid_position(layer, clear_x, clear_y):
                        if self.space.cells[layer, clear_x, clear_y] == CellState.COPPER:
                            self.space.cells[layer, clear_x, clear_y] = CellState.EMPTY
    
    def validate_via_clearances(self, routes: List['RouteNode']) -> List[str]:
        """Detect electrical shorts from vias contacting copper planes"""
        errors = []
        
        for route in routes:
            if not route.clearance:  # No clearance specified
                # Check for layer changes that might short
                for i in range(len(route.waypoints) - 1):
                    start = route.waypoints[i]
                    end = route.waypoints[i + 1]
                    
                    if (start[0] != end[0] and start[1] == end[1] and start[2] == end[2]):
                        # This is a via - check for shorts
                        via_x, via_y = start[1], start[2]
                        min_layer = min(start[0], end[0])
                        max_layer = max(start[0], end[0])
                        
                        for layer in range(min_layer + 1, max_layer):
                            if self.space.cells[layer, via_x, via_y] == CellState.COPPER:
                                errors.append(
                                    f"Dead short: Via at [{layer}, {via_x}, {via_y}] "
                                    f"contacts copper plane. Add clearance parameter."
                                )
        
        return errors
```
    
    def _draw_trace(self, start: Tuple[int, int, int], 
                   end: Tuple[int, int, int], width: int):
        """Draw copper trace between two points on same layer"""
        z = start[0]
        
        # Bresenham's line algorithm for 2D path
        x0, y0 = start[1], start[2]
        x1, y1 = end[1], end[2]
        
        points = self._bresenham_line(x0, y0, x1, y1)
        
        for x, y in points:
            if self._is_valid_position(z, x, y):
                if self.space.cells[z, x, y] != CellState.EMPTY:
                    raise ValueError(f"Collision at [{z}, {x}, {y}]")
                self.space.cells[z, x, y] = CellState.COPPER
    
    def _create_via(self, start: Tuple[int, int, int], end: Tuple[int, int, int]):
        """Create via between layers"""
        x, y = start[1], start[2]
        
        # Mark both layers as having vias
        self.space.cells[start[0], x, y] = CellState.HOLE
        self.space.cells[end[0], x, y] = CellState.HOLE
    
    def _bresenham_line(self, x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
        """Bresenham's line algorithm"""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            points.append((x0, y0))
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
                
        return points
```

### Phase 5: Physics Engine (Week 5)

#### 5.1 Modified Nodal Analysis (MNA) Solver
**File**: `src/physics/mna_solver.py`
```python
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from typing import Dict, List, Tuple
from ..materials.database import MaterialsDatabase

class MNASolver:
    def __init__(self, space, materials_db: MaterialsDatabase):
        self.space = space
        self.materials_db = materials_db
        self.node_map = {}  # Maps (z,x,y) to node index
        self.resistances = {}  # Maps node pairs to resistance values
        
    def solve_circuit(self) -> Dict[str, float]:
        """Solve circuit using Modified Nodal Analysis"""
        
        # 1. Build node mapping
        self._build_node_map()
        
        # 2. Calculate resistances for all copper cells
        self._calculate_resistances()
        
        # 3. Build conductance matrix
        G_matrix = self._build_conductance_matrix()
        
        # 4. Build current vector (boundary conditions)
        I_vector = self._build_current_vector()
        
        # 5. Solve for voltages
        V_solution = spsolve(G_matrix, I_vector)
        
        # 6. Calculate currents and power
        results = self._calculate_results(V_solution)
        
        return results
    
    def _calculate_resistances(self):
        """Calculate resistance for each copper cell using Level 1 materials"""
        copper_props = self.materials_db.get_conductor('copper')
        resistivity = copper_props['resistivity_ohm_m']
        
        # For MVP: assume uniform trace geometry
        voxel_volume = (self.space.voxel_size[0] * 1e-3) * \
                      (self.space.voxel_size[1] * 1e-3) * \
                      (self.space.voxel_size[2] * 1e-3)
        
        # R = ρ × (L / A) - Level 2 Law 1
        length = self.space.voxel_size[0] * 1e-3  # Convert mm to m
        area = (self.space.voxel_size[1] * 1e-3) * (self.space.voxel_size[2] * 1e-3)
        
        resistance_per_cell = resistivity * (length / area)
        
        # Store resistance for each copper cell connection
        for z in range(self.space.grid.z_cells):
            for x in range(self.space.grid.x_cells):
                for y in range(self.space.grid.y_cells):
                    if self.space.cells[z, x, y] == CellState.COPPER:
                        node_id = self.node_map.get((z, x, y))
                        if node_id is not None:
                            # Connect to adjacent copper cells
                            self._add_adjacent_resistances(z, x, y, resistance_per_cell)
```

#### 5.2 Thermal Analysis
**File**: `src/physics/thermal.py`
```python
from typing import Dict
from ..materials.database import MaterialsDatabase

class ThermalAnalyzer:
    def __init__(self, materials_db: MaterialsDatabase):
        self.materials_db = materials_db
    
    def analyze_thermal_limits(self, currents: Dict[str, float], 
                             resistances: Dict[str, float]) -> Dict[str, bool]:
        """Apply Level 2 Law 5: P = I² × R thermal analysis"""
        
        thermal_results = {}
        
        for node, current in currents.items():
            if node in resistances:
                # Calculate power dissipation
                power_watts = current ** 2 * resistances[node]
                
                # Get material thermal properties
                copper_props = self.materials_db.get_conductor('copper')
                thermal_conductivity = copper_props['thermal_conductivity_w_mk']
                max_temp = copper_props.get('max_operating_temp_c', 85)  # Default limit
                
                # Simple thermal model: ΔT = P × R_thermal
                # For MVP: use simplified thermal resistance
                thermal_resistance = 1.0 / thermal_conductivity  # Simplified
                temp_rise = power_watts * thermal_resistance
                
                # Check if within limits
                thermal_results[node] = temp_rise < max_temp
                
                if temp_rise >= max_temp:
                    print(f"⚠️  Thermal Warning at {node}: "
                          f"Temperature rise {temp_rise:.1f}°C exceeds limit {max_temp}°C")
        
        return thermal_results
```

### Phase 6: Integration and Testing (Week 6)

#### 6.1 Main Engine Integration
**File**: `src/engine.py`
```python
from .parser.lexer import Lexer
from .parser.parser import Parser
from .core.space import Space, Dimensions, Grid
from .materials.database import MaterialsDatabase
from .routing.router import Router
from .physics.mna_solver import MNASolver
from .physics.thermal import ThermalAnalyzer

class HardwareScriptEngine:
    def __init__(self):
        self.materials_db = MaterialsDatabase()
        
    def compile_hw_file(self, hw_content: str) -> dict:
        """Main compilation pipeline"""
        
        # Phase 1: Parse .hw file
        lexer = Lexer(hw_content)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        
        # Phase 2: Build space and place components
        space = self._build_space(ast_nodes)
        
        # Phase 3: Route connections
        router = Router(space)
        self._execute_routing(ast_nodes, router)
        
        # Phase 4: Physics simulation
        mna_solver = MNASolver(space, self.materials_db)
        electrical_results = mna_solver.solve_circuit()
        
        thermal_analyzer = ThermalAnalyzer(self.materials_db)
        thermal_results = thermal_analyzer.analyze_thermal_limits(
            electrical_results['currents'], 
            electrical_results['resistances']
        )
        
        # Phase 5: Validation
        validation_results = self._validate_design(space, electrical_results, thermal_results)
        
        return {
            'space': space,
            'electrical': electrical_results,
            'thermal': thermal_results,
            'validation': validation_results,
            'success': validation_results['passed']
        }
```

#### 6.2 CLI Interface
**File**: `hw_cli.py`
```python
#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from src.engine import HardwareScriptEngine

def main():
    parser = argparse.ArgumentParser(description='Hardware Script Compiler')
    parser.add_argument('command', choices=['verify', 'generate'], 
                       help='Command to execute')
    parser.add_argument('file', help='Hardware Script (.hw) file to process')
    parser.add_argument('--output', '-o', help='Output directory')
    
    args = parser.parse_args()
    
    # Read .hw file
    hw_file = Path(args.file)
    if not hw_file.exists():
        print(f"❌ Error: File {args.file} not found")
        sys.exit(1)
    
    hw_content = hw_file.read_text()
    
    # Initialize engine
    engine = HardwareScriptEngine()
    
    try:
        # Compile
        results = engine.compile_hw_file(hw_content)
        
        if args.command == 'verify':
            if results['success']:
                print("✅ Verification Successful: 0 Errors")
            else:
                print("❌ Verification Failed:")
                for error in results['validation']['errors']:
                    print(f"  {error}")
                sys.exit(1)
                
        elif args.command == 'generate':
            if results['success']:
                # Generate output files
                output_dir = Path(args.output or 'build')
                output_dir.mkdir(exist_ok=True)
                
                # For MVP: generate simple text output
                with open(output_dir / 'circuit_analysis.txt', 'w') as f:
                    f.write("Hardware Script Compilation Results\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(f"Space: {results['space'].name}\n")
                    f.write(f"Dimensions: {results['space'].dimensions}\n")
                    f.write(f"Grid: {results['space'].grid}\n\n")
                    f.write("Electrical Analysis:\n")
                    for node, voltage in results['electrical']['voltages'].items():
                        f.write(f"  Node {node}: {voltage:.3f}V\n")
                
                print(f"✅ Generated output files in {output_dir}")
            else:
                print("❌ Cannot generate: Validation failed")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Compilation Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_parser.py
def test_parse_simple_space():
    hw_code = '''
    define Space "TestBoard":
        dimensions: 10mm by 10mm by 2mm
        grid: 10 by 10 by 2
    '''
    
    lexer = Lexer(hw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast) == 1
    assert ast[0].name == "TestBoard"

# tests/test_routing.py  
def test_simple_route():
    space = Space("Test", Dimensions(10, 10, 2), Grid(10, 10, 2))
    router = Router(space)
    
    waypoints = [(0, 0, 0), (0, 5, 0), (0, 5, 5)]
    success = router.route_connection(waypoints)
    
    assert success
    assert space.cells[0, 2, 0] == CellState.COPPER  # Midpoint should be copper
```

### Integration Tests
```python
# tests/test_integration.py
def test_complete_compilation():
    hw_code = '''
    import Battery from standard.power
    import Resistor from standard.components
    
    define Space "SimpleCircuit":
        dimensions: 20mm by 20mm by 2mm
        grid: 20 by 20 by 2
        
        add Battery (5V) named Power at [1, 5, 5]
        add Resistor (1k) named R1 at [1, 15, 5]
        
        route Power.VCC to R1.in:
            path:
                - [1, 5, 5]
                - [1, 15, 5]
    '''
    
    engine = HardwareScriptEngine()
    results = engine.compile_hw_file(hw_code)
    
    assert results['success']
    assert 'voltages' in results['electrical']
    assert len(results['validation']['errors']) == 0
```

---

## Success Criteria

### MVP Completion Checklist
- [ ] Parse complete .hw syntax (imports, define, add, route)
- [ ] 3D tensor grid with component placement
- [ ] Component rotation (North/South/East/West)
- [ ] Explicit waypoint routing with via generation
- [ ] Materials database integration (8 core materials)
- [ ] Basic MNA solver for electrical analysis
- [ ] Thermal limit validation
- [ ] CLI interface (hw verify, hw generate)
- [ ] Unit and integration test suite
- [ ] Example .hw files demonstrating functionality

### Performance Targets
- Parse and validate 100-component design in <1 second
- Solve electrical analysis for 1000-node circuit in <5 seconds
- Generate manufacturing output files in <2 seconds
- Memory usage <100MB for typical designs

### Quality Metrics
- 100% explicit syntax (no auto-generation)
- All physics calculations traceable to Level 1-2 specifications
- Error messages provide actionable feedback
- Generated output compatible with standard PCB fabrication

---

## Conclusion

This roadmap provides a complete path from architectural specification to working Python MVP. The implementation follows our locked Level 0-5 architecture with zero compromises on the explicit paradigm.

**Key Success Factors**:
- Strict adherence to explicit-only syntax
- Mathematical rigor in all physics calculations
- Comprehensive testing at each phase
- Clear separation of concerns between parsing, physics, and output generation

**Expected Outcome**: A functional Hardware Script compiler that demonstrates the revolutionary potential of text-based, AI-native hardware design while maintaining professional engineering accuracy.

**Ready to Begin**: All architectural decisions are locked, materials database is complete, and implementation path is clearly defined.