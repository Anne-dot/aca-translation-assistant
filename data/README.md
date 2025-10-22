# Data Directory

**Source files and extracted data for ACA Translation Assistant**

---

## 📂 Directory Structure

```
data/
├── ACA_WSO/              # Source glossary files (498 terms total)
├── 1_extracted/          # Extracted JSON files (PHASE 1)
├── 2_merged/             # Merged data (PHASE 1 - future)
├── 3_cleaned/            # Cleaned and normalized (PHASE 1 - future)
└── 4_tbx/                # Final TBX output (PHASE 1 - future)
```

---

## 1️⃣ Source Files (`ACA_WSO/`)

**Complete glossary from three sources**

See detailed documentation: [ACA_WSO/README.md](ACA_WSO/README.md)

**Summary:**
- Foundation Glossary: 334 terms (primary source)
- TMS-Glossary-template.xlsx: 102 unique terms
- Translation-Foundation-Glossary-Template-2025.docx: 62 unique terms
- **Total: 498 unique terms**

---

## 2️⃣ Extracted Data (`1_extracted/`)

**Output from extraction scripts**

**Current files:**

**`foundation_raw.json`**
- Source: `ACA_WSO/foundation_glossary.csv`
- Terms: 334
- Script: `src/extract_foundation_glossary.py`
- Structure: Terms with meanings array, auto-split multiple definitions
- Fields: term, grammaticalType, seeAlso, meanings[], pageReferences, needsReview, reviewedAt, actions[], reviewNotes[]

**Status:** Extraction complete. Manual review in progress.
- Extracted: 334 terms
- Reviewed: 11/334 (3.3%)
- Not reviewed: 323/334 (96.7%)
- Flagged for review: 16 terms (15 auto-flagged + 1 manual)
- Actions tracked: accepted (10), merged (1), flagged (1)
- Review tool: `src/review_multiple_meanings.py`
- Features: Percentage-based statistics, action tracking, review filters

---

## 🔄 Data Pipeline (PHASE 1)

**Issue #21** - [Data Pipeline Implementation](https://github.com/Anne-dot/aca-translation-assistant/issues/21)

**Current Step:** 1.1 - Extract foundation_glossary.csv ✅

**Next Steps:**
- 1.2 - Extract TMS-Glossary-template.xlsx
- 1.3 - Extract Translation-Template.docx
- 1.4 - Merge three sources
- 1.5 - Cleaning & Normalization
- 1.6 - Transform to TBX structure

---

**Last Updated:** 2025-10-22
