# Next Session - 2025-10-19

## ⚠️ FIRST: Read These Before Starting

**CRITICAL - Read every time before continuing work:**
1. `~/.claude/instructions.md` - Global non-negotiable requirements
2. `TODO.md` - Current task list and progress
3. **Issue #13** - TBX-Basic research (CLOSED - 3 structural decisions = FOUNDATION)
4. **Issue #14** - JSON schema design (IN PROGRESS, 9 field decisions made)

---

## Where We Left Off (2025-10-18 Session)

### ✅ Completed This Session

**Issue #14: JSON Schema Design Session (1 hour):**
- ✅ Created GitHub Issue #14 with proper milestone and label
- ✅ Made 9 fundamental field decisions (all documented in Issue #14 comments)
- ✅ Established migration workflow patterns (ENUM + 3-phase OPTIONAL→REQUIRED)
- ✅ Progress update added to docs/PROGRESS_UPDATES.md

**9 Decisions Made:**
1. ✅ **Naming Convention:** camelCase (TBX-Basic compliant)
2. ✅ **Field `id`:** REQUIRED, auto-generated ("c001", "c002", ...)
3. ✅ **Field `subjectField`:** REQUIRED ENUM with migration workflow
4. ✅ **Field `languages`:** EN REQUIRED, ET and others OPTIONAL
5. ✅ **Field `term`:** REQUIRED (obvious)
6. ✅ **Field `partOfSpeech`:** OPTIONAL now, REQUIRED later (3-phase workflow)
7. ✅ **Field `supersededBy`:** OPTIONAL, references term text (NOT ID)
8. ✅ **Field `note`:** OPTIONAL
9. ✅ **Field `source`:** REQUIRED object (type, addedBy, date all required)

**Patterns Established:**
- ENUM migration workflow (Decision 3) - reusable template
- 3-phase OPTIONAL→REQUIRED workflow (Decision 6) - reusable pattern
- Validation rules template

**Commits:**
- e2d8871 - Add progress update for 2025-10-18 JSON schema session

---

## 🎯 Next Concrete Step

### PRIORITY 1: Continue JSON Schema Design ⭐ NEXT TASK

**What:** Complete remaining field decisions for final JSON schema

**Time estimate:** 1-2 hours (depends on complexity of remaining fields)

**Remaining fields (~6-8 fields):**

1. **`workflow` object** (Term level)
   - `atl_status`: "candidate", "atl_approved", "rejected"
   - `usage_status`: "not_in_use", "atl_in_use", "formerly_in_use"
   - From Issue #13 Decision 2 (Variant C)

2. **`usageExamples` array** (Term level)
   - Translation decision documentation with context
   - Structure for examples from different translators
   - From TBX_vs_MY_PLANS.md

3. **`transactions` array** (Term level)
   - Full history tracking
   - From Issue #13 Decision 1
   - Fields: type, date, user, details

4. **`_metadata` fields** (Concept level)
   - `component_lookups` (from Issue #13 Decision 3)
   - `term_complexity` (from Issue #7)
   - `is_glossary_term` (boolean)
   - `derived_from` (array for component terms)

5. **Other TBX-Basic fields** (if needed)
   - `definition` (optional)
   - `context` (optional)
   - Review TBX-Basic_FIELDS.md for any missing important fields

**Steps:**
   - File: `research/standards/FINAL_JSON_SCHEMA.md`
   - Based on recommended structure from TBX_vs_MY_PLANS.md (lines 384-547)
   - Include complete example with all fields
   - Document all field definitions
   - Add validation rules

**Still to decide:**
- Naming convention: `administrativeStatus` (TBX camelCase) vs `administrative_status` (Python snake_case)?
- Required vs optional fields
- Allowed values for enum fields (atl_status, usage_status, administrativeStatus)
- `source` format: string vs object?

**Base structure already designed in TBX_vs_MY_PLANS.md** - mostly copy + minor decisions

---

### PRIORITY 2: Document Data Pipeline

**After JSON schema is done:**

1. **Update DATA_PIPELINE.md**
   - Document Steps 2-5 (currently only Step 1 exists)
   - Show transformation at each step
   - Include example data at each stage
   - Map: .docx → aca-glossary.json → enrichment → final TBX structure

2. **Plan migration strategy**
   - Current: `aca-glossary-eki.json`
   - Target: New TBX-compliant structure
   - Migration script: `src/migrate_to_tbx_structure.py`

---

### PRIORITY 3: Create Migration Script

**Script: `src/migrate_to_tbx_structure.py`**

**What it does:**
1. Load current `aca-glossary-eki.json`
2. Transform each term to new TBX-compliant structure:
   - Clean English term from string → separate `term` and `note`
   - Extract part_of_speech from markers `(n.)`, `(v.)`, etc.
   - Create `languages.en` and `languages.et` sections
   - Flatten all ET variants into `languages.et.terms[]`
   - Move `term_complexity`, `component_terms`, `is_glossary_term` → `_metadata`
   - Set appropriate `administrativeStatus` values
   - Create transaction history entries
3. Save to `data/aca-glossary-tbx.json`
4. Validate output
5. Generate migration report

**Success criteria:**
- ✅ All 826 terms migrated
- ✅ No data loss
- ✅ TBX-Basic compliant structure
- ✅ All custom ATL fields preserved
- ✅ JSON validates correctly

---

## 📋 Full Task List (from TODO.md)

**Current session tasks (Tasks #10-14):**
- ✅ #10: Progress update created
- ✅ #11: PROJECT_OVERVIEW_DRAFT.md updated
- ✅ #12: NEXT_SESSION.md updated (this file)
- ⏸️ #13: README.md needs updating
- ⏸️ #14: Git commit and push

**Data Pipeline (Task #3):**
- ⏸️ Decide Variant A/B/C (atl_in_use vs atl_approved)
- ⏸️ Design final JSON schema
- ⏸️ Document Steps 2-5 in DATA_PIPELINE.md
- ⏸️ Create migration script

**Future tasks:**
- Task #4: Analyze ACA Glossary .docx structure
- Task #5: Finalize component terms extraction design
- Task #6: Design enrichment sources integration
- Tasks #7-9: Component lookup, term cleaning, glossary manager (GitHub issues)

---

## 📁 Important Files

**Standards Documentation:**
- `research/standards/TBX_vs_MY_PLANS.md` ⭐ Complete structure designed (lines 384-547)
- `research/standards/TBX-Basic_FIELDS.md` - All field definitions
- `research/standards/STRUCTURE_COMPARISON.md` - Current problems identified
- `research/standards/README.md` - Standards documentation index

**GitHub Issues:**
- **Issue #13** (CLOSED) - TBX-Basic research summary - Single source of truth for all decisions

**Current Data:**
- `data/aca-glossary-eki.json` - Current structure (needs migration)
- `data/Glossary_templatesonavara.docx` - Original ACA Glossary

**Project Documentation:**
- `TODO.md` - Current task list (use this, not TodoWrite!)
- `DECISIONS.md` v2.2 - Includes Issue #13 TBX-Basic decision
- `README.md` - Updated with Issue #13 completion
- `PROJECT_OVERVIEW_DRAFT.md` - Project overview
- `docs/PROGRESS_UPDATES.md` - Session summaries (includes 2025-10-16 evening)
- `FUTURE_IDEAS.md` - Future plans and open questions

---

## 💡 Context & Reminders

**Why TBX-Basic matters:**
- International standard for terminology exchange (ISO 30042:2019)
- FREE and OPEN (unlike ISO 704/1087)
- Enables export to professional CAT tools (SDL Trados, MemoQ)
- Used by professional translation industry
- Supports collaboration and version tracking

**All 3 structural decisions finalized:**
- ✅ Transaction history: Full `transactions[]` array
- ✅ Status tracking: Variant C - `atl_status` + `usage_status` separately
- ✅ Component lookups: Hybrid - data in `_metadata`, reference at term level
- ✅ Additional features: usage_examples, community terms, CAT tool support

**Key insight:**
TBX-Basic provides the professional foundation we need while allowing custom ATL workflow fields. Best of both worlds - standards compliance + flexibility.

---

## 🎯 Success Criteria for Next Session

**Minimum:**
- ✅ Final JSON schema documented (`research/standards/FINAL_JSON_SCHEMA.md`)
- ✅ All minor decisions made (naming conventions, required fields, etc.)
- ✅ Changes committed and pushed

**Ideal:**
- ✅ All of minimum
- ✅ DATA_PIPELINE.md updated with Steps 2-5
- ✅ Migration strategy planned

**Stretch:**
- ✅ All of ideal
- ✅ Migration script created (`src/migrate_to_tbx_structure.py`)
- ✅ First test migration successful
- ✅ Validation working

---

**Remember:**
- Take breaks, follow ADHD-friendly principles
- Update TODO.md as you go
- Issue #13 is closed - all decisions made
- You've made excellent progress! 🎉
