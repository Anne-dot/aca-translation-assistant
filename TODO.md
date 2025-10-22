# TODO - Current Tasks

**Last Updated:** 2025-10-22

---

## ✅ Recently Completed

### Quality Check Script (2025-10-22 Session 6)
- ✅ quality_check.py created (210 lines, 22 functions)
- ✅ Auto-flagged 81 terms (21 missing type, 59 multiple types, 50 idioms)
- ✅ Issue #23 completed

### Manual Review Session (2025-10-22 Session 6)
- ✅ Reviewed 175 terms before crash
- ✅ Flagged 34 terms with normalization issues
- ✅ Identified 10 categories of formatting/structure problems
- ❌ All progress lost due to Unicode crash
- ✅ Issue #24 created (Unicode bug + progress saving)
- ✅ Issue #25 created (term normalization policies)

---

## 🎯 Current Priority

### Issue #24 - Fix Unicode Bug (URGENT)
**Status:** Open, blocking manual review
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/24

**Tasks:**
1. ⏳ Fix UTF-8 encoding in input handling
2. ⏳ Add progress saving after each action
3. ⏳ Add transaction-based saving with user feedback
4. ⏳ Test with Estonian characters

### Issue #25 - Term Normalization Policies
**Status:** Research needed
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/25

**Tasks:**
1. ⏳ Research best practices (ISO 1087, CAT tools, style guides)
2. ⏳ Make policy decisions for 10 categories
3. ⏳ Enhance quality_check.py with new checks
4. ⏳ Create term normalization script

### Issue #21 - Data Pipeline (BLOCKED)
**Status:** STEP 1.1 blocked by Issue #24
**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/21

**Current Progress:**
- 0/334 terms reviewed (progress lost in crash)
- 95 flagged by quality_check.py
- 34 terms identified needing normalization
- Waiting for Issue #24 fix before continuing

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
