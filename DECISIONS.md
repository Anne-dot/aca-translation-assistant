# ACA Translation Assistant - Technical Decisions

**Note:** Active development decisions are documented in GitHub Issues during work. This file is updated periodically with strategic and architectural decisions. For current work details, see [GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues).

**Version:** 2.4
**Last Updated:** 2026-08-22

---

## 📋 Project Overview

**Name:** ACA Translation Assistant
**Purpose:** Build systematic terminology database and translation tools for ACA/ATL materials (English → Estonian)

**Technical Stack:**
- Language: Python 3.x
- Data Format: JSON (current), SQLite (future)
- Standards: TBX-Basic v1.2.1 (ISO 30042:2019), ISO 704, ISO 1087
- Workflow: Git + GitHub Issues

**End Goal:** Gift to Estonian and global ACA/ATL communities

---

## 🎯 Current Development Status

**Milestone 1: Terminology Database** (IN PROGRESS)

- ⚠️ **Step 1A:** EKI terminology collection - DEPRECATED (Issues #1, #3, #4) - EKI databases included in Sonaveeb
- ⚠️ **Step 1B:** Glossary-EKI matching - DEPRECATED (Issues #3, #4, #5, #6) - Using Sonaveeb instead
- ✅ **New Approach:** Sonaveeb enrichment (Issue #7) - script created, tested with 10 terms
- ✅ **Issue #13:** TBX-Basic standards research - all 3 structural decisions finalized
- ✅ **Issue #14:** JSON Schema Design - 19 decisions, specification + validation schema COMPLETE
- ⏳ **Next:** Migration script, Phase 2 enrichment, Issue #20
- 📋 **Future:** Extract from ATL existing translations (Step 1C)

**Recent Completions (2025-10-20):**
- ✅ **Issue #14:** JSON Schema Design (19 decisions, spec + schema)
- ✅ **Issue #13:** TBX-Basic standards research and 3 structural decisions
- ✅ **Issue #11:** Term cleaning utilities extracted
- ✅ **Issue #9:** Signal handling fixes
- ✅ **Issue #7:** Sonaveeb lookup script + term_complexity classification
- ✅ **Issue #6:** ISO 704 compliance - part_of_speech field
- ✅ **Issue #5:** Code refactoring - DRY principle (utils.py)

**Key Architectural Changes:**
- **TBX-Basic compliance:** Final structure based on ISO 30042:2019 standard
- **JSON Schema validation:** Machine-readable validation with JSON Schema Draft 7
- **Complete specification:** 52 fields across 5 hierarchy levels documented
- **Sonaveeb approach:** Replaces EKI collection (EKI data included in Sonaveeb)
- **Term complexity:** ISO 1087 classification (simple/complex/compound)
- **Component terms:** 213 multi-word terms require component extraction

See complete roadmap: [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)

---

## 📐 Architectural Decisions

### ✅ DECISION: TBX Standards Review — 7 decisions (Issue #44)

**Date:** 2026-08-21/22
**Issue:** [#44](https://github.com/Anne-dot/aca-translation-assistant/issues/44)
**Full consolidated text:** [research/standards/TBX_M1_DECISIONS_2026-08.md](research/standards/TBX_M1_DECISIONS_2026-08.md)
**Updated specification:** [research/standards/JSON_SCHEMA_SPECIFICATION.md](research/standards/JSON_SCHEMA_SPECIFICATION.md) v2.0

The critical review of the schema against the TBX-Basic standard (NotebookLM
round 1 questions) was completed with seven decisions. Summary:

1. **M1a — Target version:** TBX-Basic **Version 4** (TerminOrgs, Nov 2025)
   replaces the v1.2.1 assumption.
2. **MUST 1 — "TBX-Basic exportable":** the claim "100% compliant" is
   replaced everywhere — the JSON is the internal master, TBX is an export
   projection; export mapping table adopted.
3. **MUST 2 — Atomic components:** component data lives only in the
   component's own concept; `componentLookups` removed from the schema.
4. **MUST 3 — Status:** `workflow` is the single source of truth; the TBX
   status is derived at export, never stored (`administrativeStatus`
   removed). Renames: `atlStatus` → `communityReviewStatus`,
   `usageStatus` → `communityTextUsage` (V4 name collision +
   organisation-neutral naming; ACA → ACAD transition noted).
5. **SHOULD 1 — Part of speech:** program/human cooperation contract with
   hard gates; enum fixed to the V4 picklist ("phrase" removed,
   `properNoun`/`other` added); census: only 17/334 entries lack raw markers.
6. **SHOULD 2 — Orthogonal axes:** structure/form/grammar are independent
   facts; `termComplexity` removed (computed, not stored).
7. **SHOULD 3 — Component sync dissolved:** nothing to synchronise in the
   reference model; `componentTerms` removed (computed, not stored).

**Common principle:** original data is guarded; derived data is computed.

**Amends earlier decisions below:** Part of Speech Field (enum), Term
Complexity Classification (field removed — the classification concept
remains, as a computed function), TBX-Basic Compliant Structure (Decision 2
reaffirmed as Variant C; Decision 3 hybrid partly reversed), Final JSON
Schema Design (Decisions 6, 10, 17, 18 amended; formatVersion → 2.0).
The affected sections below are kept for history; where they conflict with
the Issue #44 decisions, **Issue #44 wins**.

---

### ✅ DECISION: English Terms as Dictionary Keys

**Date:** 2025-10-14
**Issue:** [#3](https://github.com/Anne-dot/aca-translation-assistant/issues/3)

**Decision:**
Structure `eki_combined.json` with English terms as dictionary keys:
```json
{
  "abandonment": {
    "en_sources": [...],
    "et_matches": [...]
  }
}
```

**Rationale:**
- English is source language (ACA WSO materials)
- Fast O(1) lookup during translation workflow
- Supports multiple Estonian variants (EKI + ATL + Glossary)
- Scalable to future languages (Milestone 4)

**Output:** `data/eki_combined.json` (564 EN terms, 262 ET-only terms)

---

### ✅ DECISION: Senses Array for Homonyms

**Date:** 2025-10-15
**Issue:** [#4](https://github.com/Anne-dot/aca-translation-assistant/issues/4)

**Decision:**
Each term has `senses` array to support homonyms (e.g., "abuse" as noun vs verb):
```json
{
  "senses": [
    {
      "sense_id": 1,
      "part_of_speech": "noun",
      "match_status": "matched",
      "eki_variants": [...]
    },
    {
      "sense_id": 2,
      "part_of_speech": "verb",
      "match_status": "unmatched",
      "eki_variants": []
    }
  ]
}
```

**Rationale:**
- Most terms have 1 sense (simple case)
- Homonyms get multiple senses with different meanings
- Each sense can have different domain, variants, preferred translation
- ISO 704 compliant structure
- Extensible for manual review additions

---

### ✅ DECISION: Part of Speech Field

**Date:** 2025-10-15
**Issue:** [#6](https://github.com/Anne-dot/aca-translation-assistant/issues/6)

**Decision:**
Add structured `part_of_speech` field to all senses (not free text in notes).

**Values:** `"noun"`, `"verb"`, `"adjective"`, `"adverb"`, `null`

**Rationale:**
- ISO 704 requires structured grammatical metadata
- Machine-readable (not free text like "(n.)" in notes)
- Essential for homonym identification
- Supports future automated processing

**Implementation:** Migration script added 826 senses with `part_of_speech: null`

---

### ✅ DECISION: EKI Language Filter

**Date:** 2025-10-13

**Decision:**
- All collected terms remain in JSON files
- Glossary matching uses only Estonian + English terms
- Russian, Finnish, Latin archived for possible future use

**Rationale:**
- ATL materials are English → Estonian translation
- Need English terms (source) and Estonian equivalents (translation)
- Russian/Finnish not needed for current ATL work
- Preserve all data - may be useful in future

**Result:** 1,265 usable terms (from 1,278 total)

---

### ✅ DECISION: File Format Support (MVP Strategy)

**Date:** 2025-10-14

**MVP (V1):**
- ✅ `.docx` (Word documents)
- ✅ `.txt` (plain text)
- 📝 **PDF files** - copy content manually for now (MVP approach)

**Future (if needed):**
- 📋 `.pdf` automatic support (PyPDF2, pdfplumber, pypdf)
- 📋 OCR support for scanned documents (tesseract, pytesseract)

**Rationale:**
- MVP-first: focus on core functionality
- Manual PDF copying not a problem currently
- Add capabilities when they become necessary

---

### ✅ DECISION: GitHub Organization Structure

**Date:** 2025-10-14
**Updated:** 2026-01-12

**Milestones = Development Phases (5 milestones)**
- **M0 "Project Foundation"** - Infrastructure, coding standards, documentation, tooling (supports all milestones)
- **M1-M4** - Feature milestones (Terminology Database → CLI Tool → Community Tool → Multi-Language)
- Each milestone represents one complete development phase
- Clear, high-level goals
- Human-readable names (not codes like "phase-1")

**Issues = Specific Tasks**
- Concrete, actionable work items
- Can be assigned, tracked, closed
- Linked to milestones
- **Active decisions documented in issue comments**

**Labels = Categories**
- Group related issues together
- Examples: "code-quality", "data-structure", "documentation"
- Multiple labels per issue possible
- Flexible organization without rigid hierarchy

**Rationale:**
- Simple and clear structure
- Not over-engineered
- Easy to understand at a glance
- Follows passion project philosophy (human-readable, not corporate)
- GitHub doesn't support sub-milestones, but labels achieve similar organization

---

### ✅ DECISION: Term Complexity Classification

**Date:** 2025-10-15
**Issue:** [#7](https://github.com/Anne-dot/aca-translation-assistant/issues/7)

**Decision:**
Add `term_complexity` field following ISO 1087 standard.

**Values:** `"simple"`, `"complex"`, `"compound"`, `null`

**Rationale:**
- ISO 1087 defines three term types: simple, complex, compound
- Helps interpret Sonaveeb lookup results (complex ACA terms unlikely in standard databases)
- Machine-readable classification
- Enables component-based lookup for complex terms

**Statistics (826 terms):**
- Simple: 613 (74.2%) - single-word terms
- Complex: 187 (22.6%) - multi-word terms (e.g., "addictive thinking")
- Compound: 26 (3.1%) - hyphenated terms (e.g., "self-esteem")

**Implementation:**
- Migration script `src/add_term_complexity.py`
- Automatic classification based on spaces/hyphens
- `component_terms` array added for complex terms

---

### ✅ DECISION: TBX-Basic Compliant Structure

**Date:** 2025-10-16
**Issue:** [#13](https://github.com/Anne-dot/aca-translation-assistant/issues/13)

**Decision:**
Adopt TBX-Basic v1.2.1 (ISO 30042:2019) as foundation for final JSON structure with custom ATL workflow extensions.

**Three Key Structural Decisions:**

1. **Transaction History:** Full history tracking with `transactions[]` array
   - Rationale: Collaborator wants complete audit trail for all term changes
   - TBX-Basic compliant (`transacGrp`)

2. **Status Tracking:** Variant C - Both `atl_status` + `usage_status`
   - `atl_status`: Review decision (`candidate`, `atl_approved`, `rejected`)
   - `usage_status`: Actual usage (`not_in_use`, `atl_in_use`, `formerly_in_use`)
   - Rationale: ATL texts contain historically used terms not yet reviewed

3. **Component Lookups:** Hybrid approach
   - Data stored in `_metadata.component_lookups`
   - Reference at term level: `has_components: true`
   - Rationale: Avoids duplication, smaller JSON size

**Additional Features:**
- `usage_examples` field for translation decision documentation with context
- Community-added terms support (`is_glossary_term: false` + `derived_from: []`)
- CAT tool lemmatization approach (store base form only)
- Estonian grammatical forms handling (pragmatic: add variants only if needed)

**Benefits:**
- TBX-Basic compliant → exportable to professional CAT tools (SDL Trados, MemoQ)
- Follows international terminology management standards (ISO 30042:2019)
- Supports ATL collaborative workflow
- All custom fields preserved in `workflow` and `_metadata` groups

**Documentation:**
- `research/standards/TBX-Basic_FIELDS.md` - Complete field reference (318 lines)
- `research/standards/STRUCTURE_COMPARISON.md` - Current vs TBX-Basic (296 lines)
- `research/standards/TBX_vs_MY_PLANS.md` - TBX vs ATL workflow (700+ lines)

**Next Steps:**
- ~~Design final JSON schema based on all 3 decisions~~ ✅ Complete (Issue #14)
- Create migration script to TBX-compliant structure
- Document complete data pipeline (Steps 2-5)

---

### ✅ DECISION: Final JSON Schema Design

**Date:** 2025-10-20
**Issue:** [#14](https://github.com/Anne-dot/aca-translation-assistant/issues/14)

**Decision:**
Complete JSON schema specification with 19 decisions covering all 52 fields across 5 hierarchy levels.

**Key Decisions:**

1. **Naming Convention:** camelCase for field names, snake_case for enum values
2. **ID Format:** Concept IDs `aca-0001`, Transaction IDs `tx-0000000001`
3. **Subject Field:** All concepts use `"ACA terminology"`
4. **Three-Level Hierarchy:** Root → Concept → Language → Term (TBX-Basic compliant)
5. **Term Field:** REQUIRED, supports full forms, acronyms, variants
6. **Part of Speech:** OPTIONAL in Phase 1, REQUIRED in Phase 3
7. **Superseded Terms:** supersededBy field with concept ID reference
8. **Notes Field:** OPTIONAL, min 10 characters
9. **Source Object:** 4 REQUIRED fields (type, name, date, addedBy) + 7 OPTIONAL
10. **Workflow Object:** ATL-specific (atlStatus, usageStatus, approvedBy, approvedDate, reviewNotes)
11. **Usage Examples:** Array with source, target, reference fields
12. **Transaction History:** Full audit trail with type, actionType, target, date, responsibility
13. **Language Codes:** ISO 639-1 two-letter codes
14. **Definitions:** OPTIONAL, language-specific
15. **Metadata Wrapper:** Root-level metadata (created, standard, formatVersion, author, license)
16. **Format Versioning:** Semantic versioning (major.minor), migration rules
17. **_metadata Object:** 7 fields (termComplexity, componentTerms, isGlossaryTerm, termType, derivedFrom, addedReason, componentLookups)
18. **Conditional Requirements:** addedReason REQUIRED when termType=communityAdded
19. **Term Types:** TBX-Basic termType + _metadata.termType for workflow classification

**Deliverables:**
- `research/standards/JSON_SCHEMA_SPECIFICATION.md` - Complete human-readable specification (2100+ lines, 73KB)
- `schemas/aca-tbx-terminology-schema.json` - Machine-readable JSON Schema Draft 7 validation file

**Benefits:**
- TBX-Basic v1.2.1 (ISO 30042:2019) compliant
- Machine-readable validation ready
- Exportable to professional CAT tools (SDL Trados, MemoQ)
- Supports ATL collaborative workflow
- Single source of truth for all field definitions
- Complete testing and validation suite included

**Testing Results:**
- ✅ Schema syntax validated (JSON Schema Draft 7)
- ✅ Test data validated successfully
- ✅ 100% specification compliance confirmed
- ✅ All 52 fields, 10 enums, 4 patterns validated
- ✅ TBX-Basic REQUIRED (3/3) and Highly Recommended (7/7) fields implemented

**Next Steps:**
- Create migration script (Decision 16)
- Implement Phase 2 enrichment
- Begin Issue #20 (Manual Glossary Guide)

---

## 📊 Glossary Data Structure Documentation

**Status:** 🚧 LIVING DOCUMENT - Will be finalized after Milestone 1 completion

**Current approach:**
- All active development decisions documented in GitHub Issues (single source of truth)
- This section tracks which Issues contain what decisions
- Full synthesis after Milestone 1 when structure is stable

**Why this approach:**
- Keep documentation close to active development (avoid duplication)
- Comprehensive synthesis when phase is complete
- Issues contain full context, rationale, and discussion

### Quick Reference: Data Structure Decisions

| Field | Issue | Status | Description |
|-------|-------|--------|-------------|
| English keys | #3 | ✅ | Top-level dictionary structure |
| `senses` array | #4 | ✅ | Support for homonyms/polysemy |
| `part_of_speech` | #6 | ✅ | ISO 704 grammatical metadata |
| `term_complexity` | #7 | ✅ | ISO 1087 term classification |
| `component_terms` | #7 | ✅ | Component words for complex terms |
| TBX-Basic structure | #13 | ✅ | Three-level hierarchy (Concept→Language→Term) |
| JSON Schema | #14 | ✅ | 52 fields, 5 levels, machine-readable validation |
| `sonaveeb_variants` | #7 | 🔄 | Sonaveeb database enrichment |
| `atl_variants` | Future | ⏳ | Existing ATL translations (Step 1C) |
| `preferred_variant` | Future | ⏳ | Manual review additions |

**For current field details and examples:** See individual GitHub Issues

**After Milestone 1:** This section will expand to full data structure reference with:
- Complete field inventory
- Examples for each field
- Migration history
- Visual diagrams
- Translation workflow implications

---

## ❓ Open Questions

### Milestone 1 (Terminology Database):

1. **ATL source materials location and structure**
   - ❓ Where are original + translation files located?
   - ❓ What format (docx, txt, pairs)?
   - ❓ How organized (by date, all in one file)?

2. **Terminology database final format**
   - ❓ SQLite vs JSON vs CSV?
   - 💡 **Recommendation:** JSON (simple, readable, git-friendly) + SQLite in future

3. **Preferred variant marking**
   - ❓ When multiple Estonian equivalents exist, how to mark preferred/in-use variant?
   - ⏳ To be decided during manual review

### Milestone 2 (CLI Tool):

4. **Translation workflow**
   - ❓ Should user review all terms?
   - ❓ Or automatic replacement for approved terms?
   - 💡 **Recommendation:** Always ask user for confirmation

5. **File management**
   - ❓ How to save translated texts?
   - ❓ Preserve original and create new file?
   - ❓ Version control?

---

## 💡 Future Vision

### 🌍 Universal Translation Platform

**Vision:** Transform this ATL-specific tool into a universal, multi-language translation platform for communities worldwide.

**Long-term Goals:**

#### Multi-Language Support
- 🇬🇧 → 🇪🇪 English → Estonian (current focus)
- 🇪🇪 → 🇫🇮 Estonian → Finnish
- 🇬🇧 → 🇫🇮 English → Finnish
- 🇬🇧 → 🇸🇪 English → Swedish
- ...and other language combinations

#### Organization Management
- 📤 Upload texts to platform
- 👥 User roles (translators, reviewers, admins)
- ✅ Review workflow (translate → review → approve)
- 📊 Progress tracking

#### Collaboration Features
- 👥 Multi-translator collaboration
- 📝 Comments and discussions on terms
- 🔄 Version history
- 🔀 Translation variant comparison

#### Community-Oriented
- 🎁 Free for ACA/ATL and 12-step communities
- 🌱 Open source
- 📚 Shareable terminology databases
- 🔌 API for integration

**Why This Matters:**
- Small-language speakers have limited translation resources
- Few professional translators and terminology databases
- Machine translation worse than for large languages
- This tool could provide systematic solution

**Phased Implementation:**
- **Phase 1:** ATL-specific CLI tool ✅ (current)
- **Phase 2:** ATL-specific web version (MVP)
- **Phase 3:** User roles and review workflow
- **Phase 4:** Multi-organization support
- **Phase 5:** Multi-language support
- **Phase 6:** Open platform for all communities

---

## 📝 Notes

**Working Principles:**
- ADHD-friendly code (see `~/.claude/instructions.md`)
- MVP approach (make it work → make it right → make it fast)
- Transparent documentation
- Gift to ACA/ATL community

**Documentation Strategy:**
- Active work: GitHub Issues (single source of truth)
- Strategic decisions: This file (periodic updates)
- After closing issues: Transfer important decisions here

---

**Last Updated:** 2025-10-20
