# Hardware Script Level 2: Analog Reality (Nodal Equations)

**Version**: 0.1 (Research Phase)  
**Purpose**: Mathematical equations for analog primitives using Level 1 materials  
**Status**: 📋 Planned

---

## Overview

Level 2 is where we move from static material properties to dynamic electrical behavior. This layer implements the fundamental laws of electrical engineering that govern how electrons flow through circuits.

**Key Principle**: We don't start with logic gates. We start with analog primitives that obey Kirchhoff's Laws and nodal equations.

---

## Core Electrical Laws

### Ohm's Law (Voltage-Current-Resistance)

```
V = I × R

Where:
- V = Voltage (Volts)
- I = Current (Amperes)
- R = Resistance (Ohms)
```

**Application**: Calculate voltage drop across any conductor or resistor.

### Joule's Law (Power Dissipation)

```
P = I² × R = V² / R = V × I

Where:
- P = Power (Watts)
- I = Current (Amperes)
- R = Resistance (Ohms)
- V = Voltage (Volts)
```

**Application**: Calculate heat generation in components and traces.

### Kirchhoff's Current Law (KCL)

```
Σ I_in = Σ I_out

The sum of currents entering a node equals the sum leaving.
```

**Application**: Validate current conservation at connection points.

### Kirchhoff's Voltage Law (KVL)

```
Σ V_loop = 0

The sum of voltages around any closed loop equals zero.
```

**Application**: Validate voltage drops in routing paths.

---

## Analog Primitive: Resistor

### Definition

A resistor is a passive component that opposes current flow, converting electrical energy to heat.

### .hw Component Definition

```hw
define Component "Resistor_10k":
    material: CarbonFilm
    resistance: 10000 Ohms
    max_power: 0.25 Watts
    tolerance: 5%
    
    pins:
        In at [0, 0]
        Out at [2, 0]
```

### Mathematical Model

**Voltage Drop**:
```
V_drop = I × R
```

**Power Dissipation**:
```
P = I² × R
```

**Thermal Check**:
```
if P > max_power:
    raise ThermalError("Resistor exceeds power rating")
```

### Synthesizer Validation

When Engine A encounters a resistor:

1. Calculate current through the resistor using KCL
2. Calculate voltage drop using Ohm's Law
3. Calculate power dissipation using Joule's Law
4. Verify P < max_power rating
5. Calculate temperature rise using thermal resistance

---

## Analog Primitive: Capacitor

### Definition

A capacitor stores electrical energy in an electric field between two conductive plates separated by an insulator (dielectric).

### .hw Component Definition

```hw
define Component "Capacitor_100nF":
    material: Ceramic
    capacitance: 100e-9 Farads
    max_voltage: 50 Volts
    
    pins:
        Positive at [0, 0]
        Negative at [2, 0]
```

### Mathematical Model

**Capacitance Formula**:
```
C = ε₀ × εᵣ × A / d

Where:
- C = Capacitance (Farads)
- ε₀ = Permittivity of free space (8.854e-12 F/m)
- εᵣ = Relative permittivity (from Level 1 materials)
- A = Plate area (m²)
- d = Distance between plates (m)
```

**Charge Storage**:
```
Q = C × V

Where:
- Q = Charge (Coulombs)
- C = Capacitance (Farads)
- V = Voltage (Volts)
```

**Current-Voltage Relationship**:
```
I = C × (dV/dt)

Current is proportional to rate of voltage change.
```

### Synthesizer Validation

1. Verify V < max_voltage rating
2. Calculate stored energy: E = ½CV²
3. Check for voltage spikes that exceed rating

---

## Analog Primitive: Copper Trace (Conductor)

### Definition

A copper trace is a conductive path on a PCB that carries current between components.

### Mathematical Model

**Resistance Calculation**:
```
R = ρ × L / A

Where:
- R = Resistance (Ohms)
- ρ = Resistivity from Level 1 (Copper: 1.68e-8 Ω·m)
- L = Length of trace (meters)
- A = Cross-sectional area (m²)
```

