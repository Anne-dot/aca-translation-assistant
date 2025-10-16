# TODO

**Purpose:** Action-oriented task list for current work
**Strategy & Ideas:** See [FUTURE_IDEAS.md](FUTURE_IDEAS.md) for background, rationale, and open questions

## Status Legend
- ⏳ In Progress
- ✅ Done
- ⏸️ Pending

---

## Next Session Tasks

### 🗂️ I. Project Housekeeping (DO FIRST!)

#### 1. ✅ Clean up and reorganize eki_analüüs/ folder
- Review contents: Sõnaveeb debugging files, HTML pages, test data
- Move Sõnaveeb research files → research/web_pages/sonaveeb/
- Move EKI archived files → research/web_pages/eki_archived/
- Delete unnecessary/duplicate files
- Remove empty eki_analüüs/ folder when done
- **Why critical:** Project folder organization affects findability and mental clarity

#### 2. ✅ Review and organize deprecated/ folder
- Verify all deprecated EKI scripts are there
- Check deprecated/data/ contents
- Ensure nothing important is missing
- Add README.md explaining what's deprecated and why
- **See:** Issues #1, #3, #4 for deprecation context

---

### 📊 II. Data Pipeline (Main Work)

#### 3. ⏳ Map complete data pipeline: .docx → final JSON
- **Start:** ACA Glossary .docx (original WSO document)
- **End:** Final JSON with all terms + translations from all sources
- **Progress:**
  - ✅ Created DATA_PIPELINE.md with Step 1 documented (.docx extraction)
  - ✅ Analyzed Glossary_templatesonavara.docx structure (3 columns, 874 rows)
  - ✅ Researched TBX-Basic standard (ISO 30042:2019) for final JSON structure
  - ✅ Downloaded TBX-Basic v1.2.1 specification and examples
  - ✅ Created TBX-Basic_FIELDS.md - complete field reference for final JSON design
  - ✅ Updated research/standards/README.md with field reference documentation
  - ✅ Created STRUCTURE_COMPARISON.md - compared current JSON with TBX-Basic
  - ✅ Created TBX_vs_MY_PLANS.md - compared TBX-Basic with my planned structure (FUTURE_IDEAS.md + GitHub issues)
  - ✅ Added ADHD-friendly summary to TBX_vs_MY_PLANS.md
  - ✅ Answered 3 key decisions:
    - ✅ Transaction history: Täielik (kogu ajalugu)
    - ⏸️ atl_in_use vs atl_approved: VAJA OTSUSTADA (Variant A, B või C?)
    - ✅ component_lookups: Hübriid (metadata + viide)
  - ⏸️ **Next:** Otsusta Variant A, B või C (atl_in_use vs atl_approved)
  - ⏸️ Design final JSON schema based on decisions
  - ⏸️ Document Steps 2-5 in DATA_PIPELINE.md
