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

#### 3. ⏸️ Map complete data pipeline: .docx → final JSON
- **Start:** ACA Glossary .docx (original WSO document)
- **End:** Final JSON with all terms + translations from all sources
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
