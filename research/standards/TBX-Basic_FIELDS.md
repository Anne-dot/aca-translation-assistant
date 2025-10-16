# TBX-Basic Field Reference

**Purpose:** Define required and optional fields for final terminology database JSON structure

**Source:** TBX-Basic v1.2.1 (ISO 30042:2019)

---

## Three-Level Hierarchy

TBX-Basic uses a three-level structure to organize terminology data:

```
conceptEntry (one concept)
  └─ langSec (one per language)
      └─ termSec (one per term/synonym)
```

**In JSON, we map to:**
- Concept → Top-level entry object
- Language → Language-specific fields
- Term → Individual term/variant within a language

---

## 1. Concept Level (conceptEntry)

**One concept** = one entry (e.g., "abandonment" as a concept exists in multiple languages)

### Required Fields
- **id** - Unique identifier for the concept (e.g., "c001", "c002")

### Optional Fields (Highly Recommended)

#### Subject Classification
- **subjectField** - Domain/field (e.g., "psychology", "ACA terminology")

#### Definitions
- **definition** - Definition at concept level (applies to all languages)
- **source** - Source of the definition

#### Transaction Information
- **transactionType** - Type: "origination" or "modification"
- **date** - Date in YYYY-MM-DD format
- **responsibility** - Person/organization responsible

#### Cross-References
- **crossReference** - Link to related concept (internal)
- **externalCrossReference** - External URL reference
- **xGraphic** - Link to graphic/image

#### Notes
- **note** - General notes about the concept

---

## 2. Language Level (langSec)

**One langSec per language** for the same concept

### Required Fields
- **xml:lang** - Language code (e.g., "en", "et", "en-US")

### Optional Fields (Highly Recommended)

#### Language-Specific Definition
- **definition** - Definition specific to this language
- **source** - Source of the language-specific definition

#### Transaction Information
- **transactionType** - Origination/modification
- **date** - Date
- **responsibility** - Person responsible

---

## 3. Term Level (termSec)

**One termSec per term/variant** in a given language

### Required Fields
- **term** - The actual term string (e.g., "abandonment")

### Optional Fields (Highly Recommended)

#### Grammatical Information
- **partOfSpeech** - Part of speech
  - Values: `noun`, `verb`, `adjective`, `adverb`, etc.
- **grammaticalGender** - Gender (if applicable)
  - Values: `masculine`, `feminine`, `neuter`

#### Term Classification
- **termType** - Type of term
  - Values: `fullForm`, `acronym`, `abbreviation`, `shortForm`, `variant`

