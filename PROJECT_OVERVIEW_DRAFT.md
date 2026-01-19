# ACA Translation Assistant - Project Overview (DRAFT)

## Quick Overview

**Mission:** Build a systematic terminology database and translation tools to help ACA/ATL communities translate materials consistently, even with limited resources.

**Current Status:** Milestone 1 in progress

**Progress:** See [GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues) and commit history for current status.

---

## Table of Contents

- [Mission & Dream](#mission--dream)
- [Development Roadmap](#development-roadmap)
  - [Overview](#overview)
  - [Milestone 1: Terminology Database](#milestone-1-terminology-database-in-progress)
    - [1A. Glossary Sources](#1a-glossary-sources--complete-issue-18)
    - [1B. Add Estonian Translations](#1b-add-estonian-translations--future)
    - [1C. Extract from Existing ATL Translations](#1c-extract-from-existing-atl-translations--future)
    - [1D. Collaboration Opportunities](#1d-collaboration-opportunities--optional)
  - [Milestone 2: Personal CLI Translation Assistant](#milestone-2-personal-cli-translation-assistant)
  - [Milestone 3: Estonian Community Tool](#milestone-3-estonian-community-tool)
  - [Milestone 4: Multi-Language Platform](#milestone-4-multi-language-platform)

---

## Mission & Dream

Build a tool that helps all smaller and bigger ACA communities translate ACA material into their native language, even when they lack resources - small communities, few volunteers, limited financial support, unsustainable book sales, changing team members.

**Base materials:** ACA WSO (World Service Organization) official publications

**Official Guidelines (Downloaded 2025-10-14):**
- Translation-Process-Guidelines.pdf
- Guidelines-for-Translations.pdf
- Location: `aca_official_guidelines/`

**Why this matters:**
ACA WSO guidelines emphasize that glossary/terminology database is the FIRST and MANDATORY step before translating any literature. Terms must be translated CONSISTENTLY across all documents. This tool follows WSO's recommended workflow.

**Current Focus:**
Estonian ACA/ATL materials - building a systematic terminology database as the foundation.

---

## Development Roadmap

### Overview

**Milestone 1: Terminology Database** - Foundation for everything
**Milestone 2: Personal CLI Translation Assistant** - Interactive command-line tool
**Milestone 3: Estonian Community Tool** - Web-based collaboration platform
**Milestone 4: Multi-Language Platform** - Universal translation tool for global ACA communities

---

### Milestone 1: Terminology Database (IN PROGRESS)

**Goal:** Create comprehensive terminology database for ACA/ATL translation through systematic comparison of authoritative sources.

**Why this is the foundation:**
- ACA WSO guidelines mandate glossary as FIRST step
- Ensures consistent translation across all documents
- Valuable even standalone (can be used for manual translation)
- Required for all future milestones

**Sub-steps:**

**1A. Glossary Sources (EN)**
- **Goal:** Standards-compliant EN terminology database, ready for translation
- **Input:** 3 WSO sources (~500 terms)
  - `data/ACA_WSO/foundation_glossary.csv` - PRIMARY
  - `data/ACA_WSO/TMS-Glossary-template.xlsx` - Supplementary
  - `data/ACA_WSO/Translation-Foundation-Glossary-Template-2025.docx` - Supplementary
- **Deliverable:** JSON with all terms, structure finalized, field decisions documented
- **Standard:** TBX-Basic v1.2.1 (ISO 30042:2019), see Issue #14 schema (may evolve based on actual needs)
- **Documentation:** `data/ACA_WSO/README.md`, `research/standards/`
- **Issues:** `gh issue list --label "1a-glossary-sources" --repo Anne-dot/aca-translation-assistant`

**1B. Add Estonian Translations** ⏳ FUTURE
- Details to be defined at end of 1A, before starting 1B

**1C. Extract from Existing ATL Translations** ⏳ FUTURE
- Details to be defined at end of 1B, before starting 1C

**1D. Collaboration Opportunities** 💡 OPTIONAL
- Details to be defined at end of 1C, before starting 1D

**Terminology Database Structure:**

Each term contains:
- 🇬🇧 **English term** (e.g., "Inner Child")
- 🇪🇪 **Estonian equivalent(s)** - can have multiple variants from different sources:
  - **EKI equivalent** + EKI link (authoritative source)
  - **Daily text translation** + date reference (practically tested)
  - **Glossary draft** (initial translation, needs verification)
- 📝 **Comments/explanations** (context, nuances)
- 📚 **Usage examples** (sentences from original texts and translations)
- 🔗 **Source categories** (EKI / daily text / draft)
- 🏷️ **Topics** (e.g., "12-step terminology", "therapy", "emotions")
- ⭐ **Approval status** (officially approved or not)
- ❓ **TODO: Preferred variant** - if multiple equivalents exist, how to mark preferred/in-use variant?

**Database Format Decision:**
- ❓ **Needs decision:** SQLite / JSON / CSV?
  - **SQLite** - structured database, good query capabilities, ready for web app
  - **JSON** - human-readable, easy for version control, good for backups
  - **CSV** - simplest, can open/edit in Excel/Google Sheets
- 💡 **Recommendation:** Start with JSON (simple, readable, git-friendly) + SQLite in future

**Output:** Complete terminology database ready for use in Milestone 2 (CLI tool)

---

### Milestone 2: Personal CLI Translation Assistant

**Goal:** Interactive command-line tool for solo translator work.

**Key Features:**
- Uses Milestone 1 terminology database
- Identifies terms in source text
- Suggests translations from database
- Interactive term-by-term workflow
- Saves new translations back to database

**Status:** Not started (requires Milestone 1 completion)

---

### Milestone 3: Estonian Community Tool

**Goal:** Web-based interface for Estonian ACA/ATL translation team collaboration.

**Key Features:**
- Online interface
- Multiple users with roles (translator, reviewer, admin)
- Review workflow
- Shares terminology database from Milestone 1
- Progress tracking

**Status:** Future milestone (requires Milestone 2 completion)

---

### Milestone 4: Multi-Language Platform

**Goal:** Universal translation platform for global ACA communities, especially small-language speakers.

**Key Features:**
- Multiple language pairs
- Multi-language terminology databases
- Organization management
- Open source and free for ACA communities
- API for integration

**Status:** Future vision (requires Milestone 3 completion)

---

## Current Status

**Milestone:** M1 - Terminology Database
**Phase:** 1A - Glossary Sources

For detailed progress, see [GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues) and [DECISIONS.md](DECISIONS.md).

---

## Open Questions

Undecided questions about M1 (data flow, field mapping, component terms, etc.)

See [Issue #36](https://github.com/Anne-dot/aca-translation-assistant/issues/36)

---

## Files & Locations

See [README.md](README.md) for project structure, scripts, and data documentation.

---

**Status:** Milestone 1 in progress
**Date:** 2026-01-19
