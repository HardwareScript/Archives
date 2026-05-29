# Hardware Script Level 4: Standard Logic Macros (The Digital Illusion)

**Version**: 0.1 (Research Phase)  
**Purpose**: Logic gates built from transistor arrangements  
**Status**: 📋 Planned

---

## Overview

Level 4 is where we finally create "digital logic" by packaging Level 3 transistors and Level 2 resistors into reusable logic gate macros.

**Key Principle**: Every logic gate is just a specific arrangement of analog components. There is no magic—just carefully balanced voltages and currents.

---

## Logic Gate Implementations

### NOT Gate (Inverter)

**Circuit**: Single transistor with pull-up resistor

```hw
define Component "NOT_Gate":
    grid: 3 by 3
    
    # Internal components
    add Resistor (10k) named R1 at [0, 1]
    add Transistor_NPN named T1 at [1, 1]
    
    # Internal wiring
    connect VCC to R1.in
    connect R1.out to T1.Collector
    connect T1.Emitter to GND
    
    # External pins
    pins:
        Input at [0, 0]   # Connected to T1.Base
        Output at [2, 2]  # Connected to T1.Collector
    
    body:
        spans: [0, 0] to [2, 2]
```

**Truth Table**:
```
Input | Output
------|-------
  0   |   1
  1   |   0
```

**Analog Reality**:
- Input LOW (0V) → T1 OFF → Output HIGH (5V)
- Input HIGH (5V) → T1 ON → Output LOW (0.2V)

---

### NAND Gate (Universal Gate)

**Circuit**: Two transistors in series with pull-up resistor

```hw
define Component "NAND_Gate":
    grid: 4 by 4
    
    # Internal components
    add Resistor (10k) named R1 at [0, 2]
    add Transistor_NPN named T1 at [1, 1]
    add Transistor_NPN named T2 at [2, 1]
    
    # Internal wiring (series configuration)
    connect VCC to R1.in
    connect R1.out to T1.Collector
    connect T1.Emitter to T2.Collector
    connect T2.Emitter to GND
    
    # External pins
    pins:
        InputA at [0, 0]
        InputB at [0, 1]
        Output at [3, 3]
    
    body:
        spans: [0, 0] to [3, 3]
```

**Truth Table**:
```
A | B | Output
--|---|-------
0 | 0 |   1
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```

**Analog Reality**:
- Both transistors must be ON for output to be LOW
- If either transistor is OFF, output is pulled HIGH

---

### NOR Gate

**Circuit**: Two transistors in parallel with pull-up resistor

```hw
define Component "NOR_Gate":
    grid: 4 by 4
    
    # Internal components
    add Resistor (10k) named R1 at [0, 2]
    add Transistor_NPN named T1 at [1, 0]
    add Transistor_NPN named T2 at [1, 2]
    
    # Internal wiring (parallel configuration)
    connect VCC to R1.in
    connect R1.out to T1.Collector
    connect R1.out to T2.Collector
    connect T1.Emitter to GND
    connect T2.Emitter to GND
    
    # External pins
    pins:
        InputA at [0, 0]
        InputB at [0, 1]
        Output at [3, 3]
    
    body:
        spans: [0, 0] to [3, 3]
```

**Truth Table**:
```
A | B | Output
--|---|-------
0 | 0 |   1
0 | 1 |   0
1 | 0 |   0
1 | 1 |   0
```

---

### AND Gate

**Implementation**: NAND + NOT

```hw
define Component "AND_Gate":
    grid: 7 by 4
    
    add NAND_Gate named G1 at [0, 0]
    add NOT_Gate named G2 at [4, 1]
    
    connect G1.Output to G2.Input
    
    pins:
        InputA at [0, 0]
        InputB at [0, 1]
        Output at [6, 3]
```

**Truth Table**:
```
A | B | Output
--|---|-------
0 | 0 |   0
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
```

---

### OR Gate

**Implementation**: NOR + NOT

```hw
define Component "OR_Gate":
    grid: 7 by 4
    
    add NOR_Gate named G1 at [0, 0]
    add NOT_Gate named G2 at [4, 1]
    
    connect G1.Output to G2.Input
    
    pins:
        InputA at [0, 0]
        InputB at [0, 1]
        Output at [6, 3]
```

---

### XOR Gate

**Implementation**: Complex arrangement of NAND gates

```hw
define Component "XOR_Gate":
    grid: 12 by 6
    
    add NAND_Gate named G1 at [0, 1]
    add NAND_Gate named G2 at [4, 0]
    add NAND_Gate named G3 at [4, 3]
    add NAND_Gate named G4 at [8, 1]
    
    # XOR logic: (A NAND B) NAND (A NAND A) NAND (B NAND B)
    connect InputA to G1.InputA
    connect InputB to G1.InputB
    connect InputA to G2.InputA
    connect InputA to G2.InputB
    connect InputB to G3.InputA
    connect InputB to G3.InputB
    connect G1.Output to G4.InputA
    connect G2.Output to G4.InputB
    
    pins:
        InputA at [0, 0]
        InputB at [0, 1]
        Output at [11, 5]
```

**Truth Table**:
```
A | B | Output
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```

---

## How Level 4 Feeds Level 5

Once we have these logic gate macros, Level 5 (rule syntax) can compile high-level logic into gate arrangements.

**Example**:
```hw
rule "AutoControl":
    if Sensor.value < 50%:
        Output state is ON
```

The Synthesizer translates this to:
1. Comparator circuit (analog) to check Sensor.value < 50%
2. NOT gate if logic needs inversion
3. Direct connection to Output transistor

---

## Standard Logic Library

### standard.logic Package

```hw
# Basic gates
import NOT_Gate from standard.logic
import NAND_Gate from standard.logic
import NOR_Gate from standard.logic
import AND_Gate from standard.logic
import OR_Gate from standard.logic
import XOR_Gate from standard.logic

# Complex logic
import Multiplexer from standard.logic
import Demultiplexer from standard.logic
import FlipFlop_D from standard.logic
import FlipFlop_SR from standard.logic
import Counter_4bit from standard.logic
```

---

## Next Steps

1. ✅ Define basic gate implementations (NOT, NAND, NOR)
2. ✅ Define derived gates (AND, OR, XOR)
3. 📋 Define sequential logic (flip-flops, latches)
4. 📋 Define arithmetic circuits (adders, multipliers)
5. 📋 Build gate library for standard.logic package
6. 📋 Create validation tests for each gate

---

**Status**: Research Phase  
**Last Updated**: March 2026  
**Part of**: Hardware Script (.hw) Core Engine Development
