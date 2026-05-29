# Hardware Script v0.1 - Live Test

This directory contains the working MVP compiler and test verification.

---

## Contents

- **hw.py** - The compiler (180 lines)
- **test_board.hw** - Example hardware design (9 lines)
- **standard-materials.yaml** - Materials database (100+ lines)
- **build/** - Generated output files
- **output/** - Visual verification screenshots
- **TEST-VERIFICATION.md** - Complete test report

---

## Quick Start

### Compile the Test Board

```bash
python hw.py generate test_board.hw
```

### Expected Output

```
==================================================
🔥 HARDWARE SCRIPT COMPILER (v0.1 MVP)
==================================================

📖 Reading test_board.hw...
📚 Loading Materials Database...
⚙️  Compiling Space: First_MVP_Board
   🛤️ Routing: MainSwitch.Collector_to_Power.Out
      ✅ Physics Check: Trace Resistance = 0.0101 Ω
   ✅ Exported: build/board.gtl
   ✅ Exported: build/sim.py
   ✅ Exported: build/board.obj
🎉 COMPILATION COMPLETE!
```

### View Outputs

```bash
# List generated files
ls build/

# View OBJ in online viewer
# Upload build/board.obj to https://3dviewer.net/

# View in Blender
blender --python build/sim.py
```

---

## Test Board Design

**File**: `test_board.hw`

```hw
define Space "First_MVP_Board":
    dimensions: 20mm by 20mm by 2mm
    grid: 20 by 20 by 2

add Transistor_NPN named MainSwitch at [1, 5, 5] rotated North

route MainSwitch.Collector to Power.Out:
    path:
        - [1, 5, 6]
        - [1, 15, 6]
        - [1, 15, 15]
```

**What it creates**:
- 20mm × 20mm PCB board
- 1mm voxel resolution
- L-shaped copper trace
- 20 copper cells total

---

## Output Files

### build/board.gtl
- **Format**: Gerber X2 (PCB manufacturing)
- **Size**: 21 lines
- **Content**: 20 copper coordinates
- **Use**: Send to PCB fabrication service

### build/sim.py
- **Format**: Blender Python script
- **Size**: 42 lines
- **Content**: FR4 substrate + 20 copper cubes
- **Use**: `blender --python build/sim.py`

### build/board.obj
- **Format**: Wavefront OBJ (universal 3D)
- **Size**: 1,689 lines
- **Content**: 168 vertices, 252 triangles
- **Use**: Open in any 3D viewer

---

## Visual Verification

### output/board.obj.png
Screenshot from online 3D viewer (https://3dviewer.net/)

**Shows**:
- FR4 substrate (gray base)
- Copper traces (L-shaped)
- Mesh statistics (168 vertices, 252 triangles)

### output/sim.py.png
Screenshot from Blender render

**Shows**:
- 20 copper cubes on substrate
- Scene hierarchy
- Viewport statistics

---

## Test Verification

See [TEST-VERIFICATION.md](TEST-VERIFICATION.md) for complete test report including:

- Compilation process
- Output file analysis
- Visual verification
- Physics calculations
- Geometry verification
- Test results summary

---

## Compiler Architecture

### hw.py Structure

```python
# Phase 1-2: Lexer & Parser (lines 8-60)
- Tokenize .hw source
- Build Abstract Syntax Tree

# Phase 3-4: Grid Engine & Physics (lines 62-100)
- Populate 3D tensor grid
- Calculate trace resistance

# Phase 5-6: Export Engine (lines 102-180)
- Generate Gerber files
- Generate Blender scripts
- Generate OBJ models
```

### Dependencies

```bash
pip install numpy pyyaml
```

---

## Materials Database

**File**: `standard-materials.yaml`

**Contains**:
- 3 conductors (Copper, Aluminum, Gold)
- 3 insulators (FR4, Air, Silicon Dioxide)
- 1 semiconductor (Silicon)
- 1 resistive material (Carbon Film)

**Properties**:
- Electrical (resistivity, dielectric strength)
- Thermal (conductivity, melting point)
- Physical (density, color)
- Mechanical (band gap, mobility)

**Data sources**:
- Materials Project API
- Engineering handbooks
- Manufacturer datasheets

---

## Modifying the Test

### Change Board Size

```hw
define Space "BiggerBoard":
    dimensions: 50mm by 50mm by 2mm
    grid: 50 by 50 by 2
```

### Change Trace Path

```hw
route MainSwitch.Collector to Power.Out:
    path:
        - [1, 5, 5]
        - [1, 15, 5]   # Straight line
```

### Add More Routes

```hw
route MainSwitch.Emitter to Ground.In:
    path:
        - [1, 5, 4]
        - [1, 10, 4]
```

---

## Troubleshooting

### Error: "No module named 'numpy'"
```bash
pip install numpy
```

### Error: "FileNotFoundError: standard-materials.yaml"
Make sure you're in the `live-test` directory:
```bash
cd live-test
python hw.py generate test_board.hw
```

### No output files
Check for error messages in console. Verify syntax in .hw file.

---

## Performance

**Test board compilation**:
- Lexing: < 1ms
- Parsing: < 1ms
- Grid compilation: < 1ms
- Physics calculation: < 1ms
- Export: < 5ms
- **Total: < 10ms**

---

## Next Steps

1. Read [../Docs/v0.1/GETTING-STARTED.md](../Docs/v0.1/GETTING-STARTED.md)
2. Try modifying test_board.hw
3. Experiment with different trace patterns
4. View outputs in different tools
5. Check [../ROADMAP.md](../ROADMAP.md) for future features

---

**Hardware Script v0.1** - Proof that hardware can be compiled from text.
