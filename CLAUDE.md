# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## MANDATORY: Read Global Instructions First

**Before starting ANY work, you MUST:**

1. Read `instructions.md` (coding standards, collaboration rules, response format)
2. **Primary location:** `/home/d0021/Automation/05-ai-instructions/instructions.md`
3. **Fallback (if primary not found):** `docs/ai-instructions/instructions.md` (repo copy)
4. Read WITHOUT optimization (full file, not summary)
5. Follow these instructions ALWAYS throughout the session

## Project Overview

Translation assistant tool for Estonian ACA (Adult Children of Alcoholics) materials. Building systematic terminology database and translation workflow following ACA WSO Translation Guidelines.

**Status:** Milestone 1 - Terminology Database (IN PROGRESS)

**Primary Goal:** Build comprehensive EN→ET terminology database

**Future Goals:**
- CLI translation assistant tool (Milestone 2)
- Web-based collaboration platform for Estonian ATL community (Milestone 3)
- Universal platform for small-language ACA communities worldwide (Milestone 4)

## Why This Matters

ACA World Service Organization guidelines require **glossary/terminology database as FIRST and MANDATORY step** before translating literature. This ensures:
- Consistent terminology across all documents
- Authoritative sources (Sõnaveeb - includes EKI terminology databases)
- Practically tested translations (existing ATL materials)
- Systematic approach for resource-limited communities

## Commands

### Development
```bash
# Run scripts from project root
python3 src/extract_foundation_glossary.py
python3 src/interactive_glossary_terms_review.py
python3 src/add_term_complexity.py
```

### Common Operations
See `src/README.md` for detailed script documentation.

## Project Structure

```
ATL_tõlkeprojekt/
├── src/                        # Source code (Python scripts)
│   ├── extract_foundation_glossary.py
│   ├── interactive_glossary_terms_review.py
│   ├── utils.py                # Shared utilities (DRY)
│   ├── term_cleaning.py
│   └── add_term_complexity.py
├── data/                       # Data pipeline
│   ├── ACA_WSO/               # WSO glossary sources (498 terms)
│   ├── 1_extracted/           # Extracted JSON (PHASE 1)
│   ├── 2_merged/              # Merged data (future)
│   ├── 3_cleaned/             # Cleaned data (future)
│   └── 4_tbx/                 # TBX output (future)
├── deprecated/                # Old EKI approach
├── docs/                      # Documentation
│   ├── PROGRESS_UPDATES.md    # Daily progress log (Estonian)
│   └── EXISTING_TOOLS_ANALYSIS.md
├── research/standards/        # TBX-Basic & ISO standards docs
├── schemas/                   # JSON Schema validation
├── PROJECT_OVERVIEW_DRAFT.md  # Detailed roadmap
├── DECISIONS.md               # Technical decisions
├── FUTURE_IDEAS.md            # Pending decisions
└── TODO.md                    # Current tasks
```

## Technology Stack

- **Language:** Python 3.x
- **Data Format:** JSON (current), SQLite (future)
- **Standards:** TBX-Basic v1.2.1 (ISO 30042:2019), ISO 704, ISO 1087
- **Version Control:** Git + GitHub Issues workflow

## Important Files

- **PROJECT_OVERVIEW_DRAFT.md** - Complete project roadmap
- **DECISIONS.md** - Technical decisions and architecture
- **TODO.md** - Current tasks (updated real-time, active items only)
- **docs/PROGRESS_UPDATES.md** - Daily progress log (Estonian, history preserved)
- **src/README.md** - All scripts, how to run them, parameters
- **data/README.md** - Data pipeline explanation
- **GitHub Issues** - Active development tasks

## Recent Progress

- ✅ Quality check automation (Issue #23) - 81 terms auto-flagged
- ✅ Unicode bug fixed (Issue #24) - UTF-8 encoding + progress saving
- 📋 34 terms need normalization decisions (Issue #25)

## Key Principles

- **Single Source of Truth** - Code reuse via `src/utils.py`
- **GitHub Issues Workflow** - All decisions/findings in issue comments while working
- **Documentation** - Transfer important info to docs after issue closed
- **TODO Management** - Keep TODO.md updated real-time, delete completed items
- **Progress Updates** - History in `docs/PROGRESS_UPDATES.md`, current state in TODO.md

## Context

This is a passion project for Estonian ACA/ATL community. Future goal: open-source gift to global ACA communities. Human-first approach required (not corporate).
