# Data Pipeline Documentation (DRAFT)

**Version:** 0.1
**Status:** Planning phase
**Last Updated:** 2025-10-20

---

## Purpose

Complete transformation pipeline from ACA WSO sources to TBX-Basic compliant terminology database with Estonian translations, dictionary enrichment, and manual review workflow.

**Input:** 3 source files (~500 unique terms) + dictionaries + manual additions
**Output:** Master glossary JSON (TBX-Basic v1.2.1 compliant, validated)

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────┐
│ PHASE 1: Source Consolidation & Structure              │
│ Goal: Merge 3 sources → TBX structure (EN only)        │
└─────────────────────────────────────────────────────────┘

Source 1: foundation_glossary.csv    (334 terms)
Source 2: TMS-Glossary-template.xlsx (102 unique)
Source 3: Translation-Template.docx  (62 unique)
          ↓
    STEP 1.1: Extract foundation_glossary.csv → JSON
    STEP 1.2: Extract TMS-Glossary-template.xlsx → JSON
    STEP 1.3: Extract Translation-Template.docx → JSON
          ↓
    STEP 1.4: Merge 3 JSONs → master_glossary_raw.json
              - Deduplicate (Foundation = primary)
              - Total: ~500 unique terms (498 expected)
          ↓
    STEP 1.5: Cleaning & Normalization
              - Parse "(n.)" → partOfSpeech
              - Normalize whitespace
              - Term complexity classification
          ↓
    STEP 1.6: TBX Structure Transform
              - Generate IDs (aca-0001, aca-0002, ...)
              - Create 3-level hierarchy (Concept→Language→Term)
              - Add metadata wrapper
              - Create initial transactions
          ↓
    OUTPUT: master_glossary_en_only.json (~500 terms, TBX compliant)
    VALIDATE: Against aca-tbx-terminology-schema.json

┌─────────────────────────────────────────────────────────┐
│ PHASE 2: Dictionary Enrichment (Automated)             │
│ Goal: Add dictionary translations (EN→ET)               │
└─────────────────────────────────────────────────────────┘
          ↓
    STEP 2.1: Component Term Extraction
              - Identify complex terms (termComplexity = "complex")
              - Extract component words from componentTerms array
              - Create ~150 new component concepts
              - termType (_metadata): "component"
              - derivedFrom: [parent concept IDs]
          ↓
    STEP 2.2: EN Dictionary Lookup
              - Merriam-Webster API (definitions)
              - Oxford API (definitions + examples)
              - Simple terms first → Component terms
              - Store componentLookups in parent _metadata
          ↓
    STEP 2.3: ET Dictionary Lookup
              - Sõnaveeb API (EKI databases included)
              - aare.edu.ee scraping
              - Simple → Component → Complex terms
              - Multiple ET variants per term
              - Store componentLookups.et in parent _metadata
          ↓
    OUTPUT: master_glossary_enriched.json (~648 concepts)
    VALIDATE: Against aca-tbx-terminology-schema.json

┌─────────────────────────────────────────────────────────┐
│ PHASE 3: Manual Review & Approval (Human)              │
│ Goal: ATL community review, approve translations        │
└─────────────────────────────────────────────────────────┘
          ↓
    STEP 3.1: Manual Review Workflow
              Tool: glossary_manager_via_terminal.py (Issue #20)

              For each term:
              - Review dictionary ET suggestions
              - Accept/reject/modify translations
              - Add ATL community terms
              - Mark workflow.atlStatus (candidate/atl_approved/rejected)
              - Mark workflow.usageStatus (atl_in_use/not_in_use)
              - Add usageExamples from ATL texts
              - Record transactions (who, when, what)
          ↓
    STEP 3.2: Extract from Existing ATL Translations
              Sources:
              - ATL päevamõtted (daily meditations)
              - 12 sammu tekst (12 Steps)
              - Kodulehe tõlked (website)

              For each match:
              - Add as variant with usageStatus=atl_in_use
              - Add usageExample from source
              - Link to document + date
          ↓
    STEP 3.3: Final Validation & Statistics
              - Validate against aca-tbx-terminology-schema.json
              - Generate statistics report
              - Create timestamped backup
          ↓
    OUTPUT: master_glossary_final.json
    BACKUP: master_glossary_YYYYMMDD_HHMMSS.json
```

---

## Implementation Plan

**Status:** High-level plan only. Detailed steps will be discussed and documented during implementation.

### Summary of Steps

**PHASE 1:** Extract 3 sources → Merge → Clean → TBX Transform
- Result: master_glossary_en_only.json (~500 terms, TBX compliant)

**PHASE 2:** Component extraction → EN dictionary → ET dictionary
- Result: master_glossary_enriched.json (~650 terms with translations)

**PHASE 3:** Manual review → ATL extraction → Validation
- Result: master_glossary_final.json

### Key Decisions Made

1. **Merge strategy:** Foundation = primary source, add unique terms from TMS and Template
2. **Deduplication:** Normalize terms for comparison, keep Foundation version if duplicate
3. **Component terms:** Extract BEFORE dictionary lookup
4. **Dictionary order:** Simple → Component → Complex terms
5. **Manual review:** Interactive terminal tool (Issue #20)
6. **Validation:** Against aca-tbx-terminology-schema.json at each major step


---

## Next Steps

1. Create GitHub Issue for DATA_PIPELINE implementation
2. Start with PHASE 1: Source consolidation
3. Discuss and document detailed sub-steps during implementation
4. Test each step with sample data before full run

---

**Status:** DRAFT - High-level overview only
**Note:** Detailed implementation will be planned step-by-step with user discussion
