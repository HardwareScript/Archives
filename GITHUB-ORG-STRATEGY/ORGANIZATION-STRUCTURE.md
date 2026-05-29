# GitHub Organization Structure

**Hardware Script Organization**: `hwsl-lang`  
**Last Updated**: March 2026

---

## Overview

This document defines the complete structure of the `hwsl-lang` GitHub organization, designed to achieve:
- $0 hosting costs (using GitHub infrastructure)
- Clear separation of concerns
- Infinite scalability
- Professional open-source structure

---

## The Five Core Repositories

### 1. `hwsl-lang/compiler`

**Purpose**: The actual Hardware Script compiler and CLI tools

**Contents**:
```
compiler/
├── Cargo.toml              # Workspace manifest
├── Cargo.lock              # Dependency lockfile
├── build.bat               # Windows build script
├── build.sh                # Unix build script
├── README.md               # Getting started for contributors
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT or Apache 2.0
├── .github/
│   └── workflows/
│       ├── ci.yml          # Continuous integration
│       ├── release.yml     # Binary releases
│       └── test.yml        # Test suite
├── crates/
│   ├── hwc-cli/           # Command-line interface
│   ├── hwc-parser/        # Pest grammar parser
│   ├── hwc-compiler/      # Compiler orchestration
│   ├── hwc-engine/        # Voxel engine & routing
│   ├── hwc-physics/       # Physics validation
│   ├── hwc-export/        # Gerber/GDSII/OBJ export
│   ├── hwc-materials/     # Materials database
│   └── hwc-stdlib/        # Standard library loader
├── tests/
│   ├── integration/       # End-to-end tests
│   └── fixtures/          # Test .hw files
└── docs/
    └── ARCHITECTURE.md    # High-level compiler architecture
```

**GitHub Actions**:
- **CI**: Run tests on every PR
- **Release**: Build binaries for Windows/Mac/Linux on tagged releases
- **Publish**: Upload binaries to GitHub Releases (free CDN)

**Installation Flow**:
```bash
# Users download pre-built binaries from GitHub Releases
curl -sSL https://github.com/hwsl-lang/compiler/releases/latest/download/hwc-linux-x64.tar.gz | tar xz
```

**Why separate from stdlib**: Compiler and standard library can be versioned independently. Users can update stdlib without recompiling.

---

### 2. `hwsl-lang/architecture`

**Purpose**: Creation documentation, design philosophy, and RFCs

**Contents**:
```
architecture/
├── README.md                          # Index of all documents
├── 001-the-vision.md                  # Why Hardware Script exists
├── 002-first-principles-thinking.md   # Core design philosophy
├── 003-why-voxel-grid.md             # Why 3D tensor grid
├── 004-why-morton-z-curve.md         # Spatial indexing decision
├── 005-why-vecdeque-determinism.md   # Deterministic routing
├── 006-why-custom-emitters.md        # Why not generic libraries
├── 007-materials-database-design.md  # 3-tiered material system
├── 008-llm-native-design.md          # AI-first architecture
├── 009-package-manager-philosophy.md # Git-based registry
├── 010-zero-cost-hosting.md          # GitHub infrastructure strategy
├── rfcs/
│   ├── 0001-behavioral-synthesis.md  # Proposed: HDL-level synthesis
│   ├── 0002-quantum-support.md       # Proposed: Quantum computing
│   └── template.md                   # RFC template
└── decisions/
    ├── 001-rust-over-cpp.md          # Why Rust
    ├── 002-pest-over-lalrpop.md      # Why Pest parser
    └── 003-no-floating-point.md      # Why i64 fixed-point
```

**Audience**: Future contributors, researchers, academics

**Why this exists**: When contributors join the project, they need to understand:
- Why you chose Morton Z-curve encoding over HashMaps
- Why you used VecDeque for determinism
- Why you built custom emitters instead of generic libraries
- The first-principles thinking behind every major decision

**Without this repository**: Contributors will submit PRs that use floating-point math or HashMaps because they don't understand the underlying ideology.

**RFC Process** (Request For Comments):
1. Contributor writes RFC in `rfcs/NNNN-feature-name.md`
2. Opens PR for community discussion
3. After consensus, RFC is merged
4. Implementation PR references the RFC

---

### 3. `hwsl-lang/docs`

**Purpose**: User-facing documentation website

