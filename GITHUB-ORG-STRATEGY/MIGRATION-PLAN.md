# Migration Plan: Personal Repo → Organization

**From**: `CaneTheDev/Hardware-Script`  
**To**: `hwsl-lang` organization  
**Timeline**: 1-2 weeks  
**Last Updated**: March 2026

---

## Overview

This document provides a step-by-step guide for migrating Hardware Script from a personal experimental repository to a professional open-source organization.

**Goal**: Transform from "personal tool" to "community infrastructure"

---

## Pre-Migration Checklist

### Legal & Licensing

- [ ] Choose license (MIT or Apache 2.0 recommended)
- [ ] Add LICENSE file to all repositories
- [ ] Add copyright headers to source files
- [ ] Create CONTRIBUTING.md with contribution guidelines
- [ ] Create CODE_OF_CONDUCT.md

### Documentation Audit

- [ ] Review all documentation for accuracy
- [ ] Remove personal notes and TODOs
- [ ] Ensure all examples work
- [ ] Add installation instructions
- [ ] Create getting started guide

### Code Quality

- [ ] Run `cargo fmt` on all Rust code
- [ ] Run `cargo clippy` and fix warnings
- [ ] Ensure all tests pass
- [ ] Remove debug code and commented-out sections
- [ ] Add missing documentation comments

### Repository Cleanup

- [ ] Remove sensitive information (API keys, personal data)
- [ ] Clean up commit history (optional: squash WIP commits)
- [ ] Remove large binary files (use Git LFS if needed)
- [ ] Update .gitignore for production use

### Dependency Management

- [ ] Download all dependency libraries and include them in the project folder
- [ ] Vendor dependencies to ensure reproducible builds
- [ ] Document all external dependencies in README
- [ ] Verify project builds without internet access (offline-first)

---

## Migration Steps

### Step 1: Create GitHub Organization

**Timeline**: Day 1

1. **Create organization**:
   - Go to https://github.com/organizations/new
   - Organization name: `hwsl-lang`
   - Email: `hardwarescript@gmail.com`
   - Plan: Free (public repositories)

2. **Configure organization settings**:
   - Profile picture: Hardware Script logo
   - Description: "Hardware Script: A text-based hardware design language"
   - Website: `https://hw-script.org`
   - Twitter: `@hwsl_lang`

3. **Set up teams**:
   - `@hwsl-lang/core` - Core maintainers (you initially)
   - `@hwsl-lang/contributors` - Active contributors
   - `@hwsl-lang/community` - Community members

---

### Step 2: Create Core Repositories

**Timeline**: Day 1-2

#### 2.1 Create `hwsl-lang/compiler`

```bash
# On GitHub, create new repository
# Name: compiler
# Description: Hardware Script compiler and CLI tools
# Public: Yes
# Initialize: No (we'll push existing code)

# Locally, prepare the code
cd /path/to/Hardware-Script
git remote add org https://github.com/hwsl-lang/compiler.git

# Copy only the compiler code
mkdir -p /tmp/compiler-migration
cp -r hwc/ /tmp/compiler-migration/
cp Cargo.toml Cargo.lock build.bat build.sh /tmp/compiler-migration/
cp README.md LICENSE CONTRIBUTING.md /tmp/compiler-migration/

# Initialize new repo
cd /tmp/compiler-migration
git init
git add .
git commit -m "Initial commit: Hardware Script compiler v0.1.3"
git branch -M main
git remote add origin https://github.com/hwsl-lang/compiler.git
git push -u origin main
```

#### 2.2 Create `hwsl-lang/architecture`

```bash
# On GitHub, create new repository
# Name: architecture
# Description: Design philosophy, RFCs, and creation documentation
# Public: Yes

# Locally, prepare the architecture docs
mkdir -p /tmp/architecture-migration
cd /path/to/Hardware-Script

# Copy creation documentation
cp -r Docs/ /tmp/architecture-migration/
cp ARCHITECTURE-VISION.md /tmp/architecture-migration/
cp CHANGELOG.md /tmp/architecture-migration/

# Create README
cat > /tmp/architecture-migration/README.md << 'EOF'
# Hardware Script Architecture

This repository contains the design philosophy, architectural decisions, and RFCs for Hardware Script.

## Contents

- `Docs/` - Historical documentation and design evolution
- `rfcs/` - Request For Comments (proposed features)
- `decisions/` - Architectural Decision Records (ADRs)

## For Contributors

Before submitting a PR to the compiler, read:
1. `001-the-vision.md` - Why Hardware Script exists
2. `002-first-principles-thinking.md` - Core design philosophy
3. Relevant RFCs for the feature you're working on

## For Researchers

This repository documents the first-principles thinking behind every major decision in Hardware Script's design.
EOF

# Initialize and push
cd /tmp/architecture-migration
git init
git add .
git commit -m "Initial commit: Hardware Script architecture documentation"
git branch -M main
git remote add origin https://github.com/hwsl-lang/architecture.git
git push -u origin main
```

#### 2.3 Create `hwsl-lang/docs`

