# Source Code Scripts

**Extraction and processing scripts for ACA Translation Assistant**

---

## 📁 Current Scripts

### Data Extraction (PHASE 1)

**`extract_foundation_glossary.py`**
- Extracts foundation_glossary.csv to structured JSON
- Auto-detects and splits terms with multiple meanings
- Extracts grammatical types and cross-references
- Output: `data/1_extracted/foundation_raw.json`

**Usage:**
```bash
python3 src/extract_foundation_glossary.py
```

**Output:**
- 334 terms extracted
- Terms with multiple meanings flagged for review
- JSON structure with meanings array, synonyms as lists

---

### Quality Control (PHASE 1)

**`interactive_glossary_terms_review.py`**
- Interactive review tool for extracted terms
- Quality control for auto-split extraction logic
- Manual verification and editing

**Usage:**
```bash
python3 src/interactive_glossary_terms_review.py
```

**Menu Options:**
- [1] Review flagged terms only (needsReview: true)
- [2] Review not reviewed terms (no reviewedAt)
- [3] Review all terms
- [4] Show statistics and exit

**Review Actions:**
- [a] Accept - Mark as reviewed
- [s] Skip - Review later
- [f] Flag - Mark for review with optional note
- [e] Edit - Modify definitions, synonyms, examples
- [m] Merge - Combine multiple meanings (with preview & edit)
- [q] Quit - Save progress

**Statistics:**
- Percentage-based progress tracking
- Action distribution (accepted/merged/edited/flagged)
- Review status overview

**Output:**
- Updates `data/1_extracted/foundation_raw.json` in-place
- Adds timestamps and review notes
- Progress saved on quit

---

### Utilities

**`utils.py`**
- Shared utility functions following DRY principle
- File operations: `read_csv_file()`, `load_json_file()`, `save_json_file()`
- Directory operations: `ensure_output_dir()`
- Text processing: `clean_text()`, `parse_list_from_text()`, `normalize_term()`
- Multiple meanings detection: `detect_numbered_meanings()`, `split_numbered_text()`

**`migrate_add_actions.py`**
- One-time migration script to add actions array to reviewed terms
- Retrospectively adds action tracking to pre-existing reviewed terms
- Determines action type based on meanings count (1=merged, 2+=accepted)

---

## 🎯 Active Development

**Current Focus:** PHASE 1 - Data Extraction Pipeline (Issue #21)

**Status:** Manual review in progress (11/334 terms reviewed, 3.3%)
- Statistics enhancement complete ✅
- Actions tracking implemented ✅
- Review filters: flagged / not reviewed / all ✅

**Next:** Continue manual review (323 terms remaining), then STEP 1.2 (extract TMS xlsx)

---

**Last Updated:** 2025-10-22
