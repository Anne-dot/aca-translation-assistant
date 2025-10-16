# Current Structure vs TBX-Basic Comparison

**Purpose:** Analyze how current `aca-glossary-eki.json` aligns with TBX-Basic standard

**Date:** 2025-10-16

---

## Current Data Structure

```json
{
  "metadata": {
    "created": "2025-10-15T02:45:25",
    "source_files": ["aca-glossary.json", "eki_combined.json"],
    "glossary_total": 845,
    "matched_count": 10,
    "term_complexity_added": "2025-10-15T18:13:54"
  },
  "terms": {
    "abandonment": {
      "english": "Abandonment\n(This can be...)",
      "letter": "A",
      "glossary_row": 3,
      "senses": [
        {
          "sense_id": 1,
          "match_status": "matched",
          "match_confidence": "exact",
          "domain": "psychology/therapy",
          "eki_variants": [
            {
              "estonian": "ebastabiilsus",
              "source": "eki_skt",
              "link": "https://sonaveeb.ee/...",
              "definition": "eeldus, et kõik elu jooksul..."
            }
          ],
          "synonyms": ["instability"],
          "preferred_variant": null,
          "notes": "This can be physical or emotional...",
          "part_of_speech": null,
          "term_complexity": "simple",
          "component_terms": null
        }
      ]
    }
  }
}
```

---

## TBX-Basic Required Structure

```xml
<conceptEntry id="c001">
  <descrip type="subjectField">psychology/therapy</descrip>

  <langSec xml:lang="en">
    <termSec>
      <term>abandonment</term>
      <termNote type="partOfSpeech">noun</termNote>
      <termNote type="administrativeStatus">preferredTerm-admn-sts</termNote>
      <note>This can be physical or emotional...</note>
    </termSec>
  </langSec>

  <langSec xml:lang="et">
    <termSec>
      <term>ebastabiilsus</term>
      <termNote type="partOfSpeech">noun</termNote>
      <termNote type="administrativeStatus">admittedTerm-admn-sts</termNote>
      <admin type="source">Sõnaveeb SKT</admin>
      <descrip type="definition">eeldus, et kõik elu jooksul...</descrip>
    </termSec>
  </langSec>
</conceptEntry>
```

---

## Field-by-Field Comparison

| TBX-Basic Field | Current Field | Status | Notes |
|----------------|---------------|--------|-------|
| **Concept Level** |
| `id` | Key in `terms` object | ⚠️ Partial | Using English term as key, not numeric ID |
| `subjectField` | `domain` | ✅ Present | "psychology/therapy" |
| `definition` (concept) | - | ❌ Missing | No concept-level definition |
| **Language Level** |
| `xml:lang` | - | ❌ Missing | No explicit language coding |
| EN language section | `english` field | ⚠️ Partial | Mixed with notes in string |
| ET language section | `eki_variants[]` | ⚠️ Partial | Inside source-specific array |
| **Term Level** |
| `term` | `english` / `estonian` | ⚠️ Partial | Mixed with markers like "(v.)", "(to)" |
| `partOfSpeech` | `part_of_speech` | ⚠️ Exists but null | Field exists, values not populated |
| `administrativeStatus` | `match_status` | ⚠️ Different | "matched"/"unmatched" vs TBX values |
| `definition` (term) | `definition` in `eki_variants` | ⚠️ Partial | Only in EKI variants, not structured |
| `context` | - | ❌ Missing | No usage examples separated |
| `source` | `source` in variants | ✅ Present | "eki_skt", etc. |
| `note` | `notes` | ✅ Present | Text notes exist |
| **Custom Fields** |
| - | `term_complexity` | ➕ Extra | ISO 1087 classification (good!) |
| - | `component_terms` | ➕ Extra | For complex terms (good!) |
| - | `synonyms` | ➕ Extra | EN synonyms |
| - | `letter` | ➕ Extra | Alphabetical section |
| - | `glossary_row` | ➕ Extra | Row number in original .docx |
| - | `match_confidence` | ➕ Extra | Matching quality |

---

## Key Problems

### 1. ❌ No Language Separation

**Problem:** English and Estonian are not organized by language sections

**Current:**
```json
{
  "english": "Abandonment\n(...)",
  "senses": [{
    "eki_variants": [{"estonian": "ebastabiilsus"}]
  }]
}
```

**Should be:**
```json
{
  "id": "c001",
  "languages": {
    "en": {
      "terms": [{"term": "abandonment", "partOfSpeech": "noun"}]
    },
    "et": {
      "terms": [{"term": "ebastabiilsus", "partOfSpeech": "noun", "source": "Sõnaveeb SKT"}]
    }
  }
}
```

