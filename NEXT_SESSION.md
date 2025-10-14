# Next Session - 2025-10-15

## ⚠️ FIRST: Read These Before Starting

**CRITICAL - Read every time before continuing work:**
1. `~/.claude/instructions.md` - Global non-negotiable requirements (always follow this as primary source)
2. `AI_COLLABORATION_GUIDE.md` - Project collaboration rules
3. **If this is after compacting:** Read compacting summary to get back to speed

**Important:** All work must follow `~/.claude/instructions.md` principles - 29 line limit, show TEXT first, ask open questions, NO SILENT FAILURES, ADHD-friendly code.

## Where We Left Off (2025-10-14)

**Issue #3 completed and closed:**
- ✅ Migrated codebase from Estonian to English (`eki_koguja.py` → `eki_collector.py`)
- ✅ Re-collected all 4 EKI databases with English structure
- ✅ Created `src/load_eki_data.py` - loads and combines EKI data
- ✅ Output: `data/eki_combined.json` (564 English terms, 262 Estonian-only, 1,278 total)
- ✅ Documentation updated (PROJECT_OVERVIEW_DRAFT.md, PROGRESS_UPDATES.md)

**Key decision:** English terms as dictionary keys (fast lookup, source language, supports multiple variants, scalable)

## Next Concrete Step

**Create Issue #4: Implement matching algorithm**

### What to do
1. Create new GitHub issue for Step 3 of Milestone 1B
2. Implement matching algorithm:
   - Load Glossary (845 terms from `data/aca-glossary.json`)
   - Load EKI combined data (`data/eki_combined.json`)
   - Match English → English
   - For matches: link Estonian equivalents from EKI
   - Generate statistics (matched/unmatched)
3. Output: `data/aca-glossary-eki.json` (enriched Glossary)

### Files involved
- Input: `data/aca-glossary.json` (845 Glossary terms)
- Input: `data/eki_combined.json` (1,278 EKI terms)
- Output: `data/aca-glossary-eki.json` (enriched database)
- Script: `src/match_glossary_eki.py` (to create)

### Success criteria
✅ Glossary terms matched with EKI equivalents
✅ Statistics report generated (how many matched)
✅ Ready for manual review

## After This
Issue #5: Extract from ATL existing translations (Milestone 1C)

## Important Context
- See Issue #3 for data structure details: https://github.com/Anne-dot/aca-translation-assistant/issues/3
- English terms as keys enables fast translation workflow
- Multiple Estonian variants possible (EKI + ATL + Glossary)
