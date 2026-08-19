# ACA Translation Assistant

**Translation assistant tool for Estonian ACA (Adult Children of Alcoholics) materials**

Building a systematic terminology database and translation workflow tool to support small ACA/ATL communities in creating consistent, high-quality translations.

---

## 📋 Overview

This project creates a comprehensive terminology database and translation assistant for ACA/ATL materials translation from English to Estonian, following [ACA WSO Translation Guidelines](aca_official_guidelines/).

### Why This Matters

ACA World Service Organization guidelines emphasize that a **glossary/terminology database is the FIRST and MANDATORY step** before translating any literature. This tool follows WSO's recommended workflow to ensure:

- Consistent terminology across all documents
- Authoritative sources (Sõnaveeb - includes EKI terminology databases)
- Practically tested translations (existing ATL materials)
- Systematic approach for resource-limited communities

---

## 🎯 Goals

**Primary Goal:** Build comprehensive EN→ET terminology database

**Secondary Goals:**
- Create CLI translation assistant tool (Milestone 2)
- Develop web-based collaboration platform for Estonian ATL community (Milestone 3)
- Scale to universal platform for small-language ACA communities worldwide (Milestone 4)

---

## 🚀 Current Status

**Milestone 1: Terminology Database** (IN PROGRESS)

**Recent Progress:**
- ✅ Quality check automation (Issue #23) - 81 terms auto-flagged
- ✅ Unicode bug fixed (Issue #24) - UTF-8 encoding + progress saving
- 📋 34 terms need normalization decisions (Issue #25)

**Current Priorities:** See [TODO.md](TODO.md)

See detailed roadmap: [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)

---

## 📁 Project Structure

```
ATL_tõlkeprojekt/
├── src/                           # Source code (see src/README.md)
│   ├── extract_foundation_glossary.py  # PHASE 1, STEP 1.1 extraction
│   ├── interactive_glossary_terms_review.py     # PHASE 1, STEP 1.1 quality control
│   ├── utils.py                   # Shared utility functions (DRY)
│   ├── sonaveeb_lookup.py        # Sõnaveeb enrichment (legacy)
│   ├── term_cleaning.py          # Term normalization utilities
│   └── add_term_complexity.py    # ISO 1087 classification
│
├── data/                          # Data files (see data/README.md)
│   ├── ACA_WSO/                   # ACA WSO glossary sources (498 terms total)
│   │   ├── foundation_glossary.csv    # Primary source (334 terms)
│   │   ├── TMS-Glossary-template.xlsx # Supplementary (102 unique)
│   │   ├── Translation-Foundation-Glossary-Template-2025.docx # Supplementary (62 unique)
│   │   └── README.md              # Source documentation
│   ├── 1_extracted/               # Extracted JSON files (PHASE 1)
│   │   └── foundation_raw.json    # 334 terms from foundation glossary
│   ├── 2_merged/                  # Merged data (future)
│   ├── 3_cleaned/                 # Cleaned data (future)
│   └── 4_tbx/                     # TBX output (future)
│
├── deprecated/                    # Deprecated EKI approach
│   ├── eki_collector_deprecated.py
│   ├── match_glossary_eki_deprecated.py
│   └── data/                     # Old EKI data files
│
├── docs/                          # Documentation
│   ├── PROGRESS_UPDATES.md       # Daily progress log (Estonian)
│   └── EXISTING_TOOLS_ANALYSIS.md # Translation tools analysis
│
├── research/                      # Research materials
│   ├── standards/                # TBX-Basic & ISO standards documentation
│   │   ├── JSON_SCHEMA_SPECIFICATION.md # Complete specification (2100+ lines)
│   │   ├── TBX-Basic_FIELDS.md  # Complete field reference (318 lines)
│   │   ├── STRUCTURE_COMPARISON.md # Current vs TBX-Basic
│   │   └── TBX_vs_MY_PLANS.md   # TBX vs ATL workflow (700+ lines)
│   └── web_pages/sonaveeb/       # Sõnaveeb debugging files
│
├── schemas/                       # JSON Schema validation files
│   └── aca-tbx-terminology-schema.json # JSON Schema Draft 7 validation
│
├── PROJECT_OVERVIEW_DRAFT.md      # Detailed project roadmap
├── DECISIONS.md                   # Technical decisions and architecture
├── FUTURE_IDEAS.md                # Pending decisions and future work
├── TODO.md                        # Current tasks (post-compacting)
└── instructions.md                # Claude Code instructions
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.x
- **Data Format:** JSON (current), SQLite (future)
- **Standards:** TBX-Basic v1.2.1 (ISO 30042:2019), ISO 704, ISO 1087
- **Version Control:** Git + GitHub Issues workflow

---

## 📖 Documentation

- **[PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)** - Complete project roadmap and milestones
- **[DECISIONS.md](DECISIONS.md)** - Technical decisions and architecture
- **[FUTURE_IDEAS.md](FUTURE_IDEAS.md)** - Pending decisions and future work
- **[TODO.md](TODO.md)** - Current tasks list
- **[docs/PROGRESS_UPDATES.md](docs/PROGRESS_UPDATES.md)** - Daily progress log (Estonian)
- **[GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues)** - Active development tasks

---

## 🤝 Contributing

This project is currently in private development. Future goal: open-source gift to the Estonian and global ACA/ATL communities.

---

**Version:** 0.5.0-alpha
**Last Updated:** 2025-10-22
