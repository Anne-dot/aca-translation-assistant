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

**`review_multiple_meanings.py`**
- Interactive review tool for extracted terms
- Quality control for auto-split extraction logic
- Manual verification and editing

**Usage:**
```bash
python3 src/review_multiple_meanings.py
```

**Features:**
- [1] Review flagged terms / [2] Review all / [3] Show stats
- [a] Accept - Mark as reviewed
- [s] Skip - Review later
- [f] Flag - Mark for review with optional note
- [e] Edit - Modify definitions, synonyms, examples
- [m] Merge - Combine multiple meanings (with preview & edit)
- [q] Quit - Save progress

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

---

## 🎯 Active Development

**Current Focus:** PHASE 1 - Data Extraction Pipeline (Issue #21)

**Status:** Manual review in progress (2/19 flagged terms reviewed)

**Next:** Complete manual review, then STEP 1.2 (extract TMS xlsx)

---

**Last Updated:** 2025-10-22
