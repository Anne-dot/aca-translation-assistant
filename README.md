# ACA Translation Assistant

**Translation assistant tool for Estonian ACA (Adult Children of Alcoholics) materials**

Building a systematic terminology database and translation workflow tool to support small ACA/ATL communities in creating consistent, high-quality translations.

---

## 📋 Overview

This project creates a comprehensive terminology database and translation assistant for ACA/ATL materials translation from English to Estonian, following [ACA WSO Translation Guidelines](aca_official_guidelines/).

### Why This Matters

ACA World Service Organization guidelines emphasize that a **glossary/terminology database is the FIRST and MANDATORY step** before translating any literature. This tool follows WSO's recommended workflow to ensure:

- Consistent terminology across all documents
- Authoritative sources (EKI terminology databases)
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

- ✅ **Step 1A:** Collected 1,278 terms from 4 EKI terminology databases
- ✅ **Step 1B:** Matched 845 Glossary terms with EKI data (10 matches, 1.2% rate)
- ✅ CSV files generated for manual review
- ✅ JSON structure created with ISO 704 compliance
- ⏳ **Next:** Manual review and validation

**Recent Completions:**
- Issue #4: Automated matching algorithm ✅
- Issue #5: Code refactoring (DRY principle) ✅
- Issue #6: Add part_of_speech field (ISO 704) ✅

See detailed roadmap: [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)

---

## 📁 Project Structure

```
ATL_tõlkeprojekt/
├── src/                           # Source code
│   ├── eki_collector.py          # EKI data collector
│   ├── load_eki_data.py          # EKI data loader & combiner
│   ├── match_glossary_eki.py     # Matching algorithm
│   ├── generate_review_csv.py    # CSV generation for review
│   ├── add_part_of_speech.py     # Migration script
│   └── utils.py                  # Shared utility functions
│
├── data/                          # Data files
│   ├── eki_terms/                # EKI terminology databases (4 files)
│   ├── eki_combined.json         # Combined EKI data (564 EN, 262 ET)
│   ├── aca-glossary.json         # ACA Glossary (845 terms)
│   ├── aca-glossary-eki.json     # Enriched Glossary with EKI matches
│   ├── glossary-review.csv       # Manual review file (826 terms)
│   └── eki-terms.csv             # EKI reference (564 EN→ET pairs)
│
├── docs/                          # Documentation
│   └── MANUAL_REVIEW_GUIDE.md    # Manual JSON editing guide
│
├── PROJECT_OVERVIEW_DRAFT.md      # Detailed project roadmap
├── NEXT_SESSION.md                # Next session instructions
├── DECISIONS.md                   # Technical decisions and architecture
└── PROGRESS_UPDATES.md            # Daily progress log (Estonian)
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
- **[NEXT_SESSION.md](NEXT_SESSION.md)** - Instructions for continuing work
- **[docs/MANUAL_REVIEW_GUIDE.md](docs/MANUAL_REVIEW_GUIDE.md)** - Manual review workflow guide
- **[DECISIONS.md](DECISIONS.md)** - Technical decisions and architecture
- **[GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues)** - Active development tasks

---

## 🤝 Contributing

This project is currently in private development. Future goal: open-source gift to the Estonian and global ACA/ATL communities.

---

## 📝 License

MIT License (to be added)

---

**Version:** 0.2.0-alpha
**Last Updated:** 2025-10-15