```bash
# On GitHub, create new repository
# Name: docs
# Description: User-facing documentation (GitHub Pages)
# Public: Yes
# Enable GitHub Pages: Yes (from main branch, /docs folder)

# Locally, prepare documentation
mkdir -p /tmp/docs-migration
cd /tmp/docs-migration

# Install mdBook
cargo install mdbook

# Initialize mdBook project
mdbook init

# Copy documentation content
cp -r /path/to/Hardware-Script/Docs/v0.1.3/* src/

# Create SUMMARY.md (table of contents)
cat > src/SUMMARY.md << 'EOF'
# Hardware Script Documentation

[Introduction](./introduction.md)

# Getting Started
- [Installation](./installation.md)
- [Quick Start](./quick-start.md)
- [Your First Circuit](./first-circuit.md)

# Language Reference
- [Syntax Overview](./LANGUAGE-SPEC.md)
- [Grid System](./grid-system.md)
- [Components](./components.md)
- [Routing](./routing.md)

# Ecosystem
- [File Extensions](./ECOSYSTEM.md)
- [Package Manager](./package-manager.md)
- [Project Structure](./project-structure.md)

# Advanced Topics
- [Compiler Internals](./COMPILER-INTERNALS.md)
- [Routing & Physics](./ROUTING-AND-PHYSICS.md)
- [Custom Components](./custom-components.md)

# Community
- [Contributing](./contributing.md)
- [Code of Conduct](./code-of-conduct.md)
EOF

# Build documentation
mdbook build

# Initialize and push
git init
git add .
git commit -m "Initial commit: Hardware Script documentation"
git branch -M main
git remote add origin https://github.com/hwsl-lang/docs.git
git push -u origin main
```

#### 2.4 Create `hwsl-lang/stdlib`

```bash
# On GitHub, create new repository
# Name: stdlib
# Description: Hardware Script standard library
# Public: Yes

# Locally, prepare standard library
mkdir -p /tmp/stdlib-migration
cd /tmp/stdlib-migration

# Create directory structure
mkdir -p materials components/{power,passive,sensors,logic,comms} assets tests

# Copy standard materials
cp /path/to/Hardware-Script/engine-test/standard-materials.yaml materials/

# Create README
cat > README.md << 'EOF'
# Hardware Script Standard Library

Official standard library for Hardware Script.

## Contents

- `materials/` - Standard materials database
- `components/` - Standard component definitions
- `assets/` - 3D models and footprints
- `tests/` - Test benches

## Usage

The standard library is automatically included with the Hardware Script compiler.

```hw
import Battery from standard.power
import LED from standard.passive
import Copper from standard.materials
```
EOF

# Initialize and push
git init
git add .
git commit -m "Initial commit: Hardware Script standard library"
git branch -M main
git remote add origin https://github.com/hwsl-lang/stdlib.git
git push -u origin main
```

#### 2.5 Create `hwsl-lang/registry`

```bash
# On GitHub, create new repository
# Name: registry
# Description: Hardware Script package registry (Git-based)
# Public: Yes

# Locally, prepare registry
mkdir -p /tmp/registry-migration
cd /tmp/registry-migration

# Create directory structure
mkdir -p packages .github/workflows scripts

# Create README
cat > README.md << 'EOF'
# Hardware Script Package Registry

Git-based package registry for Hardware Script.

## How to Publish

1. Create your package repository
2. Add `package.hw.json` with metadata
3. Tag a release on GitHub
4. Run `hpm publish`

The CLI will automatically open a PR to this repository.

## Directory Structure

```
packages/
├── ad/af/adafruit-neopixel.json
├── jo/hn/johndoe-drone-motor.json
└── st/d/std-materials.json
```

Packages are organized by first 2 characters of package name for Git performance.
EOF

# Create schema
cat > schema.json << 'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "versions"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^@[a-z0-9-]+/[a-z0-9-]+$"
    },
    "versions": {
      "type": "object",
      "patternProperties": {
        "^[0-9]+\\.[0-9]+\\.[0-9]+$": {
          "type": "object",
          "required": ["download_url", "checksum"],
          "properties": {
            "download_url": {"type": "string", "format": "uri"},
            "checksum": {"type": "string", "pattern": "^sha256:[a-f0-9]{64}$"},
            "dependencies": {"type": "object"}
          }
        }
      }
    }
  }
}
EOF

# Create GitHub Action for validation
mkdir -p .github/workflows
cat > .github/workflows/validate-package.yml << 'EOF'
name: Validate Package Submission

on:
  pull_request:
    paths:
      - 'packages/**/*.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Validate JSON schema
        run: |
          # TODO: Implement validation
          echo "Validating package submission..."
      
      - name: Auto-merge if valid
        if: success()
        uses: pascalgn/automerge-action@v0.15.6
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF

# Initialize and push
git init
git add .
git commit -m "Initial commit: Hardware Script package registry"
git branch -M main
git remote add origin https://github.com/hwsl-lang/registry.git
git push -u origin main
```

---

### Step 3: Set Up GitHub Actions

**Timeline**: Day 3

