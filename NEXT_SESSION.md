# Next Session - 2025-10-17

## ⚠️ FIRST: Read These Before Starting

**CRITICAL - Read every time before continuing work:**
1. `~/.claude/instructions.md` - Global non-negotiable requirements
2. `TODO.md` - Current task list and progress

---

## Where We Left Off (2025-10-16)

### ✅ Completed This Session

**TBX-Basic Standards Research (4 hours):**
- ✅ Downloaded and analyzed TBX-Basic v1.2.1 specification (ISO 30042:2019)
- ✅ Created comprehensive field reference documentation
- ✅ Compared current JSON structure with TBX-Basic requirements
- ✅ Compared TBX-Basic standard with ATL workflow plans
- ✅ Made 2 out of 3 key structural decisions

**Documentation Created:**
- ✅ `research/standards/TBX-Basic_FIELDS.md` (318 lines) - Complete field reference
- ✅ `research/standards/STRUCTURE_COMPARISON.md` (296 lines) - Current vs TBX-Basic
- ✅ `research/standards/TBX_vs_MY_PLANS.md` (700+ lines) - TBX vs my plans with ADHD summary
- ✅ `docs/PROGRESS_UPDATES.md` - Added 2025-10-16 session entry
- ✅ `PROJECT_OVERVIEW_DRAFT.md` - Updated with TBX-Basic research
- ✅ `TODO.md` - Added documentation update tasks (#10-14)

**Key Decisions Made:**
1. ✅ **Transaction History:** Full history tracking with `transactions[]` array (collaborator wants full audit trail)
2. ✅ **Component Lookups:** Hybrid approach - data in `_metadata.component_lookups`, reference `has_components: true` at term level
3. ⏸️ **PENDING:** atl_in_use vs atl_approved - needs decision between Variant A, B, or C

---

## 🎯 Next Concrete Step

### PRIORITY 1: Make Status Tracking Decision ⚠️ BLOCKS EVERYTHING ELSE

**Decision needed:** Choose Variant A, B, or C for ATL status tracking

**Where to find info:**
- Read `research/standards/TBX_vs_MY_PLANS.md`
- Start with TL;DR (ADHD Summary) at the top
- Focus on "Otsus 2" section

**Three options:**

| Variant | Description | Complexity | Use Case |
|---------|-------------|------------|----------|
| **A** | Only `atl_approved` | 🟢 Simple | If workflow is: review → approve |
| **B** | Only `atl_in_use` | 🟢 Simple | If focus is on actual usage tracking |
| **C** | Both `atl_status` + `usage_status` | 🟡 Medium | If need to track approval AND usage separately |

**Variant C Examples (most flexible):**
- Term approved but not yet in use: `atl_approved` + `not_in_use`
- Term in use but not yet reviewed: `candidate` + `atl_in_use`
- Term rejected but still in old texts: `rejected` + `atl_in_use`
- Term approved and actively used: `atl_approved` + `atl_in_use`

**How to decide:**
1. Think about ATL workflow: Do you review first or use first?
2. Do you need to distinguish "officially approved" from "currently used"?
3. Will you have terms that are used but not yet approved? (historical terms)
4. Will you have terms that are approved but not yet in päevatekstid?

**After decision:**
- Update `research/standards/TBX_vs_MY_PLANS.md` with decision
- Update TODO.md Task #3 as complete
- Proceed to Priority 2

---

### PRIORITY 2: Design Final JSON Schema

**Once Variant A/B/C is decided:**

1. **Create JSON schema document**
   - File: `research/standards/FINAL_JSON_SCHEMA.md`
   - Based on recommended structure from TBX_vs_MY_PLANS.md
   - Include complete example with all fields
   - Document all field definitions
   - Add validation rules

2. **Update DATA_PIPELINE.md**
   - Document Steps 2-5 (currently only Step 1 exists)
   - Show transformation at each step
   - Include example data at each stage

3. **Plan migration strategy**
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
- `research/standards/TBX_vs_MY_PLANS.md` ⭐ **READ THIS FIRST** (ADHD summary at top)
- `research/standards/TBX-Basic_FIELDS.md` - All field definitions
- `research/standards/STRUCTURE_COMPARISON.md` - Current problems identified
- `research/standards/README.md` - Standards documentation index

**Current Data:**
- `data/aca-glossary-eki.json` - Current structure (needs migration)
- `data/Glossary_templatesonavara.docx` - Original ACA Glossary

**Project Documentation:**
- `TODO.md` - Current task list (use this, not TodoWrite!)
- `instructions.md` - Project-specific rules
- `PROJECT_OVERVIEW_DRAFT.md` - Project overview
- `docs/PROGRESS_UPDATES.md` - Session summaries
- `FUTURE_IDEAS.md` - Future plans and open questions

---

## 💡 Context & Reminders

**Why TBX-Basic matters:**
- International standard for terminology exchange (ISO 30042:2019)
- FREE and OPEN (unlike ISO 704/1087)
- Enables export to professional CAT tools (SDL Trados, MemoQ)
- Used by professional translation industry
- Supports collaboration and version tracking

**Current compatibility:**
- ✅ 80% of my plans align well with TBX-Basic
- ⚠️ 20% needs adjustment (mainly structure reorganization)
- ✅ All custom ATL features can be preserved
- ✅ ISO 1087 `term_complexity` field is good addition

**Key insight:**
TBX-Basic provides the professional foundation we need while allowing custom ATL workflow fields. Best of both worlds - standards compliance + flexibility.

---

## 🎯 Success Criteria for Next Session

**Minimum:**
- ✅ Decision made: Variant A, B, or C
- ✅ Final JSON schema documented
- ✅ README.md updated
- ✅ Changes committed and pushed

**Ideal:**
- ✅ All of minimum
- ✅ Migration script created
- ✅ First terms migrated successfully
- ✅ Validation working

**Stretch:**
- ✅ All of ideal
- ✅ Full migration complete (826 terms)
- ✅ Migration report generated
- ✅ Ready to continue with enrichment

---

**Remember:** Take breaks, follow ADHD-friendly principles, update TODO.md as you go. You've made excellent progress! 🎉