**Contents**:
```
docs/
├── book.toml                    # mdBook configuration
├── src/
│   ├── SUMMARY.md              # Table of contents
│   ├── introduction.md         # Getting started
│   ├── installation.md         # How to install
│   ├── quick-start.md          # First circuit tutorial
│   ├── language-spec/
│   │   ├── syntax.md           # Core syntax
│   │   ├── grid-system.md      # 3D coordinate system
│   │   ├── components.md       # Component placement
│   │   ├── routing.md          # Routing syntax
│   │   └── abstractions.md     # Five abstraction blocks
│   ├── ecosystem/
│   │   ├── file-extensions.md  # All file types
│   │   ├── project-structure.md
│   │   └── package-manager.md  # hpm usage
│   ├── compiler/
│   │   ├── cli-reference.md    # All CLI commands
│   │   ├── build-targets.md    # PCB, FPGA, ASIC
│   │   └── error-codes.md      # Error reference
│   ├── tutorials/
│   │   ├── led-blink.md        # Beginner
│   │   ├── sprinkler.md        # Intermediate
│   │   └── robot.md            # Advanced
│   └── reference/
│       ├── standard-library.md # stdlib reference
│       └── materials.md        # Material properties
├── theme/                       # Custom CSS/JS
└── .github/
    └── workflows/
        └── deploy.yml          # Auto-deploy to GitHub Pages
```

**Hosting**: GitHub Pages (100% free)

**URL**: `https://docs.hw-script.org` (custom domain via CNAME)

