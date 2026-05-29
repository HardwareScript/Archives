# GitHub Organization Strategy

**⚠️ IMPORTANT: This folder is NOT part of the Hardware Script codebase.**

This folder contains strategic planning documents for migrating Hardware Script from a personal experimental repository to a full open-source organization.

**Do NOT copy this folder when moving code to the `hwsl-lang` organization.**

---

## Purpose

This folder documents:
- How to structure the GitHub organization
- Where different types of content should live
- Migration strategy from personal repo to organization
- $0-cost hosting architecture using GitHub infrastructure

---

## Contents

- `ORGANIZATION-STRUCTURE.md` - Complete breakdown of all repositories in the organization
- `MIGRATION-PLAN.md` - Step-by-step guide for moving from personal repo to org
- `PACKAGE-MANAGER-ARCHITECTURE.md` - How to build a Git-based package registry
- `DOCUMENTATION-HOSTING.md` - Using GitHub Pages for free documentation hosting
- `CREATION-DOCS-STRATEGY.md` - What to do with first-principles development logs

---

## Quick Reference

### The hwsl-lang Organization Structure

hardware-script/hw        → compiler
hardware-script/spec      → language definition
hardware-script/std       → standard library
hardware-script/hpm       → package manager (future)
hardware-script/docs      → documentation
hardware-script/examples  → sample projects
hardware-script/ide       → IDE (future)

### What Goes Where

| Content Type | Destination | Why |
|--------------|-------------|-----|
| Rust compiler code | `hwsl-lang/compiler` | The actual implementation |
| First-principles logs | `hwsl-lang/architecture` | For future contributors |
| User documentation | `hwsl-lang/docs` | For end users |
| Standard library | `hwsl-lang/stdlib` | Separate versioning |
| Package index | `hwsl-lang/registry` | Git-based package manager |
| This strategy folder | **NOWHERE** | Personal planning only |

---

## Current Status

- [x] Personal repo created (`CaneTheDev/Hardware-Script`)
- [x] Core compiler architecture designed
- [x] Documentation structure established
- [ ] GitHub organization created (`hwsl-lang`)
- [ ] Repositories set up in organization
- [ ] Migration executed
- [ ] Package manager implemented
- [ ] Documentation site deployed

---

## Next Steps

1. Read `ORGANIZATION-STRUCTURE.md` for complete repository breakdown
2. Read `MIGRATION-PLAN.md` for step-by-step migration guide
3. Execute migration when ready
4. Archive personal repo with redirect to organization

---

**Last Updated**: March 2026  
**Status**: Planning Phase
