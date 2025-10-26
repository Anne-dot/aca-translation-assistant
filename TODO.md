# TODO - Current Tasks

---

## 🎯 Next Session

### Priority 1: Issue #27 - OOP Refactoring (IN PROGRESS)
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/27
**Status:** Design phase ~90% complete
**Current:** Ready to finalize class structure

**Completed (2025-10-26):**
- ✅ Full OOP structure (no hybrid)
- ✅ Display + Interaction separation
- ✅ Review workflow rules (5 actions: a/s/e/f/w)
- ✅ Editor format (human-readable, CAPS labels)
- ✅ Editor syntax (auto-fix, review notes)
- ✅ Validation rules (structure preservation)
- ✅ Error handling (crash recovery, backup, git automation)
- ✅ Save behavior rules (transaction pattern)
- ✅ UX rules (nano edit, letter menus)

**Still to decide:**
- ⏸️ Finalize class structure (classes, methods, responsibilities)

**Next steps:**
1. Finalize class structure (1-2 hours discussion)
2. Document final design in Issue #27
3. Start Phase 1 implementation (new session)

### Priority 2: Folder Cleanup
**Tasks:**
- Review and organize project folders
- Clean up temporary files
- Archive old/unused files

### Priority 3: Issue #26 - Synonym Edge Cases
**Status:** 6 edge cases documented
**Task:** Design and implement solutions for:
1. Multi-meaning terms
2. Partial synonyms
3. Synonym/seeAlso overlap
4. Conditional synonyms
5. Annotations in synonyms
6. Slash notation in synonyms

### Priority 4: Continue Manual Review
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/21
**Current:** 149/334 terms reviewed (44.6%)
  - Reviewed - OK: 116 terms
  - Reviewed - Flagged: 19 terms
  - Waiting for update: 14 terms
**Remaining:** 185 terms not reviewed (55.4%)
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