**Build Tool**: mdBook (Rust's standard documentation tool)

**Deployment**:
```yaml
# .github/workflows/deploy.yml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: peaceiris/actions-mdbook@v1
      - run: mdbook build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./book
```

**Why separate from compiler**: Documentation can be updated without releasing a new compiler version.

---

### 4. `hwsl-lang/stdlib`

**Purpose**: Official Hardware Script standard library

**Contents**:
```
stdlib/
├── README.md
├── materials/
│   └── standard-materials.hwmat    # Core materials (Copper, FR4, Silicon)
├── components/
│   ├── power/
│   │   ├── battery.hwx
│   │   ├── voltage-regulator.hwx
│   │   └── buck-converter.hwx
│   ├── passive/
│   │   ├── resistor.hwx
│   │   ├── capacitor.hwx
│   │   └── led.hwx
│   ├── sensors/
│   │   ├── temperature.hwx
│   │   ├── light.hwx
│   │   └── imu.hwx
│   ├── logic/
│   │   ├── and-gate.hwx
│   │   ├── or-gate.hwx
│   │   └── comparator.hwx
│   └── comms/
│       ├── uart.hwx
│       ├── i2c.hwx
│       └── spi.hwx
├── assets/
│   ├── resistor.glb
│   ├── capacitor.glb
│   └── led.glb
└── tests/
    └── component-tests.hwt
```

**Versioning**: Semantic versioning (v1.0.0, v1.1.0, etc.)

**Installation**: Bundled with compiler, but can be updated independently

**Why separate**: Standard library can evolve faster than compiler. Users can update components without recompiling the entire toolchain.

---

### 5. `hwsl-lang/registry`

**Purpose**: Git-based package manager index (like crates.io, but free)

**Contents**:
```
registry/
├── README.md                    # How to publish packages
├── index/
│   ├── po/
│   │   └── we/
│   │       └── power-5v-regulator.json
│   ├── se/
│   │   └── ns/
│   │       └── sensors-imu-module.json
│   └── mo/
│       └── to/
│           └── motor-h-bridge.json
├── .github/
│   └── workflows/
│       └── validate.yml         # Validate package submissions
└── scripts/
    └── publish.sh               # Helper script for publishing
```

**How It Works**:

1. **Package Structure** (in author's own repo):
```
@power/5v-regulator/
├── package.hw.json         # Metadata
├── regulator.hw            # Component definition
├── models/
│   └── regulator.glb       # 3D model
└── README.md
```

2. **Publishing Process**:
```bash
# Author runs in their package repo
hpm publish

# This:
# 1. Validates package.hw.json
# 2. Creates a GitHub Release with zipped source
# 3. Opens PR to hwsl-lang/registry with JSON file
```

3. **Registry JSON File** (`index/po/we/power-5v-regulator.json`):
```json
{
  "name": "@power/5v-regulator",
  "versions": {
    "1.2.0": {
      "checksum": "a3f8b9c2d1e4...",
      "download_url": "https://github.com/author/5v-regulator/releases/download/v1.2.0/package.tar.gz",
      "dependencies": {
        "@standard/materials": "^1.0.0"
      }
    },
    "1.1.0": {
      "checksum": "7e2a1f5c8b3d...",
      "download_url": "https://github.com/author/5v-regulator/releases/download/v1.1.0/package.tar.gz",
      "dependencies": {}
    }
  }
}
```

4. **Installation Process**:
```bash
# User runs
hpm install @power/5v-regulator

# hpm CLI:
# 1. Clones/fetches hwsl-lang/registry (cached locally)
# 2. Reads index/po/we/power-5v-regulator.json
# 3. Downloads tar.gz from author's GitHub Releases
# 4. Extracts to ~/.hw/packages/power/5v-regulator/
# 5. Updates hw.lock with exact version and checksum
```

**Why This Works**:
- ✅ Zero server costs (Git is the database)
- ✅ Infinite scalability (GitHub's CDN)
- ✅ Decentralized (packages live in author's repos)
- ✅ Immutable (checksums prevent tampering)
- ✅ Offline-capable (registry can be cached)

**Inspired By**: Cargo's original design, Go modules, Nix

---

## Additional Repositories (Future)

### `hwsl-lang/examples`

**Purpose**: Example projects and tutorials

**Contents**:
- LED blinker
- Automated sprinkler
- Robot controller
- USB device
- DDR4 memory controller

### `hwsl-lang/vscode-extension`

**Purpose**: VS Code language support

**Features**:
- Syntax highlighting
- IntelliSense
- Error checking
- 3D preview panel

### `hwsl-lang/blender-plugin`

**Purpose**: Blender integration for visualization

**Features**:
- Import .hwx files
- Animate electron flow
- Generate photorealistic renders

---

## Repository Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                     hwsl-lang Organization                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   compiler   │─────▶│    stdlib    │                     │
│  │  (Rust code) │      │ (components) │                     │
│  └──────────────┘      └──────────────┘                     │
│         │                      │                             │
│         │                      │                             │
│         ▼                      ▼                             │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │     docs     │      │   registry   │                     │
│  │ (GitHub Pages)      │ (Git index)  │                     │
│  └──────────────┘      └──────────────┘                     │
│         │                      │                             │
│         │                      │                             │
│         ▼                      ▼                             │
│  ┌─────────────────────────────────────┐                    │
│  │          architecture               │                    │
│  │     (Design philosophy & RFCs)      │                    │
│  └─────────────────────────────────────┘                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Cost Analysis

| Service | Cost | Usage |
|---------|------|-------|
| GitHub Organization | $0 | Public repos are free |
| GitHub Actions | $0 | 2,000 minutes/month free |
| GitHub Releases | $0 | Unlimited bandwidth |
| GitHub Pages | $0 | 1GB storage, 100GB bandwidth/month |
| Git LFS | $0 | 1GB storage, 1GB bandwidth/month |
| **Total** | **$0/month** | **Infinite scalability** |

---

## Comparison to Traditional Infrastructure

| Traditional | Hardware Script | Savings |
|-------------|-----------------|---------|
| Heroku ($7/month) | GitHub Pages ($0) | $84/year |
| AWS S3 ($5/month) | GitHub Releases ($0) | $60/year |
| PostgreSQL ($15/month) | Git ($0) | $180/year |
| CDN ($20/month) | GitHub CDN ($0) | $240/year |
| **Total** | **$47/month** | **$0/month** | **$564/year** |

---

## Security & Trust

**Package Integrity**:
- All packages have SHA-256 checksums
- Downloads are from author's GitHub Releases (HTTPS)
- Registry PRs are reviewed before merge
- Malicious packages can be removed via PR

**Compiler Integrity**:
- All releases are signed
- Reproducible builds (same input = same binary)
- Open-source (community can audit)

---

## Conclusion

This organization structure achieves:
- ✅ $0 hosting costs
- ✅ Infinite scalability
- ✅ Professional structure
- ✅ Clear separation of concerns
- ✅ Community-friendly
- ✅ Decentralized package management

**Next Step**: Read `MIGRATION-PLAN.md` for step-by-step migration guide.
