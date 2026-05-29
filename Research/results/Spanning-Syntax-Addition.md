# Spanning Syntax Addition - Professional Hardware Support

**Critical Enhancement**: Geometric Macros for Copper Pours and Ground Planes  
**Status**: ✅ Essential Addition to Level 5 Syntax  
**Date**: March 13, 2026  
**Maintains**: Complete explicit paradigm with deterministic expansion

---

## The Professional Hardware Gap

### The Problem Identified
Professional PCB and silicon design requires:
- **Ground Planes**: Solid copper sheets for electrical reference
- **Power Planes**: Solid copper sheets for power distribution  
- **Copper Pours**: Large copper areas for thermal management
- **Substrate Layers**: Complete material coverage across layers

**Current Syntax Limitation**: Forcing users to type `spanning [2, 1, 1] to [2, 50, 50]` for every solid plane is tedious and error-prone.

### The Solution: Geometric Macros
**Key Principle**: Deterministic shortcuts that expand to exact coordinates BEFORE Engine A physics calculations.

**No Violation of Explicit Paradigm**: These are mathematical transformations, not hidden algorithms.

---

## Enhanced Spanning Syntax

### 1. Entire Space Coverage (`all`)
**Use Case**: Base substrates (FR4, Silicon wafers)

```hw
# Expands to: [1, 1, 1] to [Z_max, X_max, Y_max]
add Substrate(FR4) spanning all
```

**Mathematical Expansion**:
```
For Space with grid: 50 by 50 by 4
"spanning all" → spanning [1, 1, 1] to [4, 50, 50]
```

### 2. Single Layer Coverage (`layer Z`)
**Use Case**: Ground planes, power planes, solid copper layers

```hw
# Expands to: [2, 1, 1] to [2, X_max, Y_max]  
add Copper named GroundPlane spanning layer 2

# Expands to: [3, 1, 1] to [3, X_max, Y_max]
add Copper named PowerPlane spanning layer 3
```

**Mathematical Expansion**:
```
For Space with grid: 50 by 50 by 4
"spanning layer 2" → spanning [2, 1, 1] to [2, 50, 50]
"spanning layer 3" → spanning [3, 1, 1] to [3, 50, 50]
```

### 3. Multi-Layer Coverage (`layers Z to Z`)
**Use Case**: Thick dielectric blocks, multi-layer substrates

```hw
# Expands to: [2, 1, 1] to [4, X_max, Y_max]
add Substrate(SiliconDioxide) spanning layers 2 to 4
```

**Mathematical Expansion**:
```
For Space with grid: 50 by 50 by 4
"spanning layers 2 to 4" → spanning [2, 1, 1] to [4, 50, 50]
```

---

## The Via Clearance Problem

### The Physics Reality
**Problem**: Via through solid copper plane creates electrical short
**Professional Solution**: Anti-pads (clearance holes around vias)
**Hardware Script Solution**: Explicit `clearance` parameter

### Explicit Clearance Syntax

```hw
route PowerSource.out to Motor.in:
    path:
        - [1, 10, 10]         # Start on Layer 1
        - [3, 10, 10]         # Via through Layer 2 to Layer 3
    clearance: 1mm            # EXPLICIT: Clear 1mm radius around via
```

**What This Does**:
1. Creates via hole at [2, 10, 10] (Layer 2 intersection)
2. Removes copper in 1mm radius around via on Layer 2
3. Prevents electrical short to GroundPlane
4. User explicitly commanded the clearance

### No Clearance = Physics Error

```hw
route PowerSource.out to Motor.in:
    path:
        - [1, 10, 10]
        - [3, 10, 10]         # Via through solid copper
    # NO clearance parameter = DEAD SHORT
```

**Engine A Response**:
```
❌ Fatal Electrical Error at Line 15: Dead Short Detected
  Via at [2, 10, 10] contacts GroundPlane copper
  Calculated Resistance: 0.001Ω (short circuit)
  Solution: Add 'clearance: Xmm' parameter to route block
```

**No Magic Fixes**: Engine A never automatically adds clearances

---

## Updated Language Specification

### Enhanced Grammar (EBNF)

```ebnf
spanning_clause = "spanning" spanning_target

spanning_target = "all" 
                | "layer" number
                | "layers" number "to" number
                | coordinate "to" coordinate

route_stmt = "route" socket_ref "to" socket_ref ":" 
             INDENT route_block DEDENT

route_block = path_stmt [ clearance_stmt ]

path_stmt = "path" ":" INDENT { coordinate } DEDENT

clearance_stmt = "clearance" ":" distance_value

distance_value = number unit
```