### 2. ❌ Terms Mixed with Metadata

**Problem:** English term contains notes and markers in same string

**Current:**
```json
"english": "Abandonment\n(This can be physical or emotional abandonment...)"
```

**Should be:**
```json
{
  "term": "abandonment",
  "note": "This can be physical or emotional abandonment..."
}
```

### 3. ⚠️ Source-Centric Instead of Term-Centric

**Problem:** Estonian terms grouped by source (`eki_variants`, `sonaveeb_variants`)

**Current:**
```json
{
  "eki_variants": [
    {"estonian": "ebastabiilsus", "source": "eki_skt"}
  ],
  "sonaveeb_variants": [
    {"estonian": "hüljatus", "source": "sonaveeb_skt"}
  ]
}
```

**Should be:** All ET terms in one language section with source as metadata

```json
{
  "et": {
    "terms": [
      {
        "term": "ebastabiilsus",
        "source": "Sõnaveeb SKT",
        "administrativeStatus": "admittedTerm-admn-sts"
      },
      {
        "term": "hüljatus",
        "source": "Sõnaveeb SKT",
        "administrativeStatus": "admittedTerm-admn-sts"
      },
      {
        "term": "hülgamine",
        "source": "WSO ACA Glossary",
        "administrativeStatus": "atl_approved"
      }
    ]
  }
}
```

### 4. ❌ No `part_of_speech` Values

**Problem:** Field exists but all values are `null`

**Fix needed:** Extract from English term markers:
- "Abuse (v.)" → `part_of_speech: "verb"`
- "Abandonment" → Extract from context or mark for manual review

### 5. ⚠️ administrativeStatus Values Non-Standard

**Current values:**
- `match_status: "matched"` / `"unmatched"`
- `preferred_variant: null`

**TBX-Basic standard values:**
- `preferredTerm-admn-sts` - Use this one!
- `admittedTerm-admn-sts` - Acceptable alternative
- `deprecatedTerm-admn-sts` - Don't use
- `supersededTerm-admn-sts` - Replaced by another

**Custom values for ATL (non-standard but allowed):**
- `atl_approved` - ATL has reviewed and approved
- `atl_in_use` - Currently used in ATL päevatekstid
- `candidate` - Awaiting review
- `rejected` - Explicitly rejected

### 6. ❌ Missing Structured Definitions

**Problem:** Definitions only in EKI variants, mixed English/Estonian

**Current:**
```json
"definition": "eeldus, et kõik elu jooksul loodud tähtsad suhted katkevad... [mixed ET and EN text]"
```

**Should be:**
```json
{
  "et": {
    "definition": "eeldus, et kõik elu jooksul loodud tähtsad suhted katkevad...",
    "terms": [...]
  },
  "en": {
    "definition": "the feeling that important relationships will never last...",
    "terms": [...]
  }
}
```

---

## What Works Well ✅

### 1. Concept = Top-level Entry
- ✅ Each English term is one concept
- ✅ `senses` array handles polysemy (multiple meanings)

### 2. ISO 1087 Compliance
- ✅ `term_complexity` field (simple/complex/compound)
- ✅ `component_terms` array for complex terms

### 3. Source Tracking
- ✅ Clear source labels (`eki_skt`, `sonaveeb_har`, etc.)
- ✅ Links to original sources

### 4. Domain Classification
- ✅ `domain` field tracks subject area

### 5. Metadata
- ✅ Comprehensive metadata tracking
- ✅ Timestamps for updates

---

## Migration Strategy

### Phase 1: Structural Reorganization

**Transform:**
```
terms → conceptEntry array
  ├─ english (string) → langSec en
  │   └─ Clean term + separate notes → termSec
  └─ eki_variants/sonaveeb_variants → langSec et
      └─ Flatten all ET terms → termSec array
```

**Key changes:**
1. Create `languages` object with `en` and `et` keys
2. Move `english` field content → `languages.en.terms[0]`
3. Extract notes from English string → separate `note` field
4. Flatten all Estonian variants → `languages.et.terms[]`
5. Add `xml:lang` to each language section

### Phase 2: Field Standardization

1. **Clean terms:**
   - "Abandonment\n(...)" → term: "abandonment", note: "..."
   - "Abuse (v.)" → term: "abuse", partOfSpeech: "verb"

