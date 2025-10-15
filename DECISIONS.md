# ACA Translation Assistant - Technical Decisions

**Note:** Active development decisions are documented in GitHub Issues during work. This file is updated periodically with strategic and architectural decisions. For current work details, see [GitHub Issues](https://github.com/Anne-dot/aca-translation-assistant/issues).

**Version:** 2.0
**Last Updated:** 2025-10-15

---

## 📋 Project Overview

**Name:** ACA Translation Assistant
**Purpose:** Build systematic terminology database and translation tools for ACA/ATL materials (English → Estonian)

**Technical Stack:**
- Language: Python 3.x
- Data Format: JSON (current), SQLite (future)
- Standards: ISO 704 lexicography standards
- Workflow: Git + GitHub Issues

**End Goal:** Gift to Estonian and global ACA/ATL communities

---

## 🎯 Current Development Status

**Milestone 1: Terminology Database** (IN PROGRESS)

- ✅ **Step 1A:** EKI terminology collected (1,278 terms) - Issue #1 ✅
- ✅ **Step 1B:** Glossary matched with EKI (10/845 matches) - Issues #4, #5, #6 ✅
- ⏳ **Next:** Manual review and validation
- 📋 **Future:** Extract from ATL existing translations (Step 1C)

**Recent Architectural Decisions:**
- **Data structure:** Dictionary with English terms as keys, senses array for homonyms (Issue #4)
- **Part of speech:** Added structured field following ISO 704 standards (Issue #6)
- **Code quality:** DRY principle - shared functions extracted to utils.py (Issue #5)

See complete roadmap: [PROJECT_OVERVIEW_DRAFT.md](PROJECT_OVERVIEW_DRAFT.md)

---

## 📐 Architectural Decisions

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

**Milestones = Development Phases (4 major milestones)**
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

**Last Updated:** 2025-10-15
