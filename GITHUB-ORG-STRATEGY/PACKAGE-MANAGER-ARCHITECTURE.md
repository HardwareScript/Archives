# Package Manager Architecture (hpm)

**Hardware Script Package Manager**  
**Cost**: $0/month  
**Scalability**: Infinite  
**Last Updated**: March 2026

---

## The Core Concept: Index vs Assets

To keep the system fast and free, we separate the "Map" from the "Cargo":

### The Index (The Map)
- **Repository**: `hwsl-lang/registry`
- **Contents**: Lightweight JSON files only
- **Purpose**: Tells the compiler where to find packages
- **Size**: ~1KB per package
- **Hosting**: GitHub (free)

### The Assets (The Cargo)
- **Location**: Package author's own GitHub repository
- **Contents**: Actual `.hwx` files, `.hw` logic, `.glb` 3D models
- **Purpose**: The actual package code and assets
- **Size**: Can be megabytes
- **Hosting**: Author's GitHub Releases (free)

### How It Works

```
User runs: hpm install @sensors/imu-module

1. hpm CLI downloads JSON from hwsl-lang/registry
2. JSON contains: download_url = "https://github.com/author/imu/releases/v1.0.0.zip"
3. hpm downloads zip directly from author's GitHub
4. hpm extracts to ~/.hw/packages/sensors/imu-module/
5. hpm updates hw.lock with exact version and checksum
```

**Result**: Your server costs = $0. Your storage bloat = Zero.

---

## Namespace Strategy: Official vs Community

### 1. Standard Library (`@std/` or `@core/`)

**Examples**:
- `@std/materials`
- `@std/logic`
- `@std/power`
- `@std/sensors`

**Rules**:
- Only official organization members can publish
- Guaranteed to be safe, optimized, and mathematically perfect
- Maintained by core team
- Strict quality standards
- Comprehensive documentation required

**Publishing Access**: Restricted to `hwsl-lang` organization members

### 2. Community Packages (`@username/` or `@community/`)

**Examples**:
- `@johndoe/drone-motor`
- `@adafruit/neopixel`
- `@sparkfun/gps-module`
- `@sarah/brushless-motor`

**Rules**:
- Anyone can publish
- Community uses at their own risk
- Automated validation only (CI checks)
- Ecosystem can grow infinitely
- No manual review required

**Publishing Access**: Open to all GitHub users

### 3. Verified Publishers (`@verified/`)

**Future Enhancement**: For trusted manufacturers and organizations

**Examples**:
- `@espressif/esp32`
- `@arduino/uno`
- `@raspberry-pi/pico`

**Requirements**:
- Verified GitHub organization
- Proven track record
- Manufacturer endorsement

---

## The Complete Publishing Pipeline

### Step 1: Developer Creates Package

**Sarah creates a GitHub repo**: `github.com/sarah/hw-drone-motor`

**Package Structure**:
```
hw-drone-motor/
├── package.hw.json         # Metadata
├── motor.hwx               # Component definition
├── models/
│   └── motor.glb          # 3D model
├── examples/
│   └── basic-usage.hw     # Example code
├── tests/
│   └── motor-test.hwt     # Test bench
├── README.md              # Documentation
└── LICENSE                # MIT/Apache 2.0
```

**package.hw.json**:
```json
{
  "name": "@sarah/drone-motor",
  "version": "1.0.0",
  "description": "High torque brushless motor for drones",
  "author": "Sarah Johnson <sarah@example.com>",
  "license": "MIT",
  "repository": "https://github.com/sarah/hw-drone-motor",
  "keywords": ["motor", "drone", "brushless", "high-torque"],
  "electrical": {
    "voltage_min": "7.4V",
    "voltage_max": "22.2V",
    "current_max": "30A",
    "power_max": "500W"
  },
  "physical": {
    "dimensions": "28mm x 28mm x 30mm",
    "weight": "65g",
    "mounting": "M3 screws"
  },
  "dependencies": {
    "@std/materials": "^1.0.0"
  },
  "files": [
    "motor.hwx",
    "models/motor.glb",
    "examples/",
    "README.md"
  ]
}
```

