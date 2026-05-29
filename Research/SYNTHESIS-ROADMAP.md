# Hardware Script Synthesizer: Complete Roadmap

**Version**: 0.1 (Research Phase)  
**Purpose**: Master plan for building the Hardware Script compiler/synthesizer  
**Status**: Foundation Research Complete

---

## Executive Summary

We have completed the foundational research for the Hardware Script physics engine. The system is built on a five-level ontology that starts from atomic physics and builds up to high-level declarative syntax.

**Core Innovation**: By building from the "barest scratch" (electrons and materials) upwards, the Synthesizer can mathematically prove hardware correctness before manufacturing.

---

## The Five-Level Architecture

### Level 0: Spatial Reality ✅ COMPLETE
- **Location**: `Docs/ARCHITECTURE.md`
- **What**: Discrete 3D Tensor Grid `[Z, X, Y]`
- **Purpose**: Geometric boundaries and O(1) collision detection
- **Status**: Fully specified and documented

### Level 1: Material Reality ✅ COMPLETE
- **Location**: `Research/level-1-materials.yaml`
- **What**: Physical constants for 8 core materials
- **Materials Defined**:
  - Conductors: Copper, Gold, Aluminum
  - Insulators: FR4, Air, Silicon Dioxide
  - Semiconductors: Silicon (Doped)
  - Resistives: Carbon Film
- **Status**: Database complete with all required properties

### Level 2: Analog Reality ✅ COMPLETE
- **Location**: `Research/level-2-analog-primitives.md`
- **What**: Fundamental electrical laws and analog components
- **Defined**:
  - Ohm's Law, Joule's Law, Kirchhoff's Laws
  - Resistor model
  - Capacitor model
  - Copper trace model (with thermal calculations)
  - Via model
- **Status**: Mathematical models complete

### Level 3: Transistor Logic ✅ COMPLETE
- **Location**: `Research/level-3-transistor-models.md`
- **What**: Transistors as analog valves
- **Defined**:
  - BJT (NPN) transistor model
  - MOSFET (N-channel) model
  - Operating regions (cutoff, active, saturation)
  - Threshold voltages and switching characteristics
- **Status**: Models complete

### Level 4: Logic Macros ✅ COMPLETE
- **Location**: `Research/level-4-logic-macros.md`
- **What**: Logic gates built from transistor arrangements
- **Defined**:
  - NOT, NAND, NOR gates (primitive)
  - AND, OR, XOR gates (derived)
  - Circuit topologies and truth tables
- **Status**: Gate implementations complete

### Level 5: Rule Compilation ✅ COMPLETE
- **Location**: `Research/level-5-rule-compilation.md`
- **What**: High-level rule syntax compilation
- **Defined**:
  - Rule syntax structure
  - Compilation process (rules → circuits)
  - Operator mappings
  - State assignment
- **Status**: Compilation strategy complete

---

## Implementation Roadmap

### Phase 1: Core Data Layer ✅ COMPLETE
- [x] Research and document Level 1 materials
- [x] Define Level 2 analog equations
- [x] Define Level 3 transistor models
- [x] Define Level 4 logic gate implementations
- [x] Define Level 5 rule compilation strategy

### Phase 2: Parser and AST (Next)
**Goal**: Build the .hw file parser

**Tasks**:
1. Implement lexer (tokenization)
2. Implement parser (syntax tree generation)
3. Define AST (Abstract Syntax Tree) structure
4. Implement semantic analysis
5. Build error reporting system

**Deliverables**:
- Python module: `hw_parser.py`
- AST classes: `Space`, `Component`, `Route`, `Rule`
- Test suite: `test_parser.py`

### Phase 3: Grid Engine (Level 0)
**Goal**: Implement the 3D tensor grid system