#### 3.1 Compiler CI/CD

Create `.github/workflows/ci.yml` in `hwsl-lang/compiler`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        rust: [stable]
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: ${{ matrix.rust }}
          override: true
      
      - name: Build
        run: cargo build --release
      
      - name: Run tests
        run: cargo test --all
      
      - name: Run clippy
        run: cargo clippy -- -D warnings
```

#### 3.2 Release Automation

Create `.github/workflows/release.yml` in `hwsl-lang/compiler`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact_name: hwc
            asset_name: hwc-linux-x64
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact_name: hwc.exe
            asset_name: hwc-windows-x64.exe
          - os: macos-latest
            target: x86_64-apple-darwin
            artifact_name: hwc
            asset_name: hwc-macos-x64
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          target: ${{ matrix.target }}
      
      - name: Build
        run: cargo build --release --target ${{ matrix.target }}
      
      - name: Upload binaries to release
        uses: svenstaro/upload-release-action@v2
        with:
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          file: target/${{ matrix.target }}/release/${{ matrix.artifact_name }}
          asset_name: ${{ matrix.asset_name }}
          tag: ${{ github.ref }}
```

---

### Step 4: Update Personal Repository

**Timeline**: Day 4

1. **Add deprecation notice** to `CaneTheDev/Hardware-Script`:

```markdown
# ⚠️ This repository has moved!

Hardware Script is now maintained by the `hwsl-lang` organization.

## New Locations

- **Compiler**: https://github.com/hwsl-lang/compiler
- **Documentation**: https://github.com/hwsl-lang/docs
- **Architecture**: https://github.com/hwsl-lang/architecture
- **Standard Library**: https://github.com/hwsl-lang/stdlib
- **Package Registry**: https://github.com/hwsl-lang/registry

## For Contributors

Please submit all new issues and pull requests to the appropriate repository in the `hwsl-lang` organization.

This repository is now archived and read-only.

---

**Historical Note**: This repository contains the original development history of Hardware Script from its inception to v0.1.3. It has been preserved for historical reference.
```

2. **Archive the repository**:
   - Go to repository settings
   - Scroll to "Danger Zone"
   - Click "Archive this repository"

---

### Step 5: Set Up Documentation Website

**Timeline**: Day 5

1. **Configure GitHub Pages** for `hwsl-lang/docs`:
   - Go to repository settings
   - Scroll to "GitHub Pages"
   - Source: main branch, /book folder
   - Custom domain: docs.hw-script.org

2. **Set up custom domain**:
   - Add CNAME file to repository
   - Configure DNS records:
     ```
     docs.hw-script.org CNAME hwsl-lang.github.io
     ```

3. **Test deployment**:
   - Push changes
   - Wait for GitHub Action to complete
   - Visit https://docs.hw-script.org

---

### Step 6: Announce Migration

**Timeline**: Day 6-7

1. **Create announcement blog post**
2. **Post on social media**:
   - Twitter/X
   - Reddit (r/programming, r/rust, r/hardware)
   - Hacker News
   - Dev.to

3. **Update all external links**:
   - Personal website
   - LinkedIn
   - Portfolio

4. **Email existing users** (if any)

---

## Post-Migration Tasks

### Week 2

- [ ] Set up community Discord server
- [ ] Create Twitter account (@hwsl_lang)
- [ ] Set up email (hardwarescript@gmail.com)
- [ ] Create FUNDING.yml for GitHub Sponsors
- [ ] Add badges to README (build status, license, etc.)

### Month 1

- [ ] Write blog posts about the project
- [ ] Create video tutorials
- [ ] Reach out to hardware communities
- [ ] Submit to Awesome lists (awesome-rust, awesome-hardware)

### Month 2-3

- [ ] Implement package manager (hpm)
- [ ] Create example projects
- [ ] Write comprehensive tutorials
- [ ] Build community

---

## Rollback Plan

If migration fails or issues arise:

1. **Keep personal repo active** until migration is confirmed successful
2. **Test all links** before archiving personal repo
3. **Backup all data** before deletion
4. **Gradual transition**: Keep both repos active for 1-2 weeks

---

## Success Criteria

Migration is successful when:

- [ ] All 5 core repositories are created and populated
- [ ] GitHub Actions are working
- [ ] Documentation website is live
- [ ] Personal repo is archived with redirect
- [ ] No broken links
- [ ] Community can find and contribute to the project

---

## Timeline Summary

| Day | Task | Status |
|-----|------|--------|
| 1 | Create organization and core repos | ⬜ |
| 2 | Populate repositories with code | ⬜ |
| 3 | Set up GitHub Actions | ⬜ |
| 4 | Update personal repository | ⬜ |
| 5 | Configure documentation website | ⬜ |
| 6-7 | Announce migration | ⬜ |

**Total Time**: 1 week for core migration, 2-3 months for full ecosystem

---

## Conclusion

This migration transforms Hardware Script from a personal experiment to a professional open-source project ready for community contributions and long-term growth.

**Next Step**: Execute Step 1 (Create GitHub Organization)
