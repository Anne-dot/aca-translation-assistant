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

**Next:** Interactive review script for multiple meanings verification

---

**Last Updated:** 2025-10-22