**Tasks**:
1. Implement `Space` class with voxel calculations
2. Implement `CellState` enum (EMPTY, COPPER, PAD, HOLE)
3. Implement O(1) collision detection
4. Implement waypoint interpolation (Bresenham's algorithm)
5. Implement via generation logic

**Deliverables**:
- Python module: `grid_engine.py`
- Test suite: `test_grid.py`

### Phase 4: Materials Engine (Level 1)
**Goal**: Load and query material properties

**Tasks**:
1. Implement YAML loader for materials database
2. Implement `Material` class hierarchy
3. Implement property lookup functions
4. Add temperature-dependent calculations

**Deliverables**:
- Python module: `materials.py`
- Test suite: `test_materials.py`

### Phase 5: Analog Engine (Level 2)
**Goal**: Implement electrical calculations

**Tasks**:
1. Implement Ohm's Law calculator
2. Implement Joule heating calculator
3. Implement trace resistance calculator
4. Implement Kirchhoff's Laws solver (nodal analysis)
5. Implement thermal analysis

**Deliverables**:
- Python module: `analog_engine.py`
- Test suite: `test_analog.py`

### Phase 6: Transistor Engine (Level 3)
**Goal**: Implement transistor models

**Tasks**:
1. Implement BJT model (cutoff, active, saturation)
2. Implement MOSFET model
3. Implement threshold voltage checks
4. Implement power dissipation calculations

**Deliverables**:
- Python module: `transistor_engine.py`
- Test suite: `test_transistors.py`

### Phase 7: Logic Engine (Level 4)
**Goal**: Implement logic gate library

**Tasks**:
1. Implement standard gate definitions
2. Implement gate instantiation
3. Implement truth table validation
4. Build standard.logic package

**Deliverables**:
- Python module: `logic_engine.py`
- Package: `standard/logic/*.hw`
- Test suite: `test_logic.py`

### Phase 8: Rule Compiler (Level 5)
**Goal**: Compile rules to circuits

**Tasks**:
1. Implement rule parser
2. Implement circuit generator
3. Implement operator mapping
4. Implement state assignment

**Deliverables**:
- Python module: `rule_compiler.py`
- Test suite: `test_rules.py`

### Phase 9: Engine A (Validation)
**Goal**: Complete the verification engine

**Tasks**:
1. Integrate all engines (Levels 0-5)
2. Implement end-to-end validation
3. Implement error reporting
4. Implement suggestion system

**Deliverables**:
- Python module: `engine_a.py`
- CLI command: `hw verify`
- Test suite: `test_engine_a.py`

### Phase 10: Engine B (Simulation Export)
**Goal**: Generate Blender Python scripts

**Tasks**:
1. Implement Blender API code generation
2. Implement mesh placement
3. Implement copper trace visualization
4. Implement component rendering

**Deliverables**:
- Python module: `engine_b_blender.py`
- CLI command: `hw generate --target simulation`
- Test suite: `test_engine_b.py`

### Phase 11: Engine C (Manufacturing Export)
**Goal**: Generate Gerber and GDSII files

**Tasks**:
1. Implement Gerber X2 generator
2. Implement Excellon drill file generator
3. Implement BOM generator
4. Implement GDSII generator (for silicon)

**Deliverables**:
- Python module: `engine_c_gerber.py`
- Python module: `engine_c_gdsii.py`
- CLI command: `hw generate --target manufacturing`
- Test suite: `test_engine_c.py`

### Phase 12: CLI and Integration
**Goal**: Complete the user-facing tools

**Tasks**:
1. Implement `hw verify` command
2. Implement `hw generate` command
3. Implement `hw init` command
4. Implement configuration loader
5. Build package manager foundation

**Deliverables**:
- Python module: `cli.py`
- Executable: `hw` (entry point)
- Documentation: `CLI-REFERENCE.md`

---

## MVP Definition

**Minimum Viable Product**: A working synthesizer that can:

1. Parse a simple .hw file
2. Validate electrical rules (Engine A)
3. Generate a Blender simulation (Engine B)
4. Generate Gerber files for PCB manufacturing (Engine C)

**MVP Example**: The "Automated Sprinkler" from the documentation
- Battery, LightSensor, Transistor
- Simple routing with waypoints
- One rule: `if Eye.light_level < 50%: Valve state is ON`

**Success Criteria**:
- `hw verify sprinkler.hw` → ✅ No errors
- `hw generate --target simulation` → Blender script created
- `hw generate --target manufacturing` → Gerber files created
- Files can be sent to JLCPCB and manufactured

---

## Technology Stack

### Core Language
- **Python 3.10+**: Main implementation language
- **NumPy**: For 3D tensor grid operations
- **PyYAML**: For configuration and materials database
- **Click**: For CLI interface

### Testing
- **pytest**: Unit and integration testing
- **hypothesis**: Property-based testing

### Documentation
- **Sphinx**: API documentation generation
- **MkDocs**: User documentation site

### Future Considerations
- **Rust**: For performance-critical grid operations
- **WASM**: For browser-based editor
- **TypeScript**: For VS Code extension

---

## Success Metrics

### Phase 1 (Research) ✅ COMPLETE
- [x] All 5 levels documented
- [x] Materials database complete
- [x] Mathematical models defined

### Phase 2-12 (Implementation)
- [ ] Parser handles all syntax
- [ ] Grid engine passes all collision tests
- [ ] Analog engine matches SPICE results (±5%)
- [ ] Transistor models match datasheet specs
- [ ] Logic gates produce correct truth tables
- [ ] Rules compile to working circuits
- [ ] Engine A catches all electrical violations
- [ ] Engine B generates valid Blender scripts
- [ ] Engine C generates manufacturable Gerber files
- [ ] MVP example works end-to-end

---

## Next Immediate Steps

1. **Create Python project structure**
   ```
   hardware-script/
   ├── hw/
   │   ├── __init__.py
   │   ├── parser.py
   │   ├── grid_engine.py
   │   ├── materials.py
   │   ├── analog_engine.py
   │   ├── transistor_engine.py
   │   ├── logic_engine.py
   │   ├── rule_compiler.py
   │   ├── engine_a.py
   │   ├── engine_b_blender.py
   │   ├── engine_c_gerber.py
   │   └── cli.py
   ├── tests/
   ├── standard/
   │   ├── materials/
   │   ├── logic/
   │   └── components/
   ├── examples/
   │   └── sprinkler.hw
   └── setup.py
   ```

2. **Begin Phase 2: Parser Implementation**
   - Start with lexer for tokenization
   - Build AST classes
   - Implement basic syntax parsing

3. **Create First Test Case**
   - Write `examples/sprinkler.hw` (MVP example)
   - Create test that parses it successfully
   - Use TDD (Test-Driven Development) approach

---

**Status**: Foundation Complete, Ready for Implementation  
**Last Updated**: March 2026  
**Next Milestone**: Parser Implementation (Phase 2)