### Complete Syntax Examples

```hw
define Space "ProfessionalPCB":
    dimensions: 100mm by 80mm by 1.6mm
    grid: 1000 by 800 by 4
    
    # Base substrate across all layers
    add Substrate(FR4) spanning all
    
    # Layer 1: Component layer (top)
    # Layer 2: Ground plane (solid copper)
    add Copper named GroundPlane spanning layer 2
    
    # Layer 3: Power plane (solid copper) 
    add Copper named PowerPlane spanning layer 3
    
    # Layer 4: Component layer (bottom)
    
    # Components on top layer
    add Battery (5V) named Power at [1, 100, 100]
    add Motor named Load at [4, 900, 700] rotated South
    
    # Route with explicit clearance through planes
    route Power.VCC to PowerPlane:
        path:
            - [1, 100, 100]     # Start at battery
            - [3, 100, 100]     # Via to power plane
        clearance: 0.5mm        # Clear 0.5mm around via
    
    route PowerPlane to Load.VCC:
        path:
            - [3, 900, 700]     # Start at power plane
            - [4, 900, 700]     # Via to bottom layer
        clearance: 0.5mm        # Clear 0.5mm around via
    
    route Load.GND to GroundPlane:
        path:
            - [4, 900, 700]     # Start at motor
            - [2, 900, 700]     # Via to ground plane  
        clearance: 0.5mm        # Clear 0.5mm around via
```

---

## Engine A Implementation

### Spanning Expansion Algorithm

```python
def expand_spanning_clause(spanning_target: str, space: Space) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """Expand spanning shortcuts to exact coordinates"""
    
    max_z, max_x, max_y = space.grid.z_cells, space.grid.x_cells, space.grid.y_cells
    
    if spanning_target == "all":
        return (1, 1, 1), (max_z, max_x, max_y)
    
    elif spanning_target.startswith("layer "):
        layer_num = int(spanning_target.split()[1])
        return (layer_num, 1, 1), (layer_num, max_x, max_y)
    
    elif "layers" in spanning_target and "to" in spanning_target:
        # Parse "layers 2 to 4"
        parts = spanning_target.split()
        start_layer = int(parts[1])
        end_layer = int(parts[3])
        return (start_layer, 1, 1), (end_layer, max_x, max_y)
    
    else:
        # Explicit coordinate range - parse normally
        return parse_coordinate_range(spanning_target)
```

### Clearance Implementation

```python
def apply_via_clearance(space: Space, via_pos: Tuple[int, int, int], 
                       clearance_mm: float, affected_layers: List[int]):
    """Remove copper around via for specified clearance"""
    
    # Convert clearance from mm to voxels
    clearance_voxels = int(clearance_mm / space.voxel_size[0])
    
    z, x, y = via_pos
    
    for layer in affected_layers:
        # Clear circular area around via
        for dx in range(-clearance_voxels, clearance_voxels + 1):
            for dy in range(-clearance_voxels, clearance_voxels + 1):
                if dx*dx + dy*dy <= clearance_voxels*clearance_voxels:
                    clear_x, clear_y = x + dx, y + dy
                    
                    if space.is_valid_position(layer, clear_x, clear_y):
                        if space.cells[layer, clear_x, clear_y] == CellState.COPPER:
                            space.cells[layer, clear_x, clear_y] = CellState.EMPTY
```

### Short Circuit Detection

```python
def validate_via_clearances(space: Space, routes: List[Route]) -> List[str]:
    """Detect electrical shorts from vias contacting copper planes"""
    
    errors = []
    
    for route in routes:
        for i in range(len(route.waypoints) - 1):
            start = route.waypoints[i]
            end = route.waypoints[i + 1]
            
            # Check for layer changes (vias)
            if start[0] != end[0] and start[1] == end[1] and start[2] == end[2]:
                via_x, via_y = start[1], start[2]
                
                # Check all layers between start and end
                min_layer, max_layer = min(start[0], end[0]), max(start[0], end[0])
                
                for layer in range(min_layer + 1, max_layer):
                    if space.cells[layer, via_x, via_y] == CellState.COPPER:
                        if not route.clearance:
                            errors.append(
                                f"Dead short: Via at [{layer}, {via_x}, {via_y}] "
                                f"contacts copper plane. Add clearance parameter."
                            )
    
    return errors
```

