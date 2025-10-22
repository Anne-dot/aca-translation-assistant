# Next Session - 2025-10-23

## ✅ Session 6 Completed (2025-10-22, 21:22-23:00)

### Quality Check & Manual Review
- ✅ quality_check.py created (210 lines, 22 functions)
- ✅ Auto-flagged 81 terms (missing type, multiple types, idioms)
- ✅ Manual review: 175 terms reviewed before crash
- ✅ Identified 34 terms with normalization issues (10 categories)
- ❌ Unicode crash - all progress lost

### Issues Created
- ✅ Issue #23: Quality check script (completed, needs enhancement)
- ✅ Issue #24: Unicode bug + progress saving + transactions
- ✅ Issue #25: Term normalization policies (research needed)

### Documentation
- ✅ All issues fully documented with details
- ✅ TODO.md updated
- ✅ NEXT_SESSION.md updated

---

## 🎯 Next Session: Fix Unicode Bug & Research

### Priority 1: Issue #24 - Fix Unicode Bug (URGENT)
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/24

**Tasks:**
1. ⏳ Fix UTF-8 encoding in `src/interactive_glossary_terms_review.py`
2. ⏳ Add progress saving after each action
3. ⏳ Add transaction-based saving with user feedback
4. ⏳ Test with Estonian characters (õ, ä, ö, ü)

### Priority 2: Issue #25 - Research Term Normalization
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/25

**Tasks:**
1. ⏳ Research best practices (ISO 1087, CAT tools, style guides)
2. ⏳ Make policy decisions for 10 categories:
   - Hyphens, capitalization, singular/plural
   - Quotation marks, parentheses, asterisks
   - Acronyms, prepositions, grammatical types
3. ⏳ Document decisions
4. ⏳ Enhance quality_check.py with new checks

### Blocked: Issue #21 - Manual Review
**Status:** Waiting for Issue #24 fix
**Current:** 0/334 terms reviewed (progress lost)

**After fixes:**
1. Run quality_check.py with enhanced checks
2. Resume manual review with [2] Unflagged - needs review
3. Use [f] Flag for terms needing normalization decisions
