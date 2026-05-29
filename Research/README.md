# Hardware Script Research Database

**Purpose**: Foundational physics engine and materials database for the Hardware Script Synthesizer

**Status**: Research Phase - Building MVP data layer

---

## Overview

This directory contains the research and data definitions for the core physics engine that powers Hardware Script. Before we can have logic gates, packages, or AI generation, we need a mathematically bulletproof foundation that understands electrons, heat, and physical materials.

## The System Under the System

Hardware Script is built on a five-level ontology, from the barest scratch (atomic physics) up to high-level syntax:

### Level 0: The Spatial Reality (Tensor Grid)
- **What**: The `[Z, X, Y]` voxel grid system
- **Purpose**: Provides geometric boundaries and O(1) collision detection
- **Knowledge**: Only geometry and spatial relationships
- **Status**: ✅ Defined in ARCHITECTURE.md

### Level 1: The Material Reality (The Barest Scratch)
- **What**: Physical constants for conductors, insulators, and semiconductors
- **Purpose**: Atomic physics formulas that govern electron flow and heat
- **Knowledge**: Resistivity, thermal conductivity, dielectric strength, bandgap
- **Status**: 🔄 In Progress (this research)

### Level 2: The Analog Reality (Nodal Equations)
- **What**: Analog primitives (Resistors, Capacitors, Transistors)
- **Purpose**: SPICE-like nodal equations using Kirchhoff's Laws
- **Knowledge**: Ohm's Law, Joule heating, voltage/current relationships
- **Status**: 📋 Planned

### Level 3: The Bare-Metal Switch (Transistor Logic)
- **What**: Transistors as analog valves with threshold voltages
- **Purpose**: Bridge between analog physics and digital logic
- **Knowledge**: Saturation voltages, switching characteristics
- **Status**: 📋 Planned

### Level 4: Standard Logic Macros (Digital Illusion)
- **What**: Logic gates built from transistor arrangements
- **Purpose**: Create "digital" behavior from analog components
- **Knowledge**: NOT, AND, OR, NAND gates as transistor circuits
- **Status**: 📋 Planned

### Level 5: Syntactic Sugar (High-Level Rules)
- **What**: The `rule` syntax and declarative logic
- **Purpose**: User-friendly hardware description language
- **Knowledge**: Compiles down through all layers to materials
- **Status**: ✅ Defined in LANGUAGE-SPEC.md

---

## Why This Matters

**Digital logic is an illusion.** Everything at the bottom is analog physics:
- A "1" is just 5 Volts
- A "0" is just 0 Volts  
- A logic gate is just carefully balanced analog materials

If we don't define the "barest scratch" perfectly, Engine A (The Linter) cannot mathematically prove that a circuit won't short out or catch fire.

---

## Research Goals

### Level 1 MVP: 8-10 Core Materials

We don't need the entire periodic table. The hardware industry is standardized around a tiny set of materials.

**Group A: Conductors** (3 materials)
- Copper - Universal PCB trace material
- Gold - Contact pads and wire bonding
- Aluminum - Chip-level routing and heat sinks

**Group B: Insulators/Substrates** (3 materials)
- FR4 Fiberglass - Standard PCB board
- Air - Ambient environment (spark gap calculations)
- Silicon Dioxide - Microchip insulator

**Group C: Semiconductors/Resistives** (2 materials)
- Silicon (Doped) - Transistors and diodes
- Carbon Film - Standard resistors

### Required Properties Per Material

**Conductors**:
- `resistivity` (Ω·m) - Electron flow resistance
- `thermal_conductivity` (W/(m·K)) - Heat dissipation rate
- `melting_point` (°C) - Absolute failure temperature
- `max_current_density` (A/mm²) - Fusing threshold

**Insulators**:
- `dielectric_strength` (kV/mm) - Voltage breakdown threshold
- `thermal_resistance` (K/W) - Heat trapping
- `relative_permittivity` (εᵣ) - Capacitance/interference calculations

**Semiconductors**:
- `bandgap` (eV) - Energy to free an electron
- `carrier_mobility` (cm²/V·s) - Electron velocity

---

## How Level 1 Feeds Level 2

Once we have the materials database, Level 2 becomes pure mathematics.

**Example: Trace Resistance Calculation**

```
Resistance = ρ × (Length / Area)

Where:
- ρ (resistivity) comes from Level 1 (Copper database)
- Length comes from Level 0 (voxel count in route)
- Area comes from Level 0 (trace width × thickness)
```

This is how Engine A mathematically proves hardware works before generating output files.

---

## Files in This Directory

- `README.md` - This file (overview and roadmap)
- `level-1-materials.yaml` - Materials database with physical constants
- `level-2-analog-primitives.md` - Analog component equations (planned)
- `level-3-transistor-models.md` - Transistor switching models (planned)
- `level-4-logic-macros.md` - Logic gate implementations (planned)
- `level-5-rule-compilation.md` - High-level syntax compilation (planned)

---

## Research Methodology

1. **Primary Sources**: Manufacturer datasheets, IEEE standards, physics textbooks
2. **Validation**: Cross-reference multiple sources for each constant
3. **Units**: SI units with explicit conversions documented
4. **Precision**: Engineering precision (3-4 significant figures)
5. **Temperature**: Standard conditions (25°C unless specified)

---

## Next Steps

1. ✅ Create research directory structure
2. 🔄 Research and document Level 1 materials (8-10 materials)
3. 📋 Define Level 2 analog equations (Ohm's Law, Joule heating)
4. 📋 Define Level 3 transistor models (BJT, MOSFET)
5. 📋 Define Level 4 logic gate implementations
6. 📋 Validate Level 5 rule syntax maps to lower levels
7. 📋 Build MVP Synthesizer in Python
8. 📋 Synthesize first .hw file!

---

**Status**: Research Phase  
**Last Updated**: March 2026  
**Part of**: Hardware Script (.hw) Core Engine Development
