# ACA Translation Assistant - Project Overview (DRAFT)

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

**1A. Collect EKI Terminology** ✅ DONE
- Collected from 4 EKI terminology databases
- Total: 1,278 terms (1,265 usable for Glossary matching)
- Languages: Estonian + English (+ archived: Russian, Finnish, Latin)
- Data includes: synonyms, definitions, EKI links
- Location: `data/eki_terminid/*.json`
- Tool: `src/eki_koguja.py`

**1B. Match Glossary with EKI** ✅ DONE
- Source document: `/home/d0021/Documents/ATL_drive/Jagatud/Glossary_templatesonavara.docx`
- Input: `data/aca-glossary.json` (845 terms: 210 filled + 635 untranslated)
- Output: `data/aca-glossary-eki.json` (Glossary enriched with EKI matches)
- Process steps:
  1. ✅ Extract Glossary terms (DONE)
  2. ✅ Load and prepare EKI data (DONE - Issue #3)
     - Combined all 4 EKI databases into unified structure
     - English terms as dictionary keys for fast lookup during translation
     - Why English as keys: English is source language (WSO materials), enables quick translation workflow, supports multiple Estonian variants (EKI + ATL + Glossary), scalable to future languages (Milestone 4)
     - Output: `data/eki_combined.json` (564 English terms, 262 Estonian-only terms)
     - See: [Issue #3](https://github.com/Anne-dot/aca-translation-assistant/issues/3)
  3. ✅ Implement matching algorithm (DONE - Issue #4)
     - Automated matching with aggressive normalization (handle `(n.)`, `(v.)`, newlines)
     - Match rate: 10/845 (1.2%) - low rate expected (EKI = specialized, Glossary = general ACA terms)
     - Included definitions even when Estonian term missing (4 terms)
     - Tools: `src/match_glossary_eki.py`, `src/generate_review_csv.py`
     - Output: `data/aca-glossary-eki.json`, `data/glossary-review.csv`, `data/eki-terms.csv`
     - See: [Issue #4](https://github.com/Anne-dot/aca-translation-assistant/issues/4)
  4. ⏳ Manual review and validation (NEXT)
     - Review CSV files in Excel/Sheets
     - Find additional matches manually
     - Mark homonyms, set preferred variants
     - Checkpoints every 25 terms
- Important: Glossary "draft" translations saved as source `aca_draft_volunteer` for future reference
- Next enrichment: Additional sources (IATE, Sonaveeb, Aare, Eurotermbank) in Step 1B-4
- **Code quality:** Refactored shared functions to `src/utils.py` (DRY principle) - See: [Issue #5](https://github.com/Anne-dot/aca-translation-assistant/issues/5)

**1C. Extract from Existing ATL Translations** ⏳ FUTURE
- Sources: All ATL in-use translations
  - Daily meditations (päevamõtted)
  - 12 Steps text (12 sammu tekst)
  - Website translations (kodulehe tõlked)
- Input: `data/aca-glossary-eki.json` (from step 1B)
- Output: `data/aca-glossary-eki-atl.json` (final terminology database)
- Process:
  1. Extract original + translation pairs from all sources
  2. Identify terminology usage in context
  3. Match with existing database
  4. Add ATL translations (may differ from EKI - both are valuable)
  5. Mark terms as "practically tested in real ATL texts"
- Note: These contain practically tested translations in real ACA/ATL context
- **atl = ATL existing translations**
- **TODO (later):** Define reference format for each source type:
  - Daily meditations: date reference (MM-DD format)
  - BRB (Big Red Book): page number (lk XX)
  - 12 Steps: step number and point (Step X, pt Y)

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

**Status:** Milestone 1 in progress - Step 1B complete, manual review next
**Date:** 2025-10-15
