# TODO - Current Tasks

---

## 🎯 Next Session

### Priority 1: Finish Unflagged Review (11 terms)
**Goal:** Complete the clean, easy cases
**Filter:** [8] Unflagged - not reviewed yet
**Expected:** Quick wins, feel progress

### Priority 2: Update docs/PROGRESS_UPDATES.md
**After completing session:**
- Document today's work (2025-10-25)
- Review progress and insights
- Commit updates

### Priority 3: Continue Manual Review
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/21
**Status:** Review workflow improved significantly (2025-10-25)
**Current:** 149/334 terms reviewed (44.6%)
  - Reviewed - OK: 116 terms
  - Reviewed - Flagged: 19 terms
  - Waiting for update: 14 terms
**Remaining:** 185 terms not reviewed (55.4%)
  - Unflagged: 11 terms (clean cases)
  - Flagged: 193 terms (need review)
**Tool:** `python3 src/interactive_glossary_terms_review.py`

**Recent improvements (2025-10-25):**
- ✅ Auto-flagging normalization issues on startup
- ✅ 6 edge cases documented in Issue #26
- ✅ Waiting for update functionality [w]
- ✅ Filter [8] for unflagged, not-reviewed terms
- ✅ Normalization issues always shown in term display

**Available features:**
- Auto-flagging: normalization issues detected on startup
- Normalization detection (categories 4, 5, 7, 8)
- Term field editing `[t]` with grammaticalType splitting
- Review notes auto-cleanup after all edit actions
- Waiting for update `[w]` - mark terms needing script enhancement
- 8 filters including unflagged and waiting categories

**Active issues:**
- Issue #25: Term normalization policy (OPEN - ongoing decisions)
- Issue #26: Synonym data quality patterns (6 edge cases documented)

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