#### Status Information
- **administrativeStatus** - Usage status
  - `preferredTerm-admn-sts` - Preferred term (use this one!)
  - `admittedTerm-admn-sts` - Admitted/allowed term (acceptable alternative)
  - `deprecatedTerm-admn-sts` - Deprecated (don't use, but exists)
  - `supersededTerm-admn-sts` - Superseded (replaced by another term)

#### Usage Information
- **geographicalUsage** - Where term is used (e.g., "Canada", "en-US")
- **termLocation** - Where term appears (e.g., "menuItem", "radioButton")

#### Context and Examples
- **context** - Usage context / example sentence
- **source** - Source of the context

#### Administrative Information
- **customerSubset** - Customer/organization using this term
- **projectSubset** - Project where term is used
- **source** - Source of the term

#### Transaction Information
- **transactionType** - Origination/modification
- **date** - Date
- **responsibility** - Person responsible

#### Notes
- **note** - Term-specific notes

---

## Recommended Fields for ACA Translation Assistant

Based on TBX-Basic and project needs:

### Concept Level (Required)
- ✅ **id** - Unique identifier
- ✅ **subjectField** - Always "ACA terminology" or subcategories

### Language Level (Required)
- ✅ **xml:lang** - "en" and "et"

### Term Level (Required)
- ✅ **term** - The term string
- ✅ **partOfSpeech** - Essential for translation
- ✅ **administrativeStatus** - Track ATL approval status

### Term Level (Highly Recommended)
- ✅ **definition** - Definition/explanation from ACA Glossary
- ✅ **context** - Usage examples (from ACA Glossary notes)
- ✅ **source** - Track where term came from (WSO Glossary, Sõnaveeb, ATL päevatekstid, etc.)
- ✅ **termType** - Track if acronym, abbreviation, etc.
- ✅ **note** - Additional notes (e.g., from ACA Glossary parenthetical notes)

### Term Level (Optional but Useful)
- **termComplexity** - Custom field (simple, compound, complex) from ISO 1087
- **customerSubset** - "ATL" or "WSO"
- **projectSubset** - "ACA Translation Project"
- **transactionType** / **date** / **responsibility** - Version tracking

---

## Mapping ACA Glossary to TBX-Basic

### Current ACA Glossary .docx Structure

**English column:**
```
Abandonment
(This can be physical or emotional abandonment. Shaming a child is abandoning a child.)
```

**Estonian column:**
```
hülgamine

(See võib olla füüsiline või emotsionaalne hülgamine. Lapse häbistamine on lapse hülgamine.)
```

### Proposed JSON Structure (TBX-compliant)

```json
{
  "id": "c001",
  "subjectField": "ACA terminology",
  "english": {
    "xml:lang": "en",
    "terms": [
      {
        "term": "abandonment",
        "partOfSpeech": "noun",
        "administrativeStatus": "preferredTerm-admn-sts",
        "source": "WSO ACA Glossary",
        "note": "This can be physical or emotional abandonment. Shaming a child is abandoning a child.",
        "termComplexity": "simple"
      }
    ]
  },
  "estonian": {
    "xml:lang": "et",
    "terms": [
      {
        "term": "hülgamine",
        "partOfSpeech": "noun",
        "administrativeStatus": "atl_approved",
        "source": "WSO ACA Glossary",
        "note": "See võib olla füüsiline või emotsionaalne hülgamine. Lapse häbistamine on lapse hülgamine.",
        "termComplexity": "simple"
      }
    ]
  },
  "variants": {
    "estonian": [
      {
        "term": "mahajätmine",
        "partOfSpeech": "noun",
        "administrativeStatus": "admittedTerm-admn-sts",
        "source": "Sõnaveeb EKI",
        "termComplexity": "simple"
      }
    ]
  }
}
```

---

## Custom Fields for ACA Project

Beyond TBX-Basic standard, we can add custom fields:

- **termComplexity** - From ISO 1087 (simple, compound, complex)
- **atl_approved** - Custom status value for ATL-approved terms
- **atl_in_use** - Terms currently used in ATL päevatekstid
- **candidate** - Candidate translations awaiting review
- **rejected** - Terms explicitly rejected by ATL

---

## Export Capability

By following TBX-Basic structure in JSON, we can easily export to TBX XML format:

**Benefits:**
- Import into CAT tools (SDL Trados, MemoQ, etc.)
- Share with other terminology databases
- Long-term archival in standard format
- Professional terminology management tool compatibility

**Export script:** Future implementation in `src/export_to_tbx.py`

---

## Summary: Minimum Required Fields

For TBX-Basic compliance and ACA project needs:

### Concept Level
1. `id` - Unique identifier

### Language Level
2. `xml:lang` - Language code (en/et)

### Term Level
3. `term` - The term string
4. `partOfSpeech` - Grammatical info
5. `administrativeStatus` - Usage status (preferred/admitted/deprecated)
6. `source` - Where term came from

### Recommended Additions
7. `definition` or `note` - Explanation
8. `context` - Usage example
9. `termComplexity` - ISO 1087 classification

---

**Next Steps:**
1. Design final JSON schema based on these fields
2. Update data pipeline to extract and populate these fields
3. Implement validation against TBX-Basic requirements
4. Plan future TBX export functionality

---

**Last Updated:** 2025-10-16