---

## Professional Design Examples

### Multi-Layer PCB with Power Distribution

```hw
define Space "PowerDistributionBoard":
    dimensions: 50mm by 50mm by 1.6mm
    grid: 500 by 500 by 4
    
    # Standard 4-layer stackup
    add Substrate(FR4) spanning all
    add Copper named TopLayer spanning layer 1      # Components
    add Copper named GroundPlane spanning layer 2   # Solid ground
    add Copper named PowerPlane spanning layer 3    # Solid +5V
    add Copper named BottomLayer spanning layer 4   # Components
    
    # Power input
    add Battery (5V) named MainPower at [1, 50, 50]
    
    # Multiple loads
    add Motor named Motor1 at [4, 150, 150]
    add LED named Status at [4, 350, 350] 
    add Sensor named Temp at [1, 450, 450]
    
    # Power distribution through planes
    route MainPower.VCC to PowerPlane:
        path:
            - [1, 50, 50]
            - [3, 50, 50]
        clearance: 1mm
    
    route MainPower.GND to GroundPlane:
        path:
            - [1, 50, 50]
            - [2, 50, 50]
        clearance: 1mm
    
    # Loads connect to planes
    route PowerPlane to Motor1.VCC:
        path:
            - [3, 150, 150]
            - [4, 150, 150]
        clearance: 0.5mm
    
    route Motor1.GND to GroundPlane:
        path:
            - [4, 150, 150]
            - [2, 150, 150]
        clearance: 0.5mm
```

### Silicon Chip with Metal Layers

```hw
define Space "CustomProcessor":
    dimensions: 5mm by 5mm by 0.1mm
    grid: 50000 by 50000 by 10
    
    # Silicon substrate
    add Substrate(Silicon) spanning layer 1
    
    # Dielectric layers
    add Substrate(SiliconDioxide) spanning layers 2 to 10
    
    # Metal routing layers
    add Copper named Metal1 spanning layer 3
    add Copper named Metal2 spanning layer 5  
    add Copper named Metal3 spanning layer 7
    
    # Logic gates in silicon
    add CMOS_NAND_Gate named Gate1 at [1, 1000, 1000]
    add CMOS_NAND_Gate named Gate2 at [1, 3000, 1000]
    
    # Interconnect through metal layers
    route Gate1.out to Gate2.in:
        path:
            - [1, 1000, 1000]   # Start in silicon
            - [3, 1000, 1000]   # Up to Metal1
            - [3, 3000, 1000]   # Route across Metal1
            - [1, 3000, 1000]   # Down to silicon
        clearance: 0.1um       # Nanometer-scale clearance
```

---

## Benefits of Enhanced Syntax

### Professional Workflow Support
- **Ground Planes**: Essential for signal integrity and EMI control
- **Power Distribution**: Efficient power delivery with minimal resistance
- **Thermal Management**: Large copper areas for heat dissipation
- **Manufacturing Standard**: Matches professional PCB design practices

### Maintains Explicit Paradigm
- **Deterministic Expansion**: All shortcuts expand to exact coordinates
- **No Hidden Behavior**: User sees exactly what gets created
- **Physics Validation**: Engine A validates the expanded geometry
- **Error Transparency**: Clear feedback when clearances are missing

### Scalability Across Domains
- **PCB Design**: Multi-layer boards with power/ground planes
- **Silicon Design**: Metal routing layers with via clearances
- **Industrial**: Large copper pours for high-current applications
- **Educational**: Simple examples without tedious coordinate typing

---

## Conclusion

This enhancement transforms Hardware Script from an academic exercise into a professional-grade tool capable of real-world PCB and silicon design. The spanning syntax provides the convenience needed for practical use while maintaining our core principle of explicit, deterministic behavior.

**Key Achievements**:
- ✅ Professional hardware design patterns supported
- ✅ Explicit paradigm maintained (no magic behavior)
- ✅ Deterministic coordinate expansion
- ✅ Physics-based short circuit detection
- ✅ User-controlled clearance management

**Result**: Hardware Script now supports the full spectrum of professional hardware design while remaining mathematically rigorous and completely predictable.

---

**Enhancement Status**: ✅ Critical Addition Complete  
**Explicit Paradigm**: ✅ Maintained  
**Professional Capability**: ✅ Achieved  
**Ready for Implementation**: ✅ Yes