- **Map transformations:**
  - Step 1: .docx extraction → aca-glossary.json (what fields? what's preserved?)
  - Step 2: Enrichment stages (Sõnaveeb, päevatekstid, aare.edu.ee)
  - Step 3: Component terms generation (automatic)
  - Step 4: Manual additions (glossary_manager)
  - Step 5: Validation and final output
- **Document:**
  - Input/output for each stage
  - Data integrity strategy (preserve originals, versioning)
  - Which file is "source of truth" at each stage?
- **Decide:**
  - Current files: aca-glossary.json, aca-glossary-eki.json (has deprecated EKI + term_complexity)
  - Create new clean version without EKI data?
  - What is input for Sonaveeb lookup?
  - What is input for component extraction?
- **See:** PROJECT_OVERVIEW_DRAFT.md "Open Questions" #5, FUTURE_IDEAS.md "Component Terms" Open Question #1

#### 4. ⏸️ Analyze ACA Glossary .docx structure
- Open original Glossary .docx document
- Review English terms systematically
- Identify all fields and information types:
  - Grammatical markers: `(n.)`, `(v.)`, `(adj.)` → part_of_speech field?
  - Explanations: `\n(...)` → notes field structure?
  - Multi-word terms → component handling needed?
  - Any other metadata?
- Document what must be preserved vs transformed
- Create cleanup/extraction plan
- **See:** PROJECT_OVERVIEW_DRAFT.md "Open Questions" #1

---

### 🔧 III. Component Terms & Enrichment

#### 5. ⏸️ Finalize component terms extraction design
- Review FUTURE_IDEAS.md Component Terms section
- Decide on stop words approach:
  - Hard-coded list (and, if, the, of, in, at, to, a, an, ...)?
  - Minimum word length filter (e.g., <3 letters)?
  - OR: Extract all first, review manually, create list from results?
- Plan 3-part implementation (generate → review → add to glossary)
- **See:** FUTURE_IDEAS.md "Component Terms Extraction"

#### 6. ⏸️ Design enrichment sources integration
- **Sources to integrate:**
  - Sõnaveeb (already working, Issue #7)
  - Päevatekstid (ATL existing translations)
  - aare.edu.ee (educational terminology)
  - Manual additions (glossary_manager script, Issue #10)
- **For each source:**
  - Data format and structure
  - How to store in JSON (variants array? separate field?)
  - Lookup order/priority
  - Status tracking (atl_approved, atl_in_use, candidate, rejected)
- **See:** FUTURE_IDEAS.md "Variant Structure"

---

### 🔍 IV. Additional Tasks from GitHub Issues

#### 7. ⏸️ Component Term Lookup (Issue #7 comment #6)
- **Context:** 187 complex terms (22.6%) expected low match rate in Sonaveeb
- **Goal:** For complex terms with 0 results, lookup component terms individually
- **Example:** "aca counselor" → lookup "aca" and "counselor" separately
- **Data structure:** Add `component_lookups` field to store individual component results
- **Recommendation:** Implement as separate script after initial Sonaveeb enrichment completes
- **Benefit:** Increase coverage from ~35-40% to ~45-50%
- **See:** Issue #7 comment (2025-10-15T20:00:05Z)

#### 8. ⏸️ Extract Term Cleaning Functions (Issue #11)
- **Goal:** Extract reusable functions from deprecated scripts to `src/term_cleaning.py`
- **Functions needed:**
  - `extract_base_term()` - Remove `(n.)`, `(v.)`, `(to)` markers
  - `extract_notes()` - Extract explanatory text and markers
  - `clean_glossary_term()` - Combined cleaning
  - `PARENTHESES_PATTERN` - Regex constant
- **Used by:** Issue #10 (glossary_manager), Issue #8 (component lookup), future term processing
- **See:** Issue #11

#### 9. ⏸️ Interactive Glossary Manager (Issue #10)
- **Goal:** Create `src/glossary_manager_via_terminal.py` for manual term management
- **Features:**
  - Add/edit terms interactively
  - Prompts: English term, Estonian translation, status, source, notes, is_glossary_term
  - Show example at startup
  - JSON validation after changes
- **Use cases:**
  - Add core ATL terms (ACA→ATL, Adult Child→Täiskasvanud laps)
  - Update variant status (candidate → atl_approved)
  - Add translations from ATL review
- **See:** Issue #10

---

---

### 📄 V. Documentation Updates (Current Session)

#### 10. ⏳ Progress Update for 2025-10-16 Session
- ✅ Created progress update entry in docs/PROGRESS_UPDATES.md
- ✅ Documented TBX-Basic research (4 hours)
- ✅ Documented 3 key decisions (2 completed, 1 pending)
- ✅ Documented 7 achievements (#1-7)
- ✅ Added statistics and next steps

#### 11. ✅ Update Project Structure Documentation
- ✅ Update PROJECT_OVERVIEW_DRAFT.md with TBX-Basic decisions
- ✅ Document new research/standards/ structure
- ✅ Update data pipeline documentation
- ✅ Reflect current project state

#### 12. ✅ Update NEXT_SESSION.md
- ✅ Add TBX-Basic decisions context
- ✅ Add decision needed: Variant A, B, or C (atl_in_use vs atl_approved)
- ✅ Reference TBX_vs_MY_PLANS.md for details
- ✅ Update next steps priorities

#### 13. ✅ Update README.md
- ✅ Add research/standards/ folder to structure
- ✅ Update current status to reflect TBX-Basic work
- ✅ Update version number if needed
- ✅ Add TBX-Basic compliance note

#### 14. ✅ Commit Session Work
- ✅ Git status review
- ✅ Stage new files (research/standards/*.md)
- ✅ Commit with descriptive message (b134876)
- ✅ Push to GitHub

---

## Completed (2025-10-15/16 Session)

### ✅ Post-Compacting Cleanup
- Update Steps 1A and 1B in PROJECT_OVERVIEW_DRAFT.md as deprecated
- Move deprecated EKI data files to deprecated/data/
- Move docs to docs/ folder
- Update DECISIONS.md (v2.1) and README.md (v0.3.0-alpha)
- Move PERSONAL_THOUGHTS.md content to PROGRESS_UPDATES.md
- Create TODO.md and instructions.md
- Add future tasks and cross-references
- Commits: 5b7706a, 1cf29ee, 1e0e65c

### ✅ TBX-Basic Standards Research (2025-10-16 Session)
- Research TBX-Basic v1.2.1 specification
- Create TBX-Basic_FIELDS.md (318 lines)
- Create STRUCTURE_COMPARISON.md (296 lines)
- Create TBX_vs_MY_PLANS.md (700+ lines with ADHD summary)
- Extract TBX-Basic_v1.2.1/ package
- Update research/standards/README.md
- Make 2/3 key decisions (transaction history, component_lookups)
- Update TODO.md Task #3 progress
- Create progress update entry in docs/PROGRESS_UPDATES.md

### ✅ Documentation Updates (2025-10-16 Session)
- Update PROJECT_OVERVIEW_DRAFT.md with TBX-Basic research section
- Complete rewrite of NEXT_SESSION.md with clear priorities
- Update README.md with current status and TBX-Basic compliance
- Update TODO.md with documentation tasks (#10-14)
- Commit and push all session work (commit b134876)
- 39 files changed, 14,238 insertions(+), 137 deletions(-)
