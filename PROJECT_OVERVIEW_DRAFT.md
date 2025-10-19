# ACA Translation Assistant - Project Overview (DRAFT)

## Quick Overview

**Mission:** Build a systematic terminology database and translation tools to help ACA/ATL communities translate materials consistently, even with limited resources.

**Current Status:** Milestone 1 in progress - Issue #14 JSON schema design (9/~15 decisions made), migration patterns established.

**Recent Completions:** Issue #14 created ✅ | 9 fundamental field decisions ✅ | Migration workflow patterns (ENUM + 3-phase) ✅ | TBX-Basic standards research ✅ | Field definitions documented ✅ | Structure decisions (3/3) ✅ | Issues #5, #6, #7, #9, #11 ✅ | Sonaveeb enrichment | ISO 704 & ISO 1087 compliant | EKI deprecated

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

**1A. Glossary Sources** ✅ COMPLETE (Issue #18)
- **Source:** ACA WSO official glossary materials
- **Input files:** 3 sources, 498 unique terms total
  - `data/ACA_WSO/foundation_glossary.csv` - PRIMARY (334 terms with full fields)
  - `data/ACA_WSO/TMS-Glossary-template.xlsx` - Supplementary (102 unique terms)
  - `data/ACA_WSO/Translation-Foundation-Glossary-Template-2025.docx` - Supplementary (62 unique terms)
- **Documentation:** See `data/ACA_WSO/README.md` and Issue #18
- **Output:** Master glossary JSON (following Issue #14 schema)
- **Status:** Sources identified and documented

**1B. Add Estonian Translations** ⏳ FUTURE
- **Sources:**
  - https://sonaveeb.ee/ (includes EKI terminology databases)
  - https://aare.edu.ee/dictionary.html
  - Other Estonian dictionaries as needed
- **Output:** Terms with Estonian equivalents from authoritative sources

**1C. Extract from Existing ATL Translations** ⏳ FUTURE
- **Sources:** All ATL in-use translations
  - Daily meditations (päevamõtted)
  - 12 Steps text (12 sammu tekst)
  - Website translations (kodulehe tõlked)
- **Output:** Practically tested translations in real ACA/ATL context
- **Note:** ATL translations may differ from dictionary sources - both are valuable

**1D. Collaboration Opportunities** 💡 OPTIONAL
- **EKI Terminology Database Team:** Contact established for potential future cooperation (see `EKI_terminibaasid_kontaktid.md` for details)
- **Glossary Team:** Request feedback and clarifications on translation choices
- **Community Review:** Share terminology database with ATL community for validation
- Note: These are opportunities to improve quality, not required steps

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

## Current Status & Open Questions (2025-10-16)

### What Has Been Completed

**Issues Closed:**
- ✅ **Issue #5:** Refactored shared code to `src/utils.py` (DRY principle)
- ✅ **Issue #6:** Added `part_of_speech` field to all 826 terms (ISO 704 compliance)
- ✅ **Issue #9:** Fixed Ctrl+C signal handling in sonaveeb_lookup.py
- ✅ **Issue #11:** Extracted term cleaning functions to `src/term_cleaning.py`

**Issues In Progress:**
- ⏳ **Issue #7:** Sonaveeb lookup script created, tested with 10 terms, awaiting data pipeline refactoring
- ⏳ **Issue #10:** glossary_manager_via_terminal.py (not started)

**Key Changes from Initial Plan:**

1. **EKI Approach Deprecated (Issues #1, #3, #4)**
   - **Reason:** EKI terminology databases already included in Sonaveeb
   - **Decision:** Use Sonaveeb lookup instead of separate EKI collection
   - **Deprecated files:** Moved to `deprecated/` folder:
     - `eki_collector_deprecated.py`
     - `load_eki_data_deprecated.py`
     - `match_glossary_eki_deprecated.py`
   - **Preserved logic:** Term cleaning functions extracted to `src/term_cleaning.py`

2. **Term Complexity Classification Added (Issue #7)**
   - **Discovery:** 213/826 terms are multi-word (complex/compound per ISO 1087)
   - **Implementation:** Added `term_complexity` and `component_terms` fields
   - **Impact:** Requires component term handling before Sonaveeb lookup
   - **Note:** ISO 704 and ISO 1087 standards followed from project start

3. **Documentation Structure**
   - **Created:** `FUTURE_IDEAS.md` for pending decisions and future work
   - **Purpose:** ADHD-friendly separation of current work vs future plans

4. **TBX-Basic Standards Research (2025-10-16)**
   - **Discovery:** TBX-Basic is FREE and OPEN standard for terminology exchange (ISO 30042:2019)
   - **Research completed:**
     - Downloaded TBX-Basic v1.2.1 specification and examples
     - Analyzed three-level hierarchy: Concept → Language → Term
     - Compared current JSON structure with TBX-Basic requirements
     - Compared TBX-Basic with planned ATL workflow features
   - **Documentation created:**
     - `research/standards/TBX-Basic_FIELDS.md` - Complete field reference (318 lines)
     - `research/standards/STRUCTURE_COMPARISON.md` - Current vs TBX-Basic (296 lines)
     - `research/standards/TBX_vs_MY_PLANS.md` - TBX vs my plans (700+ lines with ADHD summary)
   - **Key decisions made (3/3):**
     - ✅ Transaction history: Full history in `transactions[]` array (for collaboration)
     - ✅ Component lookups: Hybrid approach - data in `_metadata`, reference `has_components: true`
     - ✅ Status tracking: Variant C - both `atl_status` and `usage_status` (2025-10-16)
   - **Benefits:**
     - TBX-Basic compliant structure enables export to professional CAT tools
     - Follows international terminology management standards
     - Compatible with SDL Trados, MemoQ, and other professional tools
     - Supports ATL collaborative workflow with transaction tracking
   - **Next steps:**
     - Design final JSON schema based on all 3 decisions
     - Create migration script to new TBX-compliant structure
     - Document Steps 2-5 in DATA_PIPELINE.md

### Open Questions Requiring Decisions

**TBX-Basic Structure Decision (Priority: HIGH):**

0. **ATL Status Tracking: atl_in_use vs atl_approved** ✅ DECIDED
   - **Decision:** Variant C - Both separate statuses (`atl_status` + `usage_status`)
   - **Date:** 2025-10-16
   - **Rationale:** ATL texts contain historically used terms not yet reviewed. Need to distinguish "in use" vs "approved".
   - **Fields:**
     - `atl_status`: review decision (`candidate`, `atl_approved`, `rejected`)
     - `usage_status`: actual usage (`not_in_use`, `atl_in_use`, `formerly_in_use`)
   - **Documentation:** See `research/standards/TBX_vs_MY_PLANS.md`
   - **Impact:** Enables tracking both historical usage and review decisions independently

**Before Sonaveeb Full Lookup:**

1. **ACA Glossary .docx Cleanup & Field Mapping**
   - Review original Glossary document step-by-step
   - Identify what fields should emerge from cleanup process
   - Examples:
     - Grammatical markers `(n.)` → `part_of_speech` field?
     - Explanations `\n(...)` → `notes` field structure?
     - Multi-word terms → component handling?
   - **Status:** Not yet reviewed systematically

2. **Component Terms Extraction (213 terms)**
   - **Step A:** Generate component terms list from complex/compound terms
   - **Step B:** Review generic words decision:
     - Words like "to", "about", "for", "of", "the", "self", "based"
     - **Options:** Filter them out OR keep for lookup and see what emerges
     - **Current thinking:** Keep all, review results, decide filtering later
   - **Step C:** Add approved components to glossary as separate terms
   - **Step D:** Restructure lookup order: simple terms first → then complex
   - **Status:** Design complete (FUTURE_IDEAS.md), not implemented
   - **See:** FUTURE_IDEAS.md - "Component Terms Extraction" section

3. **Part of Speech Field Usage**
   - 107 terms have grammatical markers in `notes` field
   - **Question:** When to populate `part_of_speech`?
     - Before lookup? (probably not useful)
     - During manual review? (makes more sense)
   - **Status:** Field exists (Issue #6), population timing undecided

4. **Sonaveeb Database Filtering**
   - **Question:** Keep all Sonaveeb results or filter irrelevant databases?
   - **Example:** Automotive terminology not relevant for ACA/therapy
   - **Options:**
     - A: Pre-filter databases (cleaner results)
     - B: Keep ALL results, mark irrelevant during manual review with status
   - **Decision:** Variant B - small dataset, learn what exists, auto-filter later if patterns emerge
   - **Benefit:** Track rejected homonyms with reasons

5. **Data Flow Clarification**
   - Current files: `aca-glossary.json` → `aca-glossary-eki.json` (has deprecated EKI data)
   - **Questions:**
     - What is current "clean" glossary version?
     - Should we create new version without EKI data?
     - What should be input for component extraction?
     - What should be input for Sonaveeb lookup?
   - **Status:** Needs systematic review of data pipeline

### Recommended Next Steps

**Tomorrow's Fresh Start:**

1. **Review & Document Glossary Cleanup Pipeline**
   - Map: original .docx → current JSON → desired clean state
   - Identify all field mappings and transformations
   - Document what fields emerge from each step

2. **Implement Component Terms Extraction**
   - Part 1: Generate CSV of all components
   - Part 2: Review generic words (manual decision)
   - Part 3: Add to glossary

3. **Prepare Clean Glossary for Sonaveeb**
   - Determine correct input file
   - Verify structure matches Sonaveeb lookup expectations
   - Add any missing foundational terms (ACA→ATL, Adult Child→Täiskasvanud laps)

4. **Run Sonaveeb Lookup**
   - Full 826-term run
   - Simple terms first, then complex terms
   - Generate results for manual review

### Files & Locations

**Current Data:**
- `data/aca-glossary.json` - Original extraction
- `data/aca-glossary-eki.json` - With deprecated EKI matches + term_complexity
- `data/eki_combined.json` - Deprecated EKI combined data

**Scripts:**
- `src/sonaveeb_lookup.py` - Created and tested, needs refactoring for new pipeline (Issue #7)
- `src/term_cleaning.py` - Term cleanup utilities (Issue #11)
- `src/add_term_complexity.py` - Already executed
- `deprecated/` - Old EKI scripts preserved

**Documentation:**
- `FUTURE_IDEAS.md` - Component extraction, variant structure, future features
- `DECISIONS.md` - Architectural decisions log
- `PROJECT_OVERVIEW_DRAFT.md` - This document
- `research/standards/` - TBX-Basic standards documentation:
  - `TBX-Basic_FIELDS.md` - Complete field reference
  - `STRUCTURE_COMPARISON.md` - Current JSON vs TBX-Basic
  - `TBX_vs_MY_PLANS.md` - TBX-Basic vs ATL workflow (with ADHD summary)
  - `README.md` - Standards documentation index
  - `TBX-Basic_v1.2.1/` - TBX-Basic dialect package

---

**Status:** Milestone 1 in progress - TBX-Basic research complete, all 3 key decisions made, ready for final JSON schema design
**Date:** 2025-10-16
