# Deprecated Files

## 1. EKI Collection Approach (October 2025)

**Why deprecated:** Sõnaveeb already includes all EKI terminology databases, so separate collection is unnecessary.

### Scripts
- `eki_collector_deprecated.py` - EKI terminology collector (4 databases)
- `load_eki_data_deprecated.py` - EKI data loader and combiner
- `match_glossary_eki_deprecated.py` - Glossary-EKI matching algorithm

### Data (data/)
- `eki_terms/` - 4 EKI terminology databases (1,278 terms total)
  - `eki_kriis_20251014.json` (82 terms)
  - `eki_skt_20251014.json` (250 terms)
  - `eki_dkt_20251014.json` (301 terms)
  - `eki_TAI_20251014.json` (645 terms)
- `eki_combined.json` - Combined EKI data (564 EN terms, 262 ET-only)
- `eki-terms.csv` - EKI terms review file
- `glossary-review.csv` - Glossary-EKI match review file

**What was preserved:** Term cleaning functions → `src/term_cleaning.py` (Issue #11)

**Issues:** #1, #3, #4, #7, #11

---

## 2. Old Glossary Sources & Documentation (October 2025)

**Why deprecated:** New glossary sources identified (Issue #18).

### Old Glossary Data
- `aca-glossary.json` - 210 terms from Glossary_templatesonavara.docx
- `Glossary_templatesonavara.docx` - Original ACA Glossary template

**Replaced by:** 3 new sources (498 terms total)
- `data/ACA_WSO/foundation_glossary.csv` (334 terms, PRIMARY)
- `data/ACA_WSO/TMS-Glossary-template.xlsx` (102 unique)
- `data/ACA_WSO/Translation-Foundation-Glossary-Template-2025.docx` (62 unique)

### Old Documentation
- `DATA_PIPELINE_old.md` - Described .docx → aca-glossary.json pipeline
- `MANUAL_REVIEW_GUIDE_old.md` - Guide for editing aca-glossary-eki.json
- `STRUCTURE_COMPARISON_old.md` - aca-glossary-eki.json vs TBX-Basic analysis

**Issues:** #18 (glossary sources), #19 (documentation update), #20 (new guide needed)

---

**Current glossary:** See `data/ACA_WSO/README.md`
