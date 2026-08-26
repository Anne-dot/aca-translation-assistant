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
- [1] Flagged
- [2] Not reviewed
- [3] Reviewed - OK
- [4] Reviewed - Flagged
- [5] All terms
- [6] Show statistics and exit
- [7] Waiting for update
- [8] Unflagged - not reviewed yet

**Review Actions:**
- [a] Accept - Mark as reviewed (clears review notes)
- [d] Edit definition - Quick edit in external editor
- [e] Edit meanings - Modify definitions, synonyms, examples
- [t] Edit term fields - grammaticalType, seeAlso (with auto-split)
- [n] Edit review notes
- [m] Merge - Combine multiple meanings (with preview & edit)
- [f] Flag - Mark for review with optional note
- [w] Waiting for update - Park until the tool gains a needed feature
- [s] Skip - Review later
- [q] Quit review

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

**`tools/` package** (utils.py split into modules, Issue #34)
- Shared utility functions following DRY principle
- `filemanage.py`: `read_csv_file()`, `load_json_file()`, `save_json_file()`, `ensure_directory_exists()`
- `text_processing.py`: `clean_text()`, `parse_list_from_text()`, `has_numbered_meanings()`, `split_numbered_text()`, `shorten_text()`
- `normalization_detection.py` - **Normalization detection** (Issue #25): Categories 4, 5, 7, 8
  - `detect_parentheses_notation()` - (s), (ren), (es)
  - `detect_asterisk()` - footnote markers
  - `detect_multiple_terms_comma()` - comma-separated terms
  - `detect_multiple_terms_slash()` - slash-separated terms
  - `detect_verbose_seealso()` - suspicious seeAlso entries
  - `collect_normalization_issues()` - unified detection
- `ui.py`: `page_break()`

**`migrate_add_actions.py`**
- One-time migration script to add actions array to reviewed terms
- Retrospectively adds action tracking to pre-existing reviewed terms
- Determines action type based on meanings count (1=merged, 2+=accepted)

---

### Deprecated

**`deprecated/normalize_terms_review.py`**
- Standalone normalization review script (deprecated)
- Functionality integrated into `interactive_glossary_terms_review.py`
- Detection functions moved to `tools/normalization_detection.py` (DRY principle)

---

## 🎯 Active Development

**Current Focus:** PHASE 1 - Manual Review (Issue #21)

**Status:** Initial review pass complete (334/334): 139 reviewed OK, 195 flagged, 14 waiting for tool features
- Term normalization research complete ✅ (Issue #25)
- Normalization detection integrated ✅ (auto-detects categories 4, 5, 7, 8)
- Term field editing `[t]` implemented ✅
- grammaticalType auto-splitting ✅
- Review notes auto-cleanup ✅

**Features:**
- Automatic normalization issue detection during review
- Term counts shown in menu filters
- Complete term info display after edits
- Double-confirm workflow (edit → review → accept)

**Next:** Continue manual review (flagged terms priority), then STEP 1.2 (extract TMS xlsx)

---

**Last Updated:** 2026-08-21