**Sarah tests locally**:
```bash
# Verify syntax
hws check motor.hwx

# Run tests
hws test tests/motor-test.hwt

# Build example
hws build examples/basic-usage.hw
```

**Sarah tags a release**:
```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub automatically creates a release with downloadable zip file.

---

### Step 2: Developer Publishes Package

**Sarah runs**:
```bash
hpm publish
```

**What the CLI does behind the scenes**:

1. **Validates package.hw.json**:
   - Required fields present
   - Valid semantic version
   - Valid namespace (must match GitHub username)

2. **Checks GitHub release exists**:
   - Verifies tag exists on GitHub
   - Confirms release has downloadable assets

3. **Generates registry JSON**:
```json
{
  "name": "@sarah/drone-motor",
  "versions": {
    "1.0.0": {
      "description": "High torque brushless motor for drones",
      "author": "Sarah Johnson <sarah@example.com>",
      "license": "MIT",
      "repository": "https://github.com/sarah/hw-drone-motor",
      "download_url": "https://github.com/sarah/hw-drone-motor/archive/refs/tags/v1.0.0.zip",
      "checksum": "sha256:8f4e2d1a9c3b7e5f...",
      "published_at": "2026-03-15T10:30:00Z",
      "dependencies": {
        "@std/materials": "^1.0.0"
      }
    }
  }
}
```

4. **Opens Pull Request**:
   - Uses GitHub API to fork `hwsl-lang/registry`
   - Adds JSON file to `packages/sa/ra/sarah-drone-motor.json`
   - Opens PR with title: "Add @sarah/drone-motor v1.0.0"
   - PR body includes package description and changelog

---

### Step 3: Continuous Integration (Automated Validation)

**GitHub Action triggers on PR**: `.github/workflows/validate-package.yml`

```yaml
name: Validate Package Submission

