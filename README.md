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

- ⚠️ **Step 1A & 1B:** EKI approach deprecated - EKI databases included in Sõnaveeb
- ✅ **TBX-Basic Standards Research:** Complete (Issue #13) - All 3 structural decisions finalized
- ✅ **Standards Documentation:** Field definitions, structure comparison, ATL workflow integration
- ✅ **Key Decisions:** Transaction history (full), status tracking (Variant C), component lookups (hybrid)
- ✅ ISO 704, ISO 1087, TBX-Basic (ISO 30042:2019) compliance
- ✅ Term complexity classification - 213/826 terms are multi-word (complex/compound)
- ⏳ **Next:** Design final JSON schema → Document data pipeline (Steps 2-5) → Create migration script

**Recent Completions:**
- 2025-10-16: Issue #13 - TBX-Basic research and all 3 structural decisions ✅
- 2025-10-15: Issues #5, #6, #7, #9, #11 ✅
- Sõnaveeb enrichment approach ✅
- ISO 704 & ISO 1087 compliance ✅

See detailed roadmap: [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)

---

## 📁 Project Structure

```
ATL_tõlkeprojekt/
├── src/                           # Source code
│   ├── sonaveeb_lookup.py        # Sõnaveeb enrichment (current)
│   ├── term_cleaning.py          # Term normalization utilities
│   ├── add_term_complexity.py    # ISO 1087 classification
│   └── utils.py                  # Shared utility functions
│
├── data/                          # Data files
│   ├── ACA_WSO/                   # ACA WSO glossary sources (498 terms total)
│   │   ├── foundation_glossary.csv    # Primary source (334 terms)
│   │   ├── foundation_glossay.ods     # Primary source (ODS format)
│   │   ├── foundation_glossary_from_csv.json # Primary source (JSON)
│   │   ├── TMS-Glossary-template.xlsx # Supplementary (102 unique)
│   │   ├── Translation-Foundation-Glossary-Template-2025.docx # Supplementary (62 unique)
│   │   └── README.md              # Source documentation (see Issue #18)
│   └── estonian-only-terms.csv    # Estonian-only terms from Sõnaveeb
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
│   │   ├── TBX-Basic_FIELDS.md  # Complete field reference (318 lines)
│   │   ├── STRUCTURE_COMPARISON.md # Current vs TBX-Basic
│   │   └── TBX_vs_MY_PLANS.md   # TBX vs ATL workflow (700+ lines)
│   └── web_pages/sonaveeb/       # Sõnaveeb debugging files
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

## 📝 License

MIT License (to be added)

---

**Version:** 0.3.0-alpha
**Last Updated:** 2025-10-16
