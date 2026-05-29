# Hardware Script Level 3: The Bare-Metal Switch (Transistor Logic)

**Version**: 0.1 (Research Phase)  
**Purpose**: Transistor models as analog valves bridging to digital logic  
**Status**: 📋 Planned

---

## Overview

Level 3 is where we bridge from pure analog physics to the illusion of digital logic. A transistor is not a logic gate—it's an **analog valve** that uses a small control voltage to regulate a larger current flow.

**Key Principle**: Digital logic is an illusion. A "1" is just 5V, a "0" is just 0V. Transistors create this illusion through carefully controlled analog thresholds.

---

## Transistor Types

### BJT (Bipolar Junction Transistor)

**Structure**: Three layers of doped silicon (NPN or PNP)
- **Collector**: Current input
- **Base**: Control terminal (small current controls large current)
- **Emitter**: Current output

**Operating Principle**: Current-controlled current source
- Small base current (I_B) controls large collector current (I_C)
- I_C = β × I_B (where β is current gain, typically 100-300)

### MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)

**Structure**: Four terminals
- **Drain**: Current input
- **Gate**: Control terminal (voltage-controlled, no current flow)
- **Source**: Current output
- **Body/Substrate**: Usually connected to source

**Operating Principle**: Voltage-controlled current source
- Gate voltage (V_GS) controls drain current (I_D)
- Essentially zero gate current (high impedance)

---

## BJT NPN Transistor Model

### .hw Component Definition

```hw
define Component "Transistor_NPN_2N3904":
    material: Silicon
    type: BJT_NPN
    
    # Threshold Voltages
    vbe_saturation: 0.7V    # Base-Emitter voltage to turn ON
    vce_saturation: 0.2V    # Collector-Emitter voltage when saturated
    
    # Current Specifications
    max_collector_current: 200mA
    current_gain_beta: 150  # Typical β (hFE)
    
    # Power Specifications
    max_power: 625mW
    
    pins:
        Collector at [0, 1]
        Base at [1, 0]
        Emitter at [2, 1]
```

### Mathematical Model

**Operating Regions**:

1. **Cutoff** (OFF state)
   - V_BE < 0.7V
   - I_C ≈ 0
   - Transistor acts as open switch

2. **Active** (Amplification)
   - V_BE ≥ 0.7V
   - I_C = β × I_B
   - Linear amplification region

3. **Saturation** (ON state)
   - V_BE ≥ 0.7V
   - V_CE ≈ 0.2V
   - Transistor acts as closed switch
   - I_C limited by external circuit, not β

**Equations**:

```
Base Current:
I_B = (V_in - V_BE) / R_base

Collector Current (Active Region):
I_C = β × I_B

Collector Current (Saturation):
I_C = (V_CC - V_CE_sat) / R_load

Power Dissipation:
P = V_CE × I_C + V_BE × I_B
```

### Synthesizer Validation

When Engine A encounters a BJT transistor:

1. **Check Base Voltage**: Is V_BE ≥ 0.7V?
   - If NO → Transistor is OFF (cutoff)
   - If YES → Continue to step 2

2. **Calculate Base Current**: I_B = (V_in - 0.7V) / R_base

3. **Calculate Collector Current**: I_C = β × I_B

4. **Check Saturation**: Is I_C × R_load > (V_CC - 0.2V)?
   - If YES → Transistor is saturated, recalculate I_C
   - If NO → Transistor is in active region

5. **Verify Limits**:
   - I_C < max_collector_current (200mA)
   - P < max_power (625mW)

**Example Error**:
```
❌ Error at Line 45: Transistor Insufficient Drive
  Component: Switch (Transistor_NPN_2N3904)
  Base Voltage: 0.4V
  Required: ≥ 0.7V
  
  Transistor cannot turn ON with 0.4V at base.
  Suggestion: Increase input voltage or reduce base resistor.
```

---

## MOSFET N-Channel Model

### .hw Component Definition

```hw
define Component "MOSFET_N_2N7000":
    material: Silicon
    type: MOSFET_N
    
    # Threshold Voltages
    vgs_threshold: 2.1V     # Gate-Source voltage to turn ON
    vds_saturation: 0.1V    # Drain-Source voltage when ON
    
    # Current Specifications
    max_drain_current: 200mA
    on_resistance: 5 Ohms   # R_DS(on)
    
    # Power Specifications
    max_power: 400mW
    
    pins:
        Drain at [0, 1]
        Gate at [1, 0]
        Source at [2, 1]
```

### Mathematical Model

**Operating Regions**:

1. **Cutoff** (OFF state)
   - V_GS < V_threshold
   - I_D ≈ 0
   - MOSFET acts as open switch

2. **Triode/Linear** (ON state, low V_DS)
   - V_GS > V_threshold
   - V_DS < (V_GS - V_threshold)
   - Acts as voltage-controlled resistor

3. **Saturation** (ON state, high V_DS)
   - V_GS > V_threshold
   - V_DS ≥ (V_GS - V_threshold)
   - Current limited by V_GS

**Equations**:

```
Cutoff:
I_D = 0 (when V_GS < V_threshold)

Triode/Linear (ON as switch):
I_D = (V_DD - V_DS) / R_load
V_DS = I_D × R_DS(on)

Saturation (Amplification):
I_D = k × (V_GS - V_threshold)²

Power Dissipation:
P = V_DS × I_D
```

### Synthesizer Validation

1. **Check Gate Voltage**: Is V_GS ≥ V_threshold?
2. **Calculate Drain Current**: Based on operating region
3. **Calculate Voltage Drop**: V_DS = I_D × R_DS(on)
4. **Verify Limits**: I_D < max_drain_current, P < max_power

---

## How Transistors Create Digital Logic

### The NOT Gate (Inverter)

A NOT gate is just a transistor with a pull-up resistor:

```hw
define Component "NOT_Gate":
    add Resistor (10k) named R1
    add Transistor_NPN named T1
    
    # Circuit topology
    connect VCC to R1.in
    connect R1.out to T1.Collector
    connect T1.Emitter to GND
    
    pins:
        Input is T1.Base
        Output is T1.Collector
```

**Truth Table (Analog Reality)**:
```
Input = 0V (LOW):
  V_BE = 0V < 0.7V → Transistor OFF
  I_C = 0A
  V_out = VCC (pulled high by R1) → "1"

Input = 5V (HIGH):
  V_BE = 5V > 0.7V → Transistor ON
  I_C = (VCC - 0.2V) / 10kΩ
  V_out = 0.2V ≈ 0V → "0"
```

This is how we create the "digital" illusion from analog physics.

---

## Next Steps

1. ✅ Define BJT transistor model
2. ✅ Define MOSFET transistor model
3. 📋 Define switching time characteristics
4. 📋 Define thermal models for power transistors
5. 📋 Build validation algorithms for Engine A
6. 📋 Create standard transistor library

---

**Status**: Research Phase  
**Last Updated**: March 2026  
**Part of**: Hardware Script (.hw) Core Engine Development
