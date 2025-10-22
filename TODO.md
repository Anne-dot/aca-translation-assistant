# TODO - Current Tasks

**Last Updated:** 2025-10-22

---

## ✅ Recently Completed

### Issue #21 STEP 1.1 - Foundation Glossary Extraction (2025-10-22)
- ✅ Extraction script created (src/extract_foundation_glossary.py)
- ✅ Auto-split multiple meanings, extract seeAlso, parse synonyms
- ✅ DRY refactoring: 6 new utils functions, 3 modular functions
- ✅ Project cleanup: 6 legacy scripts → deprecated/
- ✅ Documentation: 3 READMEs created/updated
- ✅ Results: 334 terms → data/1_extracted/foundation_raw.json

### Interactive Review Script (2025-10-22 Session 5)
- ✅ review_multiple_meanings.py created (479 lines)
- ✅ All actions: Accept, Skip, Flag, Edit, Merge
- ✅ Flag with notes functionality
- ✅ Merge with preview and edit
- ✅ Issue #22 created (term type structure)
- ✅ FUTURE_IDEAS.md updated (split functionality)

### Review Enhancements (2025-10-22 Session 6)
- ✅ Statistics enhancement: actions tracking + percentages
- ✅ Migration script: migrate_add_actions.py (5 terms)
- ✅ Review filter: [2] Review not reviewed terms
- ✅ Manual review: 6 terms (5 accepted, 1 flagged)
- ✅ Documentation: 3 READMEs + PROJECT_OVERVIEW updated
- ✅ VISION.md: Long-term global platform vision

---

## 🎯 Current Priority

### Issue #21 - Data Pipeline Implementation (PHASE 1)
**Status:** STEP 1.1 manual review in progress
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/21

**Current Progress:**
- 11/334 terms reviewed (3.3%)
- 323/334 not reviewed (96.7%)
- 16 flagged terms (15 auto + 1 manual)
- Actions: 10 accepted, 1 merged, 1 flagged

**PRIORITY TASK:**
- ⏳ Continue manual review of terms
  - Use [2] Review not reviewed for quick simple terms
  - Use [f] Flag complex terms for later detailed review
  - Goal: Review majority of simple terms first

**After significant progress:**
- [ ] Review all flagged terms in detail ([1] Review flagged)
- [ ] Assess auto-split quality overall
- [ ] Decide if extractor needs refinement

**Next steps after STEP 1.1:**
- [ ] STEP 1.2: Extract TMS-Glossary-template.xlsx
- [ ] STEP 1.3: Extract Translation-Template.docx
- [ ] STEP 1.4: Merge 3 sources
- [ ] STEP 1.5: Cleaning & Normalization
- [ ] STEP 1.6: TBX Structure Transform

---

## 📋 Pending Tasks

### Issue #22 - Term Type Structure
**Status:** Open for discussion
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/22
**Priority:** Medium (defer to PHASE 2)
- Question: grammaticalType as string vs array
- Term complexity classification (idiom, phrasal verb)
- TBX-Basic alignment

### Issue #20 - Manual Glossary Guide
**Status:** Created, deferred to PHASE 3
**Dependencies:** Issue #21 (PHASE 1 & 2 complete first)
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/20
