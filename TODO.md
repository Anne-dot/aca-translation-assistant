# TODO - Current Tasks

---

## 🎯 Next Session

### Priority 1: Continue Manual Review
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/21
**Status:** Review workflow improved significantly (2025-10-24)
**Current:** 40/334 terms reviewed (12.0%)
**Flagged:** 183 terms (54.8%) - includes 84 AI-flagged for synonyms issue
**Tool:** `python3 src/interactive_glossary_terms_review.py`

**Recent improvements (2025-10-24):**
- ✅ Flag/filter behavior now consistent
- ✅ Flag tied to review notes lifecycle
- ✅ All edit actions auto-save
- ✅ DRY principles applied throughout
- ✅ AI flagged 84 terms with definitions in synonyms field

**Available features:**
- Normalization detection (automatic for categories 4, 5, 7, 8)
- Term field editing `[t]` with grammaticalType splitting
- Review notes auto-cleanup after all edit actions
- Flag action `[f]` loops back to menu
- Separate filters: [3] Reviewed-OK, [4] Reviewed-Flagged

**Active issues:**
- Issue #25: Term normalization policy (OPEN - ongoing decisions)
- Issue #26: Synonyms vs definitions (84 terms flagged by AI)

---

## 📋 All Open Tasks

**See GitHub Issues:** https://github.com/Anne-dot/aca-translation-assistant/issues

---

## 💡 Future Ideas

**See:** [FUTURE_IDEAS.md](FUTURE_IDEAS.md)

---

## 🗂️ Housekeeping

### Folder cleanup needed
- Review and organize project folders
- Clean up temporary files
- Archive old/unused files

### UX review needed
- Review menu consistency: letters vs numbers for options
- Consider standardizing all menus to one format

### Script refactoring needed
- `interactive_glossary_terms_review.py` is 1414 lines - too large
- Needs ADHD-friendly restructuring
- Consider splitting into modules:
  - Display functions
  - Edit functions
  - Normalization handling
  - Review workflow
- Or consider OOP approach with classes:
  - `TermReviewer` class
  - `NormalizationHandler` class
  - `SynonymHandler` class
- Goal: More maintainable, easier to navigate and understand
