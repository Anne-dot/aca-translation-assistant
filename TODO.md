# Post-Compacting Cleanup TODO

## Status Legend
- ⏳ In Progress
- ✅ Done
- ⏸️ Pending

## Tasks

### 1. ✅ Update Steps 1A and 1B in PROJECT_OVERVIEW_DRAFT.md to mark as deprecated
- Mark Step 1A (Collect EKI Terminology) as deprecated
- Mark Step 1B (Match Glossary with EKI) as deprecated
- Add references to new Sonaveeb approach (Issue #7)
- Add references to deprecation issues (#1, #3, #4)

### 2. ✅ Move deprecated EKI data files to deprecated/data/ folder
- Move `data/eki_terms/*.json` → `deprecated/data/eki_terms/`
- Move `data/eki_combined.json` → `deprecated/data/`
- Move `data/eki-terms.csv` → `deprecated/data/`
- Move `data/glossary-review.csv` → `deprecated/data/`
- Keep `data/estonian-only-terms.csv` (Issue #7 output, useful)

### 3. ✅ Move docs: PROGRESS_UPDATES.md and EXISTING_TOOLS_ANALYSIS.md to docs/
- Create `docs/` folder if needed
- Move `PROGRESS_UPDATES.md` → `docs/`
- Move `EXISTING_TOOLS_ANALYSIS.md` → `docs/`

### 4. ✅ Update DECISIONS.md with deprecated EKI info and current status
- Update "Current Status" section with Issue #7 completion
- Add deprecation notice for EKI approach
- Update with Sonaveeb approach
- Keep architectural decisions (valuable reference)

### 5. ✅ Update README.md with current project state
- Update with current workflow (Sonaveeb, not EKI)
- Add recent completions (Issues #5-#11)
- Update project structure

### 6. ✅ Decide what to do with PERSONAL_THOUGHTS.md (keep/delete/move)
- Review content
- Decision: Moved content to PROGRESS_UPDATES.md (2025-10-13 entry)
- File deleted

### 7. ⏸️ Commit all reorganization changes
- Commit after all above tasks complete
- Write descriptive commit message covering all changes
