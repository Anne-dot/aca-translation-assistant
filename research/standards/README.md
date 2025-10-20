# Standards Documentation

This folder contains international standards and specifications used for terminology database design in this project.

---

## ISO Standards (Summary)

**ISO_STANDARDS.md** - Summary of ISO 704:2022 and ISO 1087:2019 standards
- ISO standards are paid documents (not included here)
- Summary covers key principles, term classification, and application in this project
- Source: Public information from ISO website and academic papers

---

## TBX (TermBase eXchange) Specifications

TBX is ISO 30042:2019 - the international standard for representing and exchanging terminology data.

**Why TBX:**
- Free and open standard (unlike ISO 704/1087)
- Defines complete terminology database structure
- Used by professional translation and localization industry
- Enables data exchange between different terminology management systems

### Version 1 (Legacy - 2009)

**Folder:** `TBXBasic/`

**Contents:**
- `TBX_Basic_datacategoriesV23.pdf` - Original TBX-Basic specification (470KB)
- `TBX-basic-samples.tbx` - Sample terminology entries
- `TBXBasiccoreStructV02.dtd` - DTD schema
- `TBXBasicRNGV02.rng` - RNG validation schema
- `TBXBasicXCSV02.xcs` - XCS file
- Sample validation test files (bad attribute, bad element, etc.)
- `readme.txt` - Package documentation

**Source:** https://www.ttt.org/oscarStandards/tbx/TBXBasic.zip (LISA OSCAR)

**Note:** This is the original TBX-Basic from 2009. Useful for understanding the foundation, but superseded by v1.2.1.

---

### Version 1.2.1 (Current - 2023)

**Files:**
- `TBX-Basic_Definition_v1.2.1.pdf` (318KB) - Current TBX-Basic specification
- `TBX-Basic_dialect_v1.2.1.zip` (949KB) - Complete package with schemas

**Key Changes from Legacy Version:**
- Based on ISO 30042:2019 (not 2008)
- RNG schema focuses on core data model enforcement
- SCH schema handles dialect-specific constraints
- Updated for modern terminology management workflows

**Source:** https://ltac-global.github.io/TBX-Basic_dialect/
**GitHub:** https://github.com/LTAC-Global/TBX-Basic_dialect
**Maintained by:** LTAC Global

**Release Date:** February 9, 2023

---

## TBX Structure Overview

TBX uses a three-level hierarchical structure:

### 1. Concept Level (termEntry)
- Represents one concept
- Contains all languages for that concept
- ID for cross-referencing

### 2. Language Level (langSet)
- One per language
- Contains all terms in that language
- Mandatory `xml:lang` attribute

### 3. Term Level (tig)
- Individual term
- Part of speech
- Usage notes
- Definitions
- Examples
- Status information

**Example Structure:**
```xml
<termEntry id="c001">
  <langSet xml:lang="en">
    <tig>
      <term>abandonment</term>
      <termNote type="partOfSpeech">noun</termNote>
      <descrip type="definition">The act of abandoning</descrip>
    </tig>
  </langSet>
  <langSet xml:lang="et">
    <tig>
      <term>hülgamine</term>
      <termNote type="partOfSpeech">noun</termNote>
    </tig>
  </langSet>
</termEntry>
```

---

## TBX-Basic Field Reference

**TBX-Basic_FIELDS.md** - Complete field definitions for terminology database design

**Contents:**
- Required vs optional fields at each level (concept, language, term)
- All TBX-Basic data categories with explanations
- Recommended fields for ACA Translation Assistant project
- Mapping strategy: ACA Glossary → TBX-compliant JSON structure
- Custom fields for ATL workflow (atl_approved, atl_in_use, candidate, rejected)

**Purpose:** This document defines what fields must be in the final JSON structure to ensure TBX-Basic compliance and enable future export to professional terminology tools.

---

## Final JSON Schema (Issue #14 - COMPLETE)

**JSON_SCHEMA_SPECIFICATION.md** - Complete human-readable specification (2100+ lines, 73KB)

**Contents:**
- 5 complete structure examples (simple, complex, component, community, acronym)
- 52 fields across 5 hierarchy levels (Root, Concept, Language, Term, _metadata)
- Complete validation rules for each level
- 10 enum value references
- REQUIRED vs OPTIONAL quick reference table
- Issue #13 alignment (3 key decisions)
- TBX-Basic v1.2.1 compliance analysis
- Migration notes (current→new, formatVersion, Phase 2, future enhancements)

**schemas/aca-tbx-terminology-schema.json** - Machine-readable JSON Schema Draft 7 validation file

**Testing:**
- ✅ Schema syntax validated (JSON Schema Draft 7)
- ✅ Test data validated successfully
- ✅ 100% specification compliance confirmed
- ✅ TBX-Basic REQUIRED (3/3) and Highly Recommended (7/7) fields implemented

**Purpose:** Single source of truth for all field definitions. Enables machine-readable validation and professional CAT tool export.

---

## Application in This Project

**Current Format:** JSON (for git-friendliness, human readability)

**Future Capability:** Export to TBX format for:
- Sharing with professional translation tools (CAT tools)
- Testing different terminology management systems
- Collaboration with other terminology databases
- Long-term archival in standard format

**JSON → TBX Mapping:**
- Our `english` key → TBX `<term>` in English `<langSet>`
- Our `estonian` field → TBX `<term>` in Estonian `<langSet>`
- Our `part_of_speech` → TBX `<termNote type="partOfSpeech">`
- Our `term_complexity` → TBX `<termNote type="termComplexity">` (custom)
- Our `senses` array → Multiple `<tig>` elements or `<ntig>` for polysemy

---

## Online Resources

**TBX Info (Official Site):** https://www.tbxinfo.net/
- Developer resources
- Element reference (like MDN Web Docs)
- Data categories repository
- Validators and tools

**LTAC Global:** https://ltac-global.org/
- Standards maintenance organization
- TBX Version 3 stewards

**TerminOrgs:** https://www.terminorgs.net/
- Terminology organizations network
- Additional TBX resources

---

## Related Standards (Not Included)

**ISO 30042:2019** - Full TBX standard (paid, CHF ~200)
**ISO 704:2022** - Terminology work principles (paid, CHF 199)
**ISO 1087:2019** - Terminology vocabulary (paid, CHF 43)

---

**Last Updated:** 2025-10-20