on:
  pull_request:
    paths:
      - 'packages/**/*.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout registry
        uses: actions/checkout@v2
      
      - name: Install Hardware Script
        run: |
          curl -sSL https://hw-script.org/install.sh | bash
          echo "$HOME/.hw/bin" >> $GITHUB_PATH
      
      - name: Validate JSON schema
        run: |
          # Check JSON is valid
          # Check required fields present
          # Check version is semantic
          hpm validate-package ${{ github.event.pull_request.changed_files }}
      
      - name: Check download URL exists
        run: |
          # Verify URL returns 200 OK
          # Verify file is downloadable
          curl -I $DOWNLOAD_URL | grep "200 OK"
      
      - name: Download and verify checksum
        run: |
          # Download package zip
          # Calculate SHA-256
          # Compare with declared checksum
          wget $DOWNLOAD_URL -O package.zip
          echo "$CHECKSUM package.zip" | sha256sum -c
      
      - name: Security sandbox test
        run: |
          # Extract package in isolated container
          # Run syntax validation
          # Check for malicious patterns
          unzip package.zip -d /tmp/package
          hws check /tmp/package/*.hwx
      
      - name: Run package tests
        run: |
          # If package includes tests, run them
          if [ -d /tmp/package/tests ]; then
            hws test /tmp/package/tests/*.hwt
          fi
      
      - name: Auto-merge if all checks pass
        if: success()
        uses: pascalgn/automerge-action@v0.15.6
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MERGE_LABELS: "automerge,package-submission"
```

**Validation Checks**:

1. ✅ **Format Check**: JSON matches schema
2. ✅ **Link Check**: Download URL exists and is accessible
3. ✅ **Checksum Verification**: SHA-256 matches declared value
4. ✅ **Syntax Validation**: `.hwx` files compile without errors
5. ✅ **Security Scan**: No malicious patterns detected
6. ✅ **Test Execution**: Package tests pass (if present)
7. ✅ **Namespace Validation**: Author owns the namespace

**If all checks pass**: PR is automatically merged (30 seconds total)

**If any check fails**: PR is marked with failure reason, author can fix and resubmit

---

### Step 4: User Installation

**A teenager in Brazil wants to build a drone**:

```bash
hpm install @sarah/drone-motor
```

**What happens**:

1. **Fetch registry index**:
```bash
# hpm clones/pulls hwsl-lang/registry (cached locally)
git clone https://github.com/hwsl-lang/registry ~/.hw/registry
# Or if already exists:
cd ~/.hw/registry && git pull
```

2. **Read package metadata**:
```bash
# hpm reads packages/sa/ra/sarah-drone-motor.json
# Extracts download_url and checksum
```

3. **Download package**:
```bash
# Download directly from Sarah's GitHub
wget https://github.com/sarah/hw-drone-motor/archive/refs/tags/v1.0.0.zip
```

4. **Verify integrity**:
```bash
# Calculate SHA-256 and compare
echo "8f4e2d1a9c3b7e5f... package.zip" | sha256sum -c
```

5. **Extract to local cache**:
```bash
# Extract to ~/.hw/packages/@sarah/drone-motor/
unzip package.zip -d ~/.hw/packages/sarah/drone-motor/
```

6. **Update project files**:

**hw.toml** (updated):
```toml
[dependencies]
"@sarah/drone-motor" = "1.0.0"
```

**hw.lock** (auto-generated):
```toml
[[package]]
name = "@sarah/drone-motor"
version = "1.0.0"
source = "registry+https://github.com/hwsl-lang/registry"
checksum = "sha256:8f4e2d1a9c3b7e5f..."
dependencies = [
    "@std/materials 1.0.0",
]
```

7. **Ready to use**:
```hw
import DroneMotor from @sarah/drone-motor

define Space "Quadcopter":
    dimensions: 300mm by 300mm by 100mm
    grid: 300 by 300 by 10

add DroneMotor named Motor1 at [1, 50, 50]
add DroneMotor named Motor2 at [1, 250, 50]
add DroneMotor named Motor3 at [1, 50, 250]
add DroneMotor named Motor4 at [1, 250, 250]
```

---

## Registry Directory Structure

```
hwsl-lang/registry/
├── README.md                           # How to publish
├── CONTRIBUTING.md                     # Contribution guidelines
├── schema.json                         # Package JSON schema
├── packages/
│   ├── ad/
│   │   └── af/
│   │       └── adafruit-neopixel.json
│   ├── jo/
│   │   └── hn/
│   │       └── johndoe-drone-motor.json
│   ├── sa/
│   │   └── ra/
│   │       └── sarah-drone-motor.json
│   └── st/
│       └── d/
│           ├── std-materials.json
│           ├── std-logic.json
│           └── std-power.json
├── .github/
│   └── workflows/
│       ├── validate-package.yml        # Auto-validation
│       └── cleanup-old-versions.yml    # Maintenance
└── scripts/
    ├── publish.sh                      # Helper for publishing
    └── validate-schema.py              # Schema validator
```

**Why nested directories?**: Prevents single directory from having millions of files (Git performance optimization)

**Naming convention**: First 2 chars of package name → subdirectory

---

## Scaling Strategy

### Phase 1: Git-Based Registry (v0.1 - v1.0)

**Timeline**: 2026-2027  
**Capacity**: 10,000-50,000 packages  
**Cost**: $0/month  
**Infrastructure**: GitHub only

**When to use**: Early adoption phase

### Phase 2: Sparse Index (v1.0 - v2.0)

**Timeline**: 2027-2028  
**Capacity**: 50,000-500,000 packages  
**Cost**: $50-200/month  
**Infrastructure**: GitHub + CDN for index

**Optimization**: Instead of cloning entire registry, fetch only needed JSON files via HTTP

### Phase 3: Dedicated Registry Server (v2.0+)

**Timeline**: 2028+  
**Capacity**: 500,000+ packages  
**Cost**: $500-5,000/month  
**Infrastructure**: Custom registry server (like crates.io)

**When to use**: When Git repo becomes too large (>1GB)

**Funding sources by this point**:
- Corporate sponsors
- Research grants
- Venture capital
- Foundation support

---

## Comparison to Other Package Managers

| Feature | npm | Cargo | Homebrew | hpm |
|---------|-----|-------|----------|-----|
| Registry Type | Dedicated server | Sparse HTTP | Git repo | Git repo |
| Hosting Cost | $$$$ | $$$ | $0 | $0 |
| Package Hosting | Centralized | Centralized | Decentralized | Decentralized |
| Validation | Manual + CI | Manual + CI | CI only | CI only |
| Scalability | Millions | Millions | Hundreds of thousands | Tens of thousands |
| Initial Cost | High | Medium | Zero | Zero |

---

## Security Considerations

### Package Integrity

1. **Checksums**: Every package has SHA-256 checksum
2. **HTTPS**: All downloads over encrypted connections
3. **Immutable versions**: Once published, versions cannot be changed
4. **Audit trail**: All changes tracked in Git history

### Malicious Package Prevention

1. **Automated scanning**: CI checks for suspicious patterns
2. **Syntax validation**: All `.hwx` files must compile
3. **Community reporting**: Users can report malicious packages
4. **Quick removal**: Malicious packages removed via PR

### Namespace Squatting Prevention

1. **GitHub verification**: Package namespace must match GitHub username
2. **First-come-first-served**: No trademark enforcement initially
3. **Verified publishers**: Future system for official manufacturers

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)

- [ ] Create `hwsl-lang/registry` repository
- [ ] Design JSON schema for package metadata
- [ ] Implement basic directory structure
- [ ] Write README and contribution guidelines

### Phase 2: CLI Commands (Week 3-4)

- [ ] `hpm publish` - Publish package to registry
- [ ] `hpm install` - Install package from registry
- [ ] `hpm search` - Search for packages
- [ ] `hpm info` - Show package details
- [ ] `hpm update` - Update installed packages

### Phase 3: CI Automation (Week 5-6)

- [ ] GitHub Action for package validation
- [ ] Automated checksum verification
- [ ] Syntax validation in sandbox
- [ ] Auto-merge on success

### Phase 4: Documentation (Week 7-8)

- [ ] Publishing guide for developers
- [ ] Package structure best practices
- [ ] Security guidelines
- [ ] Example packages

---

## Example: Publishing Your First Package

### 1. Create Package Repository

```bash
mkdir hw-led-strip
cd hw-led-strip
git init
```

### 2. Create Package Files

**package.hw.json**:
```json
{
  "name": "@yourname/led-strip",
  "version": "1.0.0",
  "description": "Addressable RGB LED strip controller",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourname/hw-led-strip",
  "keywords": ["led", "rgb", "strip", "ws2812"],
  "dependencies": {
    "@std/materials": "^1.0.0"
  }
}
```

**led-strip.hwx**:
```hw
define Component "LED_Strip_WS2812":
    pins:
        VCC
        GND
        DIN
        DOUT
    
    electrical:
        voltage: 5V
        current_per_led: 60mA
        max_leds: 300
    
    layout:
        shape: Rectangle(5mm, 5mm, 2mm)
```

### 3. Test Locally

```bash
hws check led-strip.hwx
```

### 4. Create GitHub Release

```bash
git add .
git commit -m "Initial release"
git tag v1.0.0
git push origin main --tags
```

### 5. Publish to Registry

```bash
hpm publish
```

### 6. Wait for CI

GitHub Action validates your package (30 seconds)

### 7. Package is Live!

Users can now install:
```bash
hpm install @yourname/led-strip
```

---

## Conclusion

The Git-based package registry achieves:

- ✅ $0 hosting costs
- ✅ Infinite scalability (for early phase)
- ✅ Automated validation
- ✅ Decentralized asset hosting
- ✅ Community-driven growth
- ✅ No manual review required

**Inspired by**: Cargo (Rust), Homebrew (macOS), Go modules

**Next Step**: Read `CI-AUTOMATION-STRATEGY.md` for detailed GitHub Actions setup.
