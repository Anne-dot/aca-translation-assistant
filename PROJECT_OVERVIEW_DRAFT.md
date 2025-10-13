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

**1B. Match Glossary with EKI** 📍 CURRENT
- Source document: `/home/d0021/Documents/ATL_drive/Jagatud/Glossary_templatesonavara.docx`
- Input: `data/aca-glossary.json` (845 terms: 210 filled + 635 untranslated)
- Output: `data/aca-glossary-eki.json` (Glossary enriched with EKI matches)
- Process steps:
  1. ✅ Extract Glossary terms (DONE)
  2. Load and prepare EKI data (4 databases, 1,265 terms)
  3. Implement matching algorithm (English→English, find Estonian pair by definition)
  4. Create enriched database (combine Glossary + EKI matches)
  5. Generate matching statistics (matched/unmatched report)
  6. Manual review and validation (check quality)
- Important: Glossary "draft" translations are NOT reliable - EKI equivalents replace them

**1C. Extract from Existing ATL Translations** ⏳ NEXT
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

**Status:** Ready for implementation
**Date:** 2025-10-14