**Cross-Sectional Area**:
```
A = width × thickness

Where:
- width = trace width (from grid voxels)
- thickness = copper thickness (typically 35μm for 1oz copper)
```

**Voltage Drop**:
```
V_drop = I × R = I × (ρ × L / A)
```

**Power Dissipation (Heat)**:
```
P = I² × R
```

**Temperature Rise**:
```
ΔT = P × θ

Where:
- ΔT = Temperature rise (°C)
- P = Power dissipation (Watts)
- θ = Thermal resistance (°C/W)
```

**Current Capacity (IPC-2221A)**:
```
I = k × ΔT^0.44 × A^0.725

Where:
- I = Maximum current (Amperes)
- k = 0.048 for external layers, 0.024 for internal layers
- ΔT = Allowable temperature rise (typically 10°C)
- A = Cross-sectional area (mm²)
```

### Synthesizer Validation

When Engine A encounters a routed trace:

1. Calculate trace length from waypoint coordinates (Level 0 grid)
2. Calculate cross-sectional area from trace width and copper thickness
3. Calculate resistance using ρ from Level 1 (Copper)
4. Calculate voltage drop for expected current
5. Calculate power dissipation
6. Calculate temperature rise
7. Verify temperature < melting point (1085°C for copper)
8. Verify current < max_current_density (35 A/mm² for copper)

**Example Error**:
```
❌ Error at Line 23: Trace Overheating
  Route: PowerSource.out → Motor.in
  Trace: [1, 5, 5] → [1, 50, 5]
  Length: 45mm
  Width: 0.5mm
  Thickness: 0.035mm (1oz copper)
  Current: 5A
  
  Calculated:
    Resistance: 0.043 Ohms
    Voltage Drop: 0.215V
    Power Dissipation: 1.075W
    Temperature Rise: 61°C
  
  ⚠️  Temperature rise exceeds safe limit (10°C)
  Suggestion: Increase trace width to 2mm or use thicker copper (2oz)
```

---

## Analog Primitive: Via (Vertical Interconnect)

### Definition

A via is a conductive hole that connects traces on different layers of a PCB.

### Mathematical Model

**Resistance Calculation**:
```
R = ρ × L / A

Where:
- ρ = Resistivity (Copper: 1.68e-8 Ω·m)
- L = Via length (board thickness)
- A = π × r² (circular cross-section)
```

**Typical Values**:
- Via diameter: 0.3mm to 0.8mm
- Via length: 1.6mm (standard PCB thickness)
- Plating thickness: 25μm

**Example Calculation**:
```
Via diameter: 0.4mm → radius: 0.2mm
Via length: 1.6mm
Plating thickness: 25μm

Effective radius: 0.2mm - 0.025mm = 0.175mm
Area: π × (0.175mm)² = 0.096 mm² = 9.6e-8 m²

R = 1.68e-8 × 0.0016 / 9.6e-8 = 0.00028 Ohms
```

### Synthesizer Validation

1. Calculate via resistance based on diameter and board thickness
2. Add via resistance to total path resistance
3. Verify current capacity (typically 1-3A per via)

---

## How Level 2 Feeds Level 3

Once we have these analog primitives mathematically defined, Level 3 (Transistors) becomes possible. A transistor is just a special arrangement of semiconductor materials (from Level 1) that creates a voltage-controlled switch.

The key insight: **Everything is analog**. Even "digital" logic is just analog voltages that we interpret as 1s and 0s.

---

## Next Steps

1. ✅ Define core electrical laws (Ohm, Joule, Kirchhoff)
2. ✅ Define resistor model
3. ✅ Define capacitor model
4. ✅ Define copper trace model with thermal calculations
5. ✅ Define via model
6. 📋 Define inductor model (for future RF applications)
7. 📋 Define diode model (P-N junction, forward voltage)
8. 📋 Implement SPICE-like nodal analysis algorithm
9. 📋 Build Python validation engine for Engine A

---

**Status**: Research Phase  
**Last Updated**: March 2026  
**Part of**: Hardware Script (.hw) Core Engine Development