2. **Extract part_of_speech:**
   - Parse "(v.)", "(n.)", "(adj.)" markers
   - Use `src/term_cleaning.py` (Issue #11)

3. **Standardize administrativeStatus:**
   - Map `match_status` → appropriate TBX value
   - Add custom ATL status values

4. **Separate definitions:**
   - ET definition → `languages.et.definition`
   - EN definition → `languages.en.definition`

### Phase 3: Field Population

1. Populate `part_of_speech` from markers
2. Add `xml:lang` codes ("en", "et")
3. Set `administrativeStatus` for each term
4. Add concept-level `id` (c001, c002, ...)

---

## Recommended Final Structure

```json
{
  "metadata": {
    "created": "2025-10-16",
    "standard": "TBX-Basic v1.2.1",
    "glossary_total": 845,
    "format_version": "2.0"
  },
  "concepts": [
    {
      "id": "c001",
      "subjectField": "ACA terminology",
      "term_complexity": "simple",
      "component_terms": null,
      "languages": {
        "en": {
          "xml:lang": "en",
          "definition": null,
          "terms": [
            {
              "term": "abandonment",
              "partOfSpeech": "noun",
              "administrativeStatus": "preferredTerm-admn-sts",
              "source": "WSO ACA Glossary",
              "note": "This can be physical or emotional abandonment. Shaming a child is abandoning a child."
            }
          ]
        },
        "et": {
          "xml:lang": "et",
          "definition": "eeldus, et kõik elu jooksul loodud tähtsad suhted katkevad...",
          "terms": [
            {
              "term": "hülgamine",
              "partOfSpeech": "noun",
              "administrativeStatus": "atl_approved",
              "source": "WSO ACA Glossary",
              "note": "See võib olla füüsiline või emotsionaalne hülgamine."
            },
            {
              "term": "ebastabiilsus",
              "partOfSpeech": "noun",
              "administrativeStatus": "admittedTerm-admn-sts",
              "source": "Sõnaveeb SKT",
              "link": "https://sonaveeb.ee/search/unif/dlall/skt/ebastabiilsus"
            },
            {
              "term": "hüljatus",
              "partOfSpeech": "noun",
              "administrativeStatus": "candidate",
              "source": "Sõnaveeb SKT"
            }
          ]
        }
      }
    }
  ]
}
```

---

## Benefits of New Structure

### 1. TBX-Basic Compliant
- ✅ Three-level hierarchy (concept → language → term)
- ✅ All required fields present
- ✅ Standard field names and values
- ✅ Easy export to TBX XML

### 2. Language-First Organization
- ✅ Clear separation: English vs Estonian
- ✅ All ET terms in one place (not scattered by source)
- ✅ Language-level definitions supported

### 3. Multiple Variants Supported
- ✅ Each language can have multiple terms
- ✅ Each term has status (preferred/admitted/candidate/rejected)
- ✅ Clear which term to use (administrativeStatus)

### 4. Backward Compatible
- ✅ All existing data preserved
- ✅ ISO 1087 fields kept (term_complexity)
- ✅ Source tracking maintained
- ✅ Custom ATL status values supported

---

## Implementation Steps

### Step 1: Create Migration Script
`src/migrate_to_tbx_structure.py`

**Tasks:**
1. Load current `aca-glossary-eki.json`
2. For each term:
   - Create concept object with new structure
   - Extract clean term from English string
   - Extract notes from English string
   - Create EN language section with term
   - Flatten all ET variants into ET language section
   - Extract part_of_speech from markers
   - Set administrativeStatus values
3. Save to `data/aca-glossary-tbx.json`

### Step 2: Validation
- Check all 845 terms migrated
- Verify no data loss
- Validate against TBX-Basic schema (if available)
- Generate comparison report

### Step 3: Update Scripts
- Update all scripts to use new structure
- `sonaveeb_lookup.py` → write to new format
- `glossary_manager.py` → read/write new format

---

## Questions for Decision

1. **Naming:** Use `concepts` or `conceptEntries` for top-level array?
2. **ID format:** `c001` (numeric) or `aca_abandonment` (semantic)?
3. **Migration timing:** Now or after Sonaveeb enrichment completes?
4. **Backward compatibility:** Keep old format in parallel during transition?

---

## Summary

### Current Structure Issues:
- ❌ No language separation (EN and ET mixed)
- ❌ Terms contain metadata in strings
- ❌ Source-centric grouping (variants by source)
- ❌ `part_of_speech` unpopulated
- ❌ Non-standard status values

### Migration Priority: 🔴 High

**Why:** TBX-Basic compliance is essential for:
- Professional terminology tool compatibility
- Future TBX export capability
- Clear data organization
- ATL workflow integration

**Recommendation:** Migrate BEFORE continuing with more enrichments. Clean foundation = easier future work.

---

**Last Updated:** 2025-10-16
