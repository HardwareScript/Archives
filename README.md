# Hardware Script — Archives

**⚠️ HISTORICAL REFERENCE — NOT PART OF THE ACTIVE CODEBASE**

This directory contains archived materials from the early development of Hardware Script — including the original Python prototype compiler, Rust migration experiments, research databases, dev notes, and GitHub organization strategy planning.

These files are preserved for **historical reference, audit trail, and research** purposes. They are **not** part of the current compiler, HSM desktop application, or active toolchain. The active source code lives in:

| Component | Location |
|-----------|----------|
| **HWC Compiler** | [`hwc/`](../hwc/) |
| **HSM Desktop** | [`hsm/`](../hsm/) |
| **Implementation Roadmaps** | [`ROADMAP/`](../ROADMAP/) |
| **Language Specs & Docs** | [`Docs/`](../Docs/) |

---

## Directory Structure

```
Archives/
├── README.md                  ← This file
│
├── build/                     ┐ Compiled outputs from the original
│   ├── board.gtl              │ Python prototype compiler
│   ├── board.obj              │ (Gerber, OBJ, Blender script)
│   └── sim.py                 ┘
│
├── dev-notes/
│   ├── hope.txt               Philosophical essay — why text-based
│   │                          voxel systems matter for academic physics
│   ├── thoughts.txt           Raw development thoughts and brainstorming
│   └── llm-notes/             LLM-assisted development logs
│
├── engine-test/
│   ├── engine_a_phase1.py     Phase 1: Grid engine prototype
│   ├── engine_a_phase2.py     Phase 2: Routing engine prototype
│   ├── engine_a_phase3.py     Phase 3: Physics validation prototype
│   ├── engine_a_phase4.py     Phase 4: Export engine prototype
│   ├── engine_a_phase5.py     Phase 5: Full pipeline integration
│   ├── engine_export_phase6.py Phase 6: Export refinement
│   ├── standard-materials.yaml  Materials DB used by engine tests
│   └── build/                 Test build outputs
│
├── GITHUB-ORG-STRATEGY/
│   ├── README.md              Strategic planning for migrating to
│   │                          the `hwsl-lang` GitHub organization
│   ├── ORGANIZATION-STRUCTURE.md  Repository breakdown
│   ├── MIGRATION-PLAN.md          Step-by-step migration guide
│   ├── PACKAGE-DISCOVERY-SEARCH.md  Package registry search design
│   └── PACKAGE-MANAGER-ARCHITECTURE.md  Git-based package manager
│
├── live-test/
│   ├── hw.py                  Original Python MVP compiler (~180 LOC)
│   ├── README.md              Test documentation
│   ├── test_board.hw          Example .hw input file
│   ├── standard-materials.yaml  Materials database
│   ├── TEST-VERIFICATION.md   Test verification report
│   ├── build/                 Generated build outputs
│   └── output/                Screenshots and output artifacts
│
├── problems/
│   ├── 1.txt                  Problem analysis / debugging notes
│   ├── 2.txt
│   ├── 3.txt
│   └── 4.txt
│
├── Research/
│   ├── README.md              Research overview — 5-Level Ontology
│   ├── level-1-materials.yaml     Level 1: Material constants database
│   ├── level-2-analog-primitives.md  Level 2: Analog equations (Ohm's Law, Joule heating)
│   ├── level-3-transistor-models.md  Level 3: BJT/MOSFET models
│   ├── level-4-logic-macros.md      Level 4: Logic gate implementations
│   ├── level-5-rule-compilation.md  Level 5: High-level syntax compilation
│   ├── enhanced_materials_database.py   Materials data fetcher
│   ├── enhanced_materials.json         Fetched materials (JSON)
│   ├── enhanced_materials.yaml         Fetched materials (YAML)
│   ├── fetch_detailed_properties.py    Detailed property fetcher
│   ├── fetch_materials_data.py         Materials Project API fetcher
│   ├── simple_materials_data.json      Simplified materials DB (JSON)
│   ├── simple_materials_lookup.py      Materials lookup utility
│   ├── SYNTHESIS-ROADMAP.md            Synthesis engine roadmap
│   └── results/                        Research output data
│
└── src/                        ┐ Early Rust compiler prototype
    ├── main.rs                │ (precursor to hwc/ — not the
    ├── phase1.rs              │  active compiler)
    ├── phase2.rs              │
    ├── phase3.rs              │
    ├── phase4.rs              │
    ├── phase5.rs              │
    ├── sparse_engine.rs       │
    ├── synthesizer.rs         │
    ├── hardware.pest          │ PEST grammar definition
    ├── standard-materials.yaml │ Materials DB for Rust prototype
    ├── test_board.hw          │ Test input file
    └── doc/                    │ Auto-generated documentation
```

