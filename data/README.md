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
- Fields: term, grammaticalType, seeAlso, meanings[], pageReferences, needsReview, reviewedAt, actions[], reviewNotes[], waitingForUpdate, waitingForUpdateAt
- `waitingForUpdate` / `waitingForUpdateAt`: term is parked until the review tool gains a feature it needs ("waiting for script update"). Parked terms are excluded from normal review filters and listed via review-tool filter [7].

**Status:** Initial review complete. Waiting for human-based TBX analysis (Issue #51).
- Total terms: 334
- Reviewed - OK: 139
- Reviewed - flagged: 195
- Waiting for update: 14
- Review tool: `src/interactive_glossary_terms_review.py`

**`synonyms_analysis.json`**
- Synonym analysis results from initial review
- Script: `src/extract_synonyms_for_analysis.py`

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

**Last Updated:** 2026-01-19
