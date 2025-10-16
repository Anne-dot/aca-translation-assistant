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
- ✅ **New Approach:** Sõnaveeb enrichment (Issue #7) - script created, tested with 10 terms
- ✅ ISO 704 & ISO 1087 compliance - structured fields (part_of_speech, term_complexity)
- ✅ Term complexity classification - 213/826 terms are multi-word (complex/compound)
- ⏳ **Next:** Data pipeline refactoring, component terms extraction, full 826-term lookup

**Recent Completions (2025-10-15):**
- Issue #5: Code refactoring (DRY principle) ✅
- Issue #6: ISO 704 part_of_speech field ✅
- Issue #7: Sõnaveeb lookup + term_complexity ✅
- Issue #9: Signal handling fixes ✅
- Issue #11: Term cleaning utilities ✅

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
│   ├── aca-glossary.json         # Original ACA Glossary (845 terms)
│   ├── aca-glossary-eki.json     # With term_complexity field (826 terms)
│   └── estonian-only-terms.csv   # Estonian-only terms from Sõnaveeb
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
- **Standards:** ISO 704 lexicography standards
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