---

## What's Here and Why

### `live-test/` — The Original Python MVP
The very first working Hardware Script compiler. A ~180-line Python script that proved the core thesis: human-readable text → deterministic manufacturing files. It compiles `.hw` files to Gerber, Blender Python scripts, and OBJ 3D models using a discrete 3D tensor grid with Bresenham line interpolation.

**Historical significance**: This was the proof-of-concept that validated the entire approach. All subsequent Rust compilers and the HSM desktop app trace their lineage back to this file.

### `engine-test/` — Engine Prototyping in Python
Six phases of Python-based engine prototyping that explored the grid engine, routing, physics validation, and export pipeline before the Rust migration. These represent the iterative design process that led to the current compiler architecture.

### `src/` — Early Rust Compiler Prototype
The first Rust implementation of the Hardware Script compiler (precursor to `hwc/`). Includes:
- `main.rs` — CLI entry point with clap argument parsing
- `phase1.rs` through `phase5.rs` — Incremental compiler phases
- `sparse_engine.rs` — Sparse spatial data structure
- `synthesizer.rs` — Multi-format export engine (Gerber, OBJ, STEP)
- `hardware.pest` — PEST parser grammar

**Note**: This is **not** the active compiler. The active Rust compiler is in [`hwc/`](../hwc/).

### `Research/` — 5-Level Ontology Foundation
The research database that defines the theoretical foundation of Hardware Script's physics engine:
- **Level 0**: Spatial Reality (Tensor Grid)
- **Level 1**: Material Reality (Atomic physics constants)
- **Level 2**: Analog Reality (Nodal equations, SPICE)
- **Level 3**: Bare-Metal Switch (Transistor models)
- **Level 4**: Standard Logic Macros (Logic gates)
- **Level 5**: Syntactic Sugar (High-level `rule` syntax)

Contains materials data fetched from the Materials Project API, enhanced with manufacturer datasheet values. Active materials research continues in [`hwc/data/`](../hwc/data/) and [`hwc/stdlib/`](../hwc/stdlib/).

### `GITHUB-ORG-STRATEGY/` — Organization Migration Planning
Contains the plan for migrating Hardware Script from a personal experimental repository to the `hwsl-lang` GitHub organization. These documents are strategic planning only and should **not** be copied to any organization repository.

### `dev-notes/` — Development Philosophy & Essays
Contains raw development thoughts and philosophical essays. Notably `hope.txt`, which explores why a text-based voxel system has profound implications for theoretical physics — from Chaos Theory and Landauer's Principle to metamaterials and percolation theory.

### `problems/` — Debugging & Analysis Notes
Raw problem analysis notes captured during development. Preserved for audit trail.

### `build/` — Original Generated Outputs
The Gerber, OBJ, and Blender files generated by the original Python compiler — the very first tangible outputs of Hardware Script.

---

## How to Use These Archives

1. **Researching design history** → Browse `engine-test/` and `src/` to trace the evolution from Python → Rust prototype → production compiler.

2. **Understanding the physics foundation** → Read `Research/README.md` and the 5-level ontology documents (level-1 through level-5).

3. **Seeing the original proof-of-concept** → Run `live-test/hw.py` with `test_board.hw` to compile the very first Hardware Script design.

4. **Reading development philosophy** → Check `dev-notes/hope.txt` for the broader vision of what text-based hardware description enables.

5. **Planning GitHub organization structure** → See `GITHUB-ORG-STRATEGY/` for the migration plan (do not copy to org repos).

6. **Tracing compiler debug history** → See `problems/` for issue analysis notes.

---

## Relationship to Active Code

| Archive Component | Evolved Into |
|-------------------|--------------|
| `live-test/hw.py` (Python MVP) | `hwc/` (Rust compiler) |
| `src/` (Rust prototype) | `hwc/` (production compiler) |
| `Research/` (materials DB) | `hwc/data/`, `hwc/stdlib/` |
| `engine-test/` (routing prototypes) | `hwc/crates/` (routing engine) |
| N/A (no HSM existed yet) | `hsm/` (Hardware Script Monitor) |