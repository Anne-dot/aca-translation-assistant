# TODO - Current Tasks

**Last Updated:** 2025-10-20

---

## ✅ Recently Completed

### Issue #14 - JSON Schema Design (CLOSED 2025-10-20)
- ✅ All 19 decisions complete
- ✅ JSON_SCHEMA_SPECIFICATION.md created (2100+ lines)
- ✅ aca-tbx-terminology-schema.json created (JSON Schema Draft 7)
- ✅ Schema tested and validated
- ✅ TBX-Basic v1.2.1 compliant
- ✅ Documentation updated (README, PROJECT_OVERVIEW)

---

## 🎯 Next Steps (Priority Order)

### 1. Migration Script (Decision 16)
**Status:** Not started
**Dependencies:** Issue #14 ✅ COMPLETE

**Tasks:**
- [ ] Create `src/migrate_to_tbx_structure.py`
- [ ] Implement current → TBX-Basic structure transformation
- [ ] Test with sample data
- [ ] Validate output against JSON Schema
- [ ] Document in DATA_PIPELINE.md

---

### 2. Phase 2 Enrichment
**Status:** Not started
**Dependencies:** Migration script

**Tasks:**
- [ ] Dictionary lookups (Merriam-Webster, Oxford, Sõnaveeb)
- [ ] Add Estonian translations
- [ ] ATL community review workflow
- [ ] Sonaveeb lookup integration (Issue #7 completion)

---

### 3. Issue #20 - Manual Glossary Guide
**Status:** Created, now unblocked
**Dependencies:** Issue #14 ✅ COMPLETE

**Link:** https://github.com/Anne-dot/aca-translation-assistant/issues/20

---

## 📋 Pending Tasks

### Create Master Glossary
**Status:** Waiting for migration script
- Input: 3 sources (foundation + TMS + Template 2025)
- Transform: Apply TBX-Basic schema
- Validate: Against aca-tbx-terminology-schema.json
- Output: 498 terms in structured JSON
