     # Final JSON Schema - TBX-Basic Compliant Terminology Database

     **Version:** 1.0
     **Standard:** TBX-Basic v1.2.1 (ISO 30042:2019) + ACA workflow custom fields
     **Date:** 2025-10-20
     **Based on:** Issue #14 Decisions 1-19, Issue #13 structural decisions

     ---

     ## Document Overview

     This document provides the complete JSON schema specification for the ACA Translation Assistant terminology database. It consolidates all design decisions made during the
     schema development process and serves as the authoritative reference for implementation.

     The schema is built on TBX-Basic v1.2.1 (ISO 30042:2019), an international standard for terminology exchange, with carefully designed custom extensions to support the ATL
     (Alkohooliku Täiskasvanud Lapsed) collaborative translation workflow. This dual approach ensures both professional CAT tool compatibility and community-specific workflow
     support.

     The document includes comprehensive examples demonstrating different term types (simple glossary terms, complex multi-word terms, component terms, community-added terms,
     and acronyms), complete field specifications organized by hierarchy level, validation rules, and enum value references. All design decisions are traceable to their source
     decisions in Issue #14.

     ---

     ## Table of Contents

     - [1. Complete Structure Examples](#1-complete-structure-examples)
       - [1.1 Example 1: Simple Glossary Term](#11-example-1-simple-glossary-term)
       - [1.2 Example 2: Complex Term with Estonian Translation](#12-example-2-complex-term-with-estonian-translation)
       - [1.3 Example 3: Component Term](#13-example-3-component-term)
       - [1.4 Example 4: Community Added Term](#14-example-4-community-added-term)
       - [1.5 Example 5: Acronym + Full Form](#15-example-5-acronym--full-form)
     - [2. Field Reference by Level](#2-field-reference-by-level)
       - [2.1 Root Level](#21-root-level)
       - [2.2 Concept Level](#22-concept-level)
       - [2.3 Language Level](#23-language-level)
       - [2.4 Term Level](#24-term-level)
       - [2.5 _metadata Level](#25-_metadata-level)
     - [3. Validation Rules](#3-validation-rules)
     - [4. Enum Values Reference](#4-enum-values-reference)
     - [5. TBX-Basic Compliance](#5-tbx-basic-compliance)

     ---

     ## 1. Complete Structure Examples

     This section demonstrates the complete JSON structure through five examples covering different term types and scenarios.

     ### 1.1 Example 1: Simple Glossary Term

     **Term:** "abandonment" (single word, official WSO glossary term)

     **Demonstrates:**
     - Simple term (termComplexity: "simple")
     - WSO glossary term (isGlossaryTerm: true, termType: null)
     - Not derived (derivedFrom: [])
     - Minimal required fields
     - EN language section only
     - Single transaction (origination)

     ```json
     {
       "id": "aca-0001",
       "subjectField": "ACA terminology",
       "languages": {
         "en": {
           "xml:lang": "en",
           "definition": "The act of leaving someone or something behind",
           "terms": [
             {
               "term": "abandonment",
               "partOfSpeech": "noun",
               "administrativeStatus": "preferredTerm-admn-sts",
               "source": {
                 "type": "book",
                 "title": "ACA Glossary",
                 "publisher": "ACA WSO",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "originated",
                   "responsibility": "Anne Ruusmann",
                   "date": "2025-10-20"
                 }
               ]
             }
           ]
         }
       },
       "_metadata": {
         "termComplexity": "simple",
         "componentTerms": [],
         "isGlossaryTerm": true,
         "termType": null,
         "derivedFrom": []
       }
     }
     ```

     ---

     ### 1.2 Example 2: Complex Term with Estonian Translation

     **Term:** "addictive behavior" (multi-word, with ET translation and multiple variants)

     **Demonstrates:**
     - Complex term (termComplexity: "complex", componentTerms: ["addictive", "behavior"])
     - WSO glossary term
     - EN + ET language sections
     - ET with 2 variants (preferred approved, deprecated rejected)
     - workflow object (atlStatus, usageStatus, approvedBy/rejectedBy)
     - usageExamples array (Strengthening My Recovery book, date-based page ref)
     - Multiple transactions showing enrichment → approval/rejection
     - note field explaining rejection

     ```json
     {
       "id": "aca-0002",
       "subjectField": "ACA terminology",
       "languages": {
         "en": {
           "xml:lang": "en",
           "definition": "Pattern of behavior characterized by addiction",
           "terms": [{
             "term": "addictive behavior",
             "partOfSpeech": "noun",
             "administrativeStatus": "preferredTerm-admn-sts",
             "source": {
               "type": "book",
               "title": "ACA Glossary",
               "publisher": "ACA WSO",
               "addedBy": "Anne Ruusmann",
               "date": "2025-10-20"
             },
             "transactions": [{
               "type": "origination",
               "actionType": "originated",
               "responsibility": "Anne Ruusmann",
               "date": "2025-10-20"
             }]
           }]
         },
         "et": {
           "xml:lang": "et",
           "definition": "Sõltuvust iseloomustav käitumismuster",
           "terms": [
             {
               "term": "addiktiivne käitumine",
               "partOfSpeech": "noun",
               "administrativeStatus": "preferredTerm-admn-sts",
               "source": {
                 "type": "dictionary",
                 "title": "Sõnaveeb",
                 "url": "https://sonaveeb.ee/search/unif/dlall/dsall/addiktiivne",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "workflow": {
                 "atlStatus": "atl_approved",
                 "usageStatus": "atl_in_use",
                 "approvedBy": "ATL consensus",
                 "approvedDate": "2025-10-16"
               },
               "usageExamples": [{
                 "source": {
                   "type": "book",
                   "title": "Strengthening My Recovery",
                   "page": "03-15",
                   "addedBy": "Külli J",
                   "date": "2025-10-20"
                 },
                 "enContext": "We recognize our addictive behavior patterns.",
                 "etTranslation": "Me tunnistame oma addiktiivseid käitumismustreid."
               }],
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "enriched",
                   "responsibility": "Anne Ruusmann",
                   "date": "2025-10-20"
                 },
                 {
                   "type": "modification",
                   "actionType": "approved",
                   "responsibility": "ATL consensus",
                   "date": "2025-10-20",
                   "statusChange": "candidate → atl_approved"
                 }
               ]
             },
             {
               "term": "sõltuvuslik käitumine",
               "partOfSpeech": "noun",
               "administrativeStatus": "deprecatedTerm-admn-sts",
               "source": {
                 "type": "dictionary",
                 "title": "Sõnaveeb",
                 "url": "https://sonaveeb.ee/search/unif/dlall/dsall/sõltuvuslik",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "workflow": {
                 "atlStatus": "rejected",
                 "usageStatus": "not_in_use",
                 "rejectedBy": "ATL review team",
                 "rejectedDate": "2025-10-20",
                 "rejectedReason": "Too clinical, not ACA tone"
               },
               "note": "Too clinical for ACA context",
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "enriched",
                   "responsibility": "Anne Ruusmann",
                   "date": "2025-10-20"
                 },
                 {
                   "type": "modification",
                   "actionType": "rejected",
                   "responsibility": "ATL review team",
                   "date": "2025-10-20",
                   "statusChange": "candidate → rejected"
                 }
               ]
             }
           ]
         }
       },
       "_metadata": {
         "termComplexity": "complex",
         "componentTerms": ["addictive", "behavior"],
         "isGlossaryTerm": true,
         "termType": null,
         "derivedFrom": []
       }
     }
     ```

     ---

     ### 1.3 Example 3: Component Term

     **Term:** "addictive" (component derived from "addictive behavior")

     **Demonstrates:**
     - Component term (isGlossaryTerm: false, termType: "component")
     - Simple term (termComplexity: "simple", componentTerms: [])
     - derivedFrom: ["addictive behavior"] - shows parent term
     - EN + ET language sections
     - definition at language level (taken from parent's componentLookups)
     - Dictionary sources (Merriam-Webster, Sõnaveeb)
     - Single transaction (origination with actionType: "enriched")

     **Note on automatization:** When creating parent concept "addictive behavior", scripts auto-generate componentLookups (dictionary API lookups for all components). For each
      component, a separate concept is created with definition taken from parent's componentLookups. Both parent's componentLookups and component's definition are
     auto-generated. This ensures TBX-Basic compliance (every concept has definition) while maintaining Single Source of Truth (component lookup data stored once in parent).

     **Relationships:**
     - Parent → component: via componentTerms array
     - Component → parent: via derivedFrom array

     ```json
     {
       "id": "aca-0003",
       "subjectField": "ACA terminology",
       "languages": {
         "en": {
           "xml:lang": "en",
           "definition": "Causing or tending to cause addiction",
           "terms": [
             {
               "term": "addictive",
               "partOfSpeech": "adjective",
               "administrativeStatus": "preferredTerm-admn-sts",
               "source": {
                 "type": "dictionary",
                 "title": "Merriam-Webster",
                 "url": "https://www.merriam-webster.com/dictionary/addictive",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "originated",
                   "responsibility": "Anne Ruusmann",
                   "date": "2025-10-20"
                 }
               ]
             }
           ]
         },
         "et": {
           "xml:lang": "et",
           "definition": "Sõltuvust tekitav",
           "terms": [
             {
               "term": "addiktiivne",
               "partOfSpeech": "adjective",
               "administrativeStatus": "preferredTerm-admn-sts",
               "source": {
                 "type": "dictionary",
                 "title": "Sõnaveeb",
                 "url": "https://sonaveeb.ee/search/unif/dlall/dsall/addiktiivne",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "enriched",
                   "responsibility": "Anne Ruusmann",
                   "date": "2025-10-20"
                 }
               ]
             }
           ]
         }
       },
       "_metadata": {
         "termComplexity": "simple",
         "componentTerms": [],
         "isGlossaryTerm": false,
         "termType": "component",
         "derivedFrom": ["addictive behavior"]
       }
     }
     ```

     ---

     ### 1.4 Example 4: Community Added Term

     **Term:** "tervenemistee" (community-added, frequently discussed in ATL)

     **Demonstrates:**
     - Community added term (isGlossaryTerm: false, termType: "communityAdded")
     - addedReason REQUIRED (min 20 chars) - explains why term was added
     - derivedFrom: [] - not derived from other terms
     - ET language only (no EN equivalent - community-specific term)
     - source.type: "manual_addition"
     - workflow.atlStatus: "candidate" (not yet approved)
     - workflow.usageStatus: "atl_in_use" (already used in ATL texts)
     - administrativeStatus: "admittedTerm-admn-sts" (acceptable but not preferred yet)
     - User "Mari K" added (not Anne Ruusmann) - manual addition workflow
     - Needs group conscience review for approval

     ```json
     {
       "id": "aca-0004",
       "subjectField": "ACA terminology",
       "languages": {
         "et": {
           "xml:lang": "et",
           "definition": "Tervistumise ja enesearengu protsess ACA kontekstis",
           "terms": [
             {
               "term": "tervenemistee",
               "partOfSpeech": "noun",
               "administrativeStatus": "admittedTerm-admn-sts",
               "source": {
                 "type": "manual_addition",
                 "title": "ATL kogukonna ettepanek",
                 "addedBy": "Mari K",
                 "date": "2025-11-20"
               },
               "workflow": {
                 "atlStatus": "candidate",
                 "usageStatus": "atl_in_use"
               },
               "transactions": [
                 {
                   "type": "origination",
                   "actionType": "manual_addition",
                   "responsibility": "Mari K",
                   "date": "2025-11-20"
                 }
               ]
             }
           ]
         }
       },
       "_metadata": {
         "termComplexity": "simple",
         "componentTerms": [],
         "isGlossaryTerm": false,
         "termType": "communityAdded",
         "derivedFrom": [],
         "addedReason": "Kordub sageli ATL tekstides ja tekitab arutelusid tõlkimisel. Vajab kokkulepet eelistatud variandi osas."
       }
     }
     ```

     ---

     ### 1.5 Example 5: Acronym + Full Form

     **Terms:** "ACA" (acronym) + "Adult Children of Alcoholics" (full form)

     **Demonstrates:**
     - Multiple terms in same language (acronym + full form)
     - EN: "ACA" (preferredTerm) + "Adult Children of Alcoholics" (admittedTerm)
     - ET: "ATL" (preferredTerm) + "Alkohooliku Täiskasvanud Lapsed" (admittedTerm)
     - termType field (TBX-Basic standard): "acronym" vs "fullForm"
     - note field explains relationship and usage
     - Different administrativeStatus for variants (preferred vs admitted)
     - Long-standing approved terms (approvedDate: "2020-01-01")
     - Both EN and ET translations
     - All variants share same concept definition

     **Note on termType field:** TBX-Basic standard `termType` (term level, OPTIONAL) shows relationship between term variants
     (acronym/fullForm/abbreviation/shortForm/variant). This is different from `_metadata.termType` (concept level) which shows term origin category (component/communityAdded).
      Both fields can coexist - they serve different purposes.

     ```json
     {
       "id": "aca-0005",
       "subjectField": "ACA terminology",
       "languages": {
         "en": {
           "xml:lang": "en",
           "definition": "A 12-step program for adults who grew up in alcoholic or dysfunctional homes",
           "terms": [
             {
               "term": "ACA",
               "termType": "acronym",
               "partOfSpeech": "noun",
               "administrativeStatus": "preferredTerm-admn-sts",
               "note": "Acronym for 'Adult Children of Alcoholics'",
               "source": {
                 "type": "book",
                 "title": "ACA Glossary",
                 "publisher": "ACA WSO",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "transactions": [{
                 "type": "origination",
                 "actionType": "originated",
                 "responsibility": "Anne Ruusmann",
                 "date": "2025-10-20"
               }]
             },
             {
               "term": "Adult Children of Alcoholics",
               "termType": "fullForm",
               "partOfSpeech": "noun",
               "administrativeStatus": "admittedTerm-admn-sts",
               "note": "Full form, less commonly used",
               "source": {
                 "type": "book",
                 "title": "ACA Glossary",
                 "publisher": "ACA WSO",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "transactions": [{
                 "type": "origination",
                 "actionType": "originated",
                 "responsibility": "Anne Ruusmann",
                 "date": "2025-10-20"
               }]
             }
           ]
         },
         "et": {
           "xml:lang": "et",
           "definition": "12-sammuline programm täiskasvanutele, kes kasvasid üles alkohoolses või düsfunktsionaalses perekonnas",
           "terms": [
             {
               "term": "ATL",
               "termType": "acronym",
               "partOfSpeech": "noun",
               "administrativeStatus": "preferredTerm-admn-sts",
               "note": "Lühend - Alkohooliku Täiskasvanud Lapsed",
               "source": {
                 "type": "website",
                 "title": "ATL koduleht",
                 "url": "https://atl.ee",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "workflow": {
                 "atlStatus": "atl_approved",
                 "usageStatus": "atl_in_use",
                 "approvedBy": "ATL consensus",
                 "approvedDate": "2020-01-01"
               },
               "transactions": [{
                 "type": "origination",
                 "actionType": "originated",
                 "responsibility": "Anne Ruusmann",
                 "date": "2025-10-20"
               }]
             },
             {
               "term": "Alkohooliku Täiskasvanud Lapsed",
               "termType": "fullForm",
               "partOfSpeech": "noun",
               "administrativeStatus": "admittedTerm-admn-sts",
               "note": "Täisnimi, harva kasutatav",
               "source": {
                 "type": "website",
                 "title": "ATL koduleht",
                 "url": "https://atl.ee",
                 "addedBy": "Anne Ruusmann",
                 "date": "2025-10-20"
               },
               "workflow": {
                 "atlStatus": "atl_approved",
                 "usageStatus": "atl_in_use",
                 "approvedBy": "ATL consensus",
                 "approvedDate": "2020-01-01"
               },
               "transactions": [{
                 "type": "origination",
                 "actionType": "originated",
                 "responsibility": "Anne Ruusmann",
                 "date": "2025-10-20"
               }]
             }
           ]
         }
       },
       "_metadata": {
         "termComplexity": "simple",
         "componentTerms": [],
         "isGlossaryTerm": true,
         "termType": null,
         "derivedFrom": []
       }
     }
     ```

     ---

     ## 2. Field Reference by Level

     This section provides detailed specifications for all fields organized by hierarchy level.

     **Hierarchy:**
     ```
     Root Level (JSON file wrapper)
       └─ metadata (file-level information)
       └─ concepts[] (array of terminology entries)
           └─ Concept Level (one concept = one entry)
               └─ Language Level (one per language: en, et, etc.)
                   └─ Term Level (one per term/variant)
     ```

     ### 2.1 Root Level

     **Fields:** `metadata` (REQUIRED), `concepts` (REQUIRED)

     **Decision:** 15, 16

     ---

     #### Field: `metadata` (REQUIRED object)

     File-level metadata about the terminology database.

     **Subfields:**

     **`created`** (REQUIRED, auto-generated)
     - Type: String (ISO date YYYY-MM-DD)
     - Auto-generated by migration script
     - Example: `"2025-10-20"`

     **`standard`** (REQUIRED, fixed value)
     - Type: String
     - Value: `"TBX-Basic v1.2.1 + ACA workflow custom fields"`
     - Documents TBX-Basic compliance + custom extensions
     - Custom extensions: `workflow`, `_metadata`, `usageExamples`, `actionType`

     **`formatVersion`** (REQUIRED, auto-generated)
     - Type: String (semantic versioning)
     - Initial value: `"1.0"`
     - Version rules:
       - Minor (1.0 → 1.1): Backward compatible change (new OPTIONAL field added)
       - Major (1.0 → 2.0): BREAKING change (REQUIRED field changed/removed, structure changed)

     **`author`** (REQUIRED)
     - Type: String
     - Value: `"Anne Ruusmann"`
     - Credit for database creation and curation

     **`project`** (OPTIONAL)
     - Type: String
     - Value: `"ACA Translation Assistant"`
     - Documents project context

     **`license`** (REQUIRED)
     - Type: String
     - Value: `"CC BY-SA 4.0"`
     - Creative Commons Attribution-ShareAlike 4.0 International
     - Rationale: Free to use (including commercial - ACA WSO can use in published books), modifications must be shared, author gets credit

     ---

     #### Field: `concepts` (REQUIRED array)

     Array of all concept entries. Must contain at least one concept.

     **Example:**
     ```json
     {
       "concepts": [
         { "id": "aca-0001", ... },
         { "id": "aca-0002", ... }
       ]
     }
     ```

     ---

     ### 2.2 Concept Level

     **One concept** = one terminology entry (e.g., "abandonment" exists in multiple languages)

     **Fields:** `id`, `subjectField`, `languages`, `_metadata`

     **Decision:** 2, 3, 4, 17

     ---

     #### Field: `id` (REQUIRED, auto-generated)

     Unique identifier for the concept.

     **Decision:** 2

     - Type: String
     - Format: `"aca-"` + zero-padded 4-digit number
     - Examples: `"aca-0001"`, `"aca-0002"`, `"aca-0498"`
     - Range: aca-0001 to aca-9999
     - Auto-generated: Scripts find max ID + 1
     - Used for: Cross-references, database queries, component term links
     - Rationale: "aca-" prefix is future-proof for Milestone 4 (multi-language platform) - no migration needed

     ---

     #### Field: `subjectField` (REQUIRED)

     Domain/subject area of the terminology.

     **Decision:** 3 (REVISED)

     - Type: String
     - Current value for all terms: `"ACA terminology"`
     - Purpose: TBX-Basic domain classification (NOT term type categorization)
     - Future flexibility: Could support `"ATL Estonian specific"`, `"Recovery terminology"`

     **Note:** Term categories (glossary/component/community) tracked in `_metadata.isGlossaryTerm` and `_metadata.termType`, NOT in subjectField.

     ---

     #### Field: `languages` (REQUIRED object)

     Container for all language-specific data.

     **Decision:** 4

     - Type: Object
     - Keys: ISO 639-1 language codes ("en", "et") OR ISO 639-1 + country ("en-US", "et-EE")
     - EN language section REQUIRED (must always exist)
     - ET and other languages OPTIONAL (filled during enrichment)

     **Rationale:**
     - EN→ET translation project - English is always source language
     - Gradual enrichment workflow: start with EN, add ET later
     - Future: multi-language support (Milestone 4)

     **Example:**
     ```json
     {
       "languages": {
         "en": { "xml:lang": "en", ... },
         "et": { "xml:lang": "et", ... }
       }
     }
     ```

     ---

     #### Field: `_metadata` (REQUIRED object)

     Custom extension for term complexity, categorization, and component lookups.

     **Decision:** 17 (Parts 1-4)

     **Subfields:**
     - `termComplexity` (REQUIRED, auto)
     - `componentTerms` (OPTIONAL, auto)
     - `isGlossaryTerm` (REQUIRED, auto)
     - `termType` (CONDITIONAL)
     - `derivedFrom` (REQUIRED)
     - `addedReason` (CONDITIONAL)
     - `componentLookups` (OPTIONAL)

     **Note:** Underscore prefix marks this as custom extension (not TBX-Basic standard).

     **Details:** See Section 2.5 (_metadata Level) for complete field specifications.

     ---

     ### 2.3 Language Level

     **One language section per language** within the same concept.

     **Fields:** `xml:lang`, `definition`, `terms`

     **Decision:** 13, 14

     **Key concept:** Concept is based on English (source language). Each language section contains translations of the concept. Language code format: ISO 639-1 ("en", "et") OR
      ISO 639-1 + country ("en-US", "et-EE").

     ---

     #### Field: `xml:lang` (REQUIRED)

     TBX-Basic standard language identifier.

     **Decision:** 13

     - Type: String (ISO 639-1 language code)
     - Must match the key in `languages` object
     - Examples: `"en"`, `"et"`, `"en-US"`, `"et-EE"`
     - Current usage: Simple codes (`"en"`, `"et"`)
     - Future (Milestone 4): Language variants (`"en-US"`, `"en-GB"`)

     **Rationale:**
     - TBX-Basic standard requires it (mandatory field at langSec level)
     - Needed for TBX XML export (`<langSec xml:lang="en">`)
     - Supports language variants without changing structure
     - Key ("en", "et") provides JSON structure, `xml:lang` provides TBX-Basic compliance (separation of concerns)

     **Example:**
     ```json
     {
       "languages": {
         "en": {
           "xml:lang": "en",
           "terms": [...]
         }
       }
     }
     ```

     **Validation:**
     ```python
     for lang_code, lang_data in concept["languages"].items():
         assert "xml:lang" in lang_data
         assert lang_data["xml:lang"] == lang_code  # Must match key
     ```

     ---

     #### Field: `definition` (OPTIONAL)

     Language-specific definition of the concept.

     **Decision:** 14

     - Type: String
     - Each language can have different definition
     - Not all terms have definitions initially
     - Can be added during enrichment

     **Why language-specific:**
     - Translator needs to read definition in their language
     - Cultural context may require different explanations
     - EN definition describes the source concept, ET definition helps translator understand

     **Example:**
     ```json
     {
       "en": {
         "definition": "Pattern of behavior characterized by addiction"
       },
       "et": {
         "definition": "Sõltuvust iseloomustav käitumismuster"
       }
     }
     ```

     ---

     #### Field: `terms` (REQUIRED array)

     Array of term variants in this language.

     **Decision:** 4, 5

     - Type: Array of term objects
     - Must contain at least one term
     - Multiple variants possible (preferred, admitted, deprecated)

     **Example:**
     ```json
     {
       "terms": [
         { "term": "ACA", "administrativeStatus": "preferredTerm-admn-sts" },
         { "term": "Adult Children of Alcoholics", "administrativeStatus": "admittedTerm-admn-sts" }
       ]
     }
     ```

     ---

     ### 2.4 Term Level

     **One term object per term/variant** in a given language.

     **REQUIRED fields:** `term`, `administrativeStatus`, `source`, `transactions`

     **OPTIONAL fields:** `termType` (TBX-Basic), `partOfSpeech`, `supersededBy`, `note`, `workflow`, `usageExamples`

     **Decision:** 5, 6, 7, 8, 9, 10, 11, 12, 19

     ---

     #### Field: `term` (REQUIRED)

     The actual term text.

     **Decision:** 5

     - Type: String
     - Cannot be empty
     - Primary data point
     - Examples: `"abandonment"`, `"hülgamine"`

     ---

     #### Field: `termType` (OPTIONAL, TBX-Basic standard)

     Type of term variant (acronym, abbreviation, full form, etc.).

     **Decision:** 19

     - Type: String (enum)
     - Allowed values (TBX-Basic standard):
       - `"fullForm"` - Full expanded form
       - `"acronym"` - Acronym (e.g., "ACA")
       - `"abbreviation"` - Abbreviation (e.g., "Dr." for "Doctor")
       - `"shortForm"` - Short form (e.g., "phone" for "telephone")
       - `"variant"` - Spelling variant

     **Purpose:** Show relationship between term variants (acronym/fullForm pairs, abbreviations, etc.)

     **Note:** This is TBX-Basic standard `termType` (term level). Different from `_metadata.termType` (concept level) which shows term origin category
     (component/communityAdded). Both fields can coexist - they serve different purposes.

     **Example:**
     ```json
     {
       "term": "ACA",
       "termType": "acronym",
       "note": "Acronym for 'Adult Children of Alcoholics'"
     }
     ```

     ---

     #### Field: `partOfSpeech` (OPTIONAL initially, REQUIRED later)

     Part of speech / grammatical category.

     **Decision:** 6

     - Type: String (enum) or null
     - Allowed values: `"noun"`, `"verb"`, `"adjective"`, `"adverb"`, `"phrase"`, `null`
     - **Phase 1 (current):** OPTIONAL - `null` is valid (incomplete data initially)
     - **Phase 2:** Fill via script extraction and manual review
     - **Phase 3:** Becomes REQUIRED (migration after all terms filled)

     **Rationale:**
     - Reality: Many Glossary .docx terms lack part-of-speech markers
     - Non-blocking: Can extract all terms immediately
     - Systematic: Clear path to complete data (separate issue for enrichment)
     - Professional: Eventually meets ISO 704 standards

     **Example:**
     ```json
     {
       "term": "abandonment",
       "partOfSpeech": "noun"
     }
     ```

     ---

     #### Field: `administrativeStatus` (REQUIRED)

     Usage status (TBX-Basic standard).

     **Decision:** 10

     - Type: String (enum)
     - TBX-Basic standard values:
       - `"preferredTerm-admn-sts"` - Preferred term (USE this)
       - `"admittedTerm-admn-sts"` - Admitted term (acceptable alternative)
       - `"deprecatedTerm-admn-sts"` - Deprecated term (don't use)
       - `"supersededTerm-admn-sts"` - Superseded term (replaced by another)

     **Mapping from ATL to TBX:**
     - `atl_approved` → `"preferredTerm-admn-sts"`
     - `candidate` (in use) → `"admittedTerm-admn-sts"`
     - `candidate` (not in use) → `"admittedTerm-admn-sts"`
     - `rejected` → `"deprecatedTerm-admn-sts"`

     **Example:**
     ```json
     {
       "term": "abandonment",
       "administrativeStatus": "preferredTerm-admn-sts"
     }
     ```

     ---

     #### Field: `supersededBy` (OPTIONAL)

     Explicit term replacement link.

     **Decision:** 7

     - Type: String (term text within same concept) or null
     - References: Term text in same language, same concept (NOT concept ID, NOT term in other concept)
     - When to use: Only when `administrativeStatus` is `"supersededTerm-admn-sts"`

     **Rationale:** For concepts with many terms (5+), explicit link is essential. Example: "ACA" → "ACAD" (which term replaces it?).

     **Example:**
     ```json
     {
       "term": "ACA",
       "administrativeStatus": "supersededTerm-admn-sts",
       "supersededBy": "ACAD"
     }
     ```

     **Validation:**
     ```python
     if term.get("supersededBy"):
         assert term["administrativeStatus"] == "supersededTerm-admn-sts"
         # supersededBy must reference existing term in same language
         assert any(t["term"] == term["supersededBy"] for t in language_terms)
     ```

     ---

     #### Field: `note` (OPTIONAL)

     Explanatory notes.

     **Decision:** 8

     - Type: String or null
     - Use cases:
       - WSO usage preferences: "WSO prefers this over 'desertion'"
       - Context clarification: "Use in family context only"
       - Translation notes: "Avoid literal translation"
       - Relationship explanation: "Acronym for 'Adult Children of Alcoholics'"
       - Rejection reason: "Too clinical for ACA context"

     **Example:**
     ```json
     {
       "term": "abandonment",
       "note": "WSO literature uses this term consistently"
     }
     ```

     ---

     #### Field: `source` (REQUIRED object)

     Source provenance and metadata.

     **Decision:** 9 + Decision 9 Supplement

     - Type: Object with 4 REQUIRED fields + 7 OPTIONAL fields

     **REQUIRED fields:**

     **`type`** (REQUIRED) - Source type enum:
     - `"book"` - Published books, manuals, guidebooks
     - `"dictionary"` - Online/offline dictionaries (Sõnaveeb, etc)
     - `"website"` - Web resources
     - `"manual_addition"` - User-added terms
     - `"conference"` - Conference materials
     - `"transcription"` - Meeting transcriptions

     **`title`** (REQUIRED) - Source name/title:
     - Book: "Loving Parent Guidebook", "ACA Glossary"
     - Dictionary: "Sõnaveeb"
     - Website: "ACA WSO Official Site"
     - Manual: User's name or "Manual entry"

     **`addedBy`** (REQUIRED, auto-generated):
     - Current: "Anne Ruusmann" (logged-in user)
     - Future: Logged-in username
     - Ensures accountability and traceability

     **`date`** (REQUIRED, auto-generated):
     - ISO format: "2025-10-15"
     - Generated automatically by script when term added
     - Captures exact timestamp of addition

     **OPTIONAL fields:**

     **`chapter`** (OPTIONAL) - Chapter number or name (books)
     - Example: "3", "Chapter 3", "Introduction"

     **`page`** (OPTIONAL) - Page number or chapter reference (books)
     - Example: "42", "Chapter 3, p. 15"
     - For daily meditation books: meditation date "MM-DD" (e.g., "03-15")

     **`edition`** (OPTIONAL) - Edition information (books)
     - Example: "2nd edition", "Revised edition"

     **`isbn`** (OPTIONAL) - ISBN code (books)
     - Example: "978-0-9773793-0-5"

     **`publisher`** (OPTIONAL) - Publisher name (books)
     - Example: "ACA WSO", "Penguin Books"

     **`url`** (OPTIONAL) - Source URL (websites/dictionaries)
     - Example: "https://sonaveeb.ee/search/unif/dlall/dsall/hülgamine/1"
     - Auto for scripts (Sõnaveeb lookup), manual otherwise

     **`note`** (OPTIONAL) - Additional context
     - Example: "First result match", "Manual review approved"

     **Examples:**

     Book with page reference:
     ```json
     {
       "source": {
         "type": "book",
         "title": "Loving Parent Guidebook",
         "page": "42",
         "publisher": "ACA WSO",
         "addedBy": "Anne Ruusmann",
         "date": "2025-10-15"
       }
     }
     ```

     Dictionary lookup:
     ```json
     {
       "source": {
         "type": "dictionary",
         "title": "Sõnaveeb",
         "url": "https://sonaveeb.ee/search/unif/dlall/dsall/hülgamine/1",
         "addedBy": "Anne Ruusmann",
         "date": "2025-10-15"
       }
     }
     ```

     ---

     #### Field: `workflow` (OPTIONAL object)

     ATL custom workflow tracking.

     **Decision:** 10

     **Purpose:** Track ATL-specific review decisions and usage status. Hybrid approach: TBX-Basic `administrativeStatus` + custom `workflow` object work in parallel.

     **Subfields:**

     **`atlStatus`** (OPTIONAL, enum):
     - `"candidate"` - Not yet reviewed
     - `"atl_approved"` - Review team approved
     - `"rejected"` - Review team rejected

     **`usageStatus`** (OPTIONAL, enum):
     - `"not_in_use"` - Not used in ATL texts
     - `"atl_in_use"` - Currently used in ATL päevatekstid
     - `"formerly_in_use"` - Previously used, no longer

     **Conditional required fields:**

     IF `atlStatus = "atl_approved"`:
     - `approvedBy` (REQUIRED) - Who approved
     - `approvedDate` (REQUIRED) - When approved (ISO date)

     IF `atlStatus = "rejected"`:
     - `rejectedBy` (REQUIRED) - Who rejected
     - `rejectedDate` (REQUIRED) - When rejected (ISO date)
     - `rejectedReason` (OPTIONAL) - Why rejected

     IF `usageStatus = "atl_in_use"` OR `"formerly_in_use"`:
     - `firstUsedDate` (OPTIONAL) - When first used in ATL texts (ISO date)

     **Rationale:** ATL texts have historical terms not yet reviewed. Need to distinguish "de facto" (in use) vs "de jure" (approved). Variant C (both atlStatus + usageStatus)
     provides maximum information.

     **Example - Approved and in use:**
     ```json
     {
       "workflow": {
         "atlStatus": "atl_approved",
         "usageStatus": "atl_in_use",
         "approvedBy": "ATL consensus",
         "approvedDate": "2025-10-16",
         "firstUsedDate": "2025-10-16"
       }
     }
     ```

     **Example - Rejected:**
     ```json
     {
       "workflow": {
         "atlStatus": "rejected",
         "usageStatus": "not_in_use",
         "rejectedBy": "ATL review team",
         "rejectedDate": "2025-10-20",
         "rejectedReason": "Too clinical, not ACA tone"
       }
     }
     ```

     ---

     #### Field: `usageExamples` (OPTIONAL array)

     Usage examples from ATL texts.

     **Decision:** 11

     **Purpose:** Show term translations in context from actual ATL materials. Documents translation decisions and preserves institutional knowledge.

     **Array of usage example objects:**

     **Per usage example object:**

     **`source`** (REQUIRED object) - Same structure as Decision 9 source object. Allowed sources: ONLY WSO materials (Daily Meditations, Strengthening My Recovery, Loving
     Parent Guidebook, etc).

     **`enContext`** (REQUIRED string) - English context sentence showing term usage.

     **`etTranslation`** (REQUIRED string) - Estonian translation of the context.

     **`translatorNote`** (OPTIONAL object) - Translation decision documentation:
     - `author` (OPTIONAL) - Translator's name (auto-filled if logged-in user adds, omitted if unknown)
     - `date` (OPTIONAL) - When translated (auto-filled if logged-in user adds, omitted if unknown)
     - `explanation` (OPTIONAL) - Why this translation variant was chosen (free text)
     - `keyInsight` (OPTIONAL) - Main lesson or important note about translation (free text)

     **Example:**
     ```json
     {
       "usageExamples": [{
         "source": {
           "type": "book",
           "title": "Strengthening My Recovery",
           "page": "03-15",
           "addedBy": "Külli J",
           "date": "2025-10-20"
         },
         "enContext": "We recognize our addictive behavior patterns.",
         "etTranslation": "Me tunnistame oma addiktiivseid käitumismustreid.",
         "translatorNote": {
           "author": "Külli J",
           "date": "2025-10-18",
           "explanation": "Kasutasin 'addiktiivne' mitte 'sõltuvuslik', sest otsesem.",
           "keyInsight": "ATL kontekstis oluline säilitada isiklik toon."
         }
       }]
     }
     ```

     ---

     #### Field: `transactions` (REQUIRED array)

     Complete transaction history.

     **Decision:** 12

     **Purpose:** Full audit trail from start. Every term originates from somewhere (WSO Glossary minimum), so at least 1 transaction always exists.

     **Minimum:** 1 transaction (origination)

     **Per transaction object:**

     **`type`** (REQUIRED enum) - TBX-Basic standard transaction types:
     - `"origination"` - First creation of term
     - `"modification"` - Any subsequent change

     **`actionType`** (REQUIRED enum) - Categorizes action for statistics and filtering:
     - `"originated"` - Added from WSO Glossary
     - `"enriched"` - Added from enrichment source (Sõnaveeb, aare.edu.ee, etc)
     - `"approved"` - ATL approved
     - `"rejected"` - ATL rejected
     - `"modified"` - Other modification
     - `"manual_addition"` - Manually added by user

     **Why enum:** Enables statistics (250 approved, 45 rejected, etc), reliable filtering, progress tracking (ADHD-friendly - see numbers grow).

     **`responsibility`** (REQUIRED) - Who performed the action:
     - Examples: "Anne Ruusmann" (person), "ATL review team" (group), "System" (automated), "ATL consensus" (group decision)

     **`date`** (REQUIRED, auto-generated) - ISO format: "2025-10-15"

     **`actionDescription`** (OPTIONAL free text) - Detailed description of what happened:
     - Examples: "Added from WSO Glossary", "ATL consensus approved after review", "Rejected - too clinical tone"

     **`statusChange`** (OPTIONAL) - Documents status transitions. Format: "old_status → new_status"
     - Examples: "candidate → atl_approved", "not_in_use → atl_in_use"

     **Rationale - Hybrid approach:** Using BOTH `actionType` (enum) + `actionDescription` (free text) enables statistics (filter/count by actionType) while preserving context 
     (actionDescription details). ADHD-friendly progress tracking. Programmatic migration possible.

     **Example - Initial term:**
     ```json
     {
       "transactions": [
         {
           "type": "origination",
           "actionType": "originated",
           "actionDescription": "Added from WSO Glossary",
           "responsibility": "Anne Ruusmann",
           "date": "2025-10-12"
         }
       ]
     }
     ```

     **Example - Enriched then approved:**
     ```json
     {
       "transactions": [
         {
           "type": "origination",
           "actionType": "originated",
           "responsibility": "Anne Ruusmann",
           "date": "2025-10-12"
         },
         {
           "type": "modification",
           "actionType": "enriched",
           "actionDescription": "Found in Sõnaveeb lookup",
           "responsibility": "Anne Ruusmann",
           "date": "2025-10-15"
         },
         {
           "type": "modification",
           "actionType": "approved",
           "actionDescription": "ATL consensus approved as preferred term",
           "responsibility": "ATL review team",
           "date": "2025-10-16",
           "statusChange": "candidate → atl_approved"
         }
       ]
     }
     ```

     ---

     ### 2.5 _metadata Level

     **Custom extension object** for term complexity, categorization, and component lookups.

     **Decision:** 17 (Parts 1-4)

     **Fields:** `termComplexity`, `componentTerms`, `isGlossaryTerm`, `termType`, `derivedFrom`, `addedReason`, `componentLookups`

     ---

     #### Field: `termComplexity` (REQUIRED, auto-generated)

     Structural complexity classification (ISO 1087 based).

     **Decision:** 17 Part 1

     - Type: String (enum)
     - Allowed values:
       - `"simple"` - Single word term
       - `"complex"` - Multi-word term (phrase, compound)

     **Auto-generation logic:**
     1. Count words in term (split by whitespace)
     2. Remove parenthetical content first: "abuse (n.)" → "abuse"
     3. If 1 word → "simple"
     4. If 2+ words → "complex"

     **Examples:**
     - "abandonment" → "simple"
     - "blameless inventory" → "complex"
     - "at ease" → "complex"

     ---

     #### Field: `componentTerms` (OPTIONAL, auto-generated)

     Array of component words (for complex terms).

     **Decision:** 17 Part 1

     - Type: Array of strings (lowercase)
     - When filled: Only when `termComplexity = "complex"`

     **Auto-generation logic:**
     1. Split term by whitespace
     2. Convert to lowercase
     3. Keep ALL words (including "at", "of", etc. - no stop-words filtering)

     **Examples:**
     - "blameless inventory" → `["blameless", "inventory"]`
     - "at ease" → `["at", "ease"]`
     - "adult children of alcoholics" → `["adult", "children", "of", "alcoholics"]`
     - "abandonment" → `[]` (simple term)

     **Component terms workflow:**
     1. Extract term: "blameless inventory"
     2. Auto-generate: `termComplexity: "complex"`, `componentTerms: ["blameless", "inventory"]`
     3. Create separate concepts for "blameless" (aca-0002) and "inventory" (aca-0003)
     4. Mark them: `isGlossaryTerm: false`, `derivedFrom: ["blameless inventory"]`, `termType: "component"`

     ---

     #### Field: `isGlossaryTerm` (REQUIRED, auto-generated)

     Distinguish official WSO glossary terms from other terms.

     **Decision:** 17 Part 2

     - Type: Boolean
     - Auto-generation:
       - Glossary.docx import → `true`
       - Component generation → `false`
       - User manual addition → User choice (interactive prompt)

     **Examples:**
     ```json
     // WSO official glossary term
     {
       "isGlossaryTerm": true
     }

     // Component term
     {
       "isGlossaryTerm": false
     }
     ```

     ---

     #### Field: `termType` (CONDITIONAL REQUIRED, auto/manual)

     Term origin category.

     **Decision:** 17 Part 2

     - Type: String (enum) or null
     - Allowed values:
       - `"component"` - Derived from glossary term (auto-generated from componentTerms)
       - `"communityAdded"` - Added by community/user (manual addition)
       - `null` - When `isGlossaryTerm = true`

     **Logic:**
     ```python
     if isGlossaryTerm == True:
         termType = null
     else:
         termType = "component" OR "communityAdded"  # REQUIRED
     ```

     **Note:** This is `_metadata.termType` (concept level, term origin). Different from TBX-Basic `termType` (term level, acronym/fullForm). Both can coexist - different
     purposes.

     **Examples:**
     ```json
     // WSO glossary term
     {
       "isGlossaryTerm": true,
       "termType": null
     }

     // Component term
     {
       "isGlossaryTerm": false,
       "termType": "component"
     }

     // Community term
     {
       "isGlossaryTerm": false,
       "termType": "communityAdded"
     }
     ```

     ---

     #### Field: `derivedFrom` (REQUIRED)

     Track which glossary terms this term was derived from.

     **Decision:** 17 Part 3

     - Type: Array of strings (term texts, NOT concept IDs)
     - Purpose: Document parent terms when this is a component or derived term

     **Why term texts (not IDs):**
     - Human-readable
     - Self-documenting (can see relationship without lookup)
     - Easier manual editing
     - Similar to Decision 7 (`supersededBy` uses term text)

     **Auto-generation logic:**

     WSO glossary terms (not derived):
     ```python
     concept["_metadata"]["derivedFrom"] = []
     ```

     Component terms (derived from parent):
     ```python
     # Can have MULTIPLE parents if component appears in multiple terms
     if term in parent_terms:
         concept["_metadata"]["derivedFrom"] = parent_terms
     ```

     Community terms (not derived):
     ```python
     concept["_metadata"]["derivedFrom"] = []
     ```

     **Examples:**

     WSO glossary term:
     ```json
     {
       "term": "blameless inventory",
       "derivedFrom": []
     }
     ```

     Component term (one parent):
     ```json
     {
       "term": "blameless",
       "derivedFrom": ["blameless inventory"]
     }
     ```

     Component term (multiple parents):
     ```json
     {
       "term": "addictive",
       "derivedFrom": ["addictive behavior", "addictive thinking"]
     }
     ```

     **Validation:**
     ```python
     assert "derivedFrom" in concept["_metadata"]
     assert isinstance(concept["_metadata"]["derivedFrom"], list)

     # Component terms must have parent
     if concept["_metadata"]["termType"] == "component":
         assert len(concept["_metadata"]["derivedFrom"]) >= 1
     else:
         # Glossary and community terms should have empty array
         assert concept["_metadata"]["derivedFrom"] == []
     ```

     ---

     #### Field: `addedReason` (CONDITIONAL REQUIRED)

     Explanation why community term was added.

     **Decision:** 17 Part 2

     - Type: String (free text) or null
     - Minimum length: 20 characters (substantive explanation required)

     **Logic:**
     ```python
     if termType == "communityAdded":
         addedReason = REQUIRED (min 20 chars)
     else:
         addedReason = null or omitted
     ```

     **Purpose:**
     - Documents WHY term was added
     - Enables group conscience evaluation
     - Helps decide whether to keep or remove term
     - Provides context for future reviewers

     **Example:**
     ```json
     {
       "termType": "communityAdded",
       "addedReason": "Kordub sageli ATL tekstides ja tekitab arutelusid tõlkimisel"
     }
     ```

     ---

     #### Field: `componentLookups` (OPTIONAL)

     Store component word definitions from external sources (dictionaries).

     **Decision:** 17 Part 4

     - Type: Nested object structure
     - Purpose: Store component word meanings from dictionaries, help translators understand component parts, multiple sources confirm translations
     - When used: Only when `termComplexity = "complex"`
     - Location: Parent concept `_metadata` object (NOT in component concept)

     **Note on data flow:** When creating parent concept, scripts auto-generate componentLookups (dictionary API lookups). Component concepts are created separately with
     `definition` taken from parent's componentLookups. This maintains Single Source of Truth (lookup data stored once in parent) while ensuring TBX-Basic compliance (every
     concept has definition).

     **Structure breakdown:**

     **Level 1: Language code**
     ```json
     "componentLookups": {
       "en": { ... },
       "et": { ... }
     }
     ```

     **Level 2: Component name (from componentTerms)**
     ```json
     "en": {
       "addictive": [ ... ],
       "behavior": [ ... ]
     }
     ```

     **Level 3: Array of variants/definitions**
     ```json
     "addictive": [
       { "term": "addictive", ... },
       { "term": "addiction-causing", ... }
     ]
     ```

     **Level 4: Variant object**
     ```json
     {
       "term": "sõltuvuslik",
       "partOfSpeech": "adjective",     // OPTIONAL
       "definitions": ["..."],           // OPTIONAL (mainly EN)
       "sources": [                      // REQUIRED (if variant exists)
         {
           "name": "Sõnaveeb",
           "link": "https://..."
         }
       ]
     }
     ```

     **Sources array rationale:** Same term found in multiple sources (e.g., "sõltuvuslik" in Sõnaveeb and aare.edu.ee). Sources array shows multiple sources confirm
     translation, preserves all source links, no duplication.

     **Example:**
     ```json
     {
       "_metadata": {
         "componentLookups": {
           "en": {
             "addictive": [{
               "term": "addictive",
               "partOfSpeech": "adjective",
               "definitions": ["causing or tending to cause addiction"],
               "sources": [{
                 "name": "Merriam-Webster",
                 "link": "https://www.merriam-webster.com/dictionary/addictive"
               }]
             }]
           },
           "et": {
             "addictive": [
               {
                 "term": "sõltuvuslik",
                 "partOfSpeech": "adjective",
                 "sources": [
                   { "name": "Sõnaveeb", "link": "https://sonaveeb.ee/..." },
                   { "name": "aare.edu.ee", "link": "https://aare.edu.ee/..." }
                 ]
               },
               {
                 "term": "addiktiivne",
                 "partOfSpeech": "adjective",
                 "sources": [
                   { "name": "Sõnaveeb", "link": "https://sonaveeb.ee/..." }
                 ]
               }
             ]
           }
         }
       }
     }
     ```

     ---

     ### 2.6 REQUIRED vs OPTIONAL Quick Reference Table

     This table provides a quick overview of all fields, their requirement status, auto-generation, and implementation phase.

     #### Root Level

     | Field | Status | Auto-generated | Phase | Level |
     |-------|--------|----------------|-------|-------|
     | `metadata` | REQUIRED | Partial | 1 | Root |
     | `metadata.created` | REQUIRED | Yes | 1 | Root |
     | `metadata.standard` | REQUIRED | Yes | 1 | Root |
     | `metadata.formatVersion` | REQUIRED | Yes | 1 | Root |
     | `metadata.author` | REQUIRED | No | 1 | Root |
     | `metadata.project` | OPTIONAL | No | 1 | Root |
     | `metadata.license` | REQUIRED | No | 1 | Root |
     | `concepts` | REQUIRED | No | 1 | Root |

     #### Concept Level

     | Field | Status | Auto-generated | Phase | Level |
     |-------|--------|----------------|-------|-------|
     | `id` | REQUIRED | Yes | 1 | Concept |
     | `subjectField` | REQUIRED | Yes | 1 | Concept |
     | `languages` | REQUIRED | No | 1 | Concept |
     | `_metadata` | REQUIRED | Partial | 1 | Concept |

     #### Language Level

     | Field | Status | Auto-generated | Phase | Level |
     |-------|--------|----------------|-------|-------|
     | `xml:lang` | REQUIRED | Yes | 1 | Language |
     | `definition` | OPTIONAL | No | 2 | Language |
     | `terms` | REQUIRED | No | 1 | Language |

     #### Term Level

     | Field | Status | Auto-generated | Phase | Level |
     |-------|--------|----------------|-------|-------|
     | `term` | REQUIRED | No | 1 | Term |
     | `termType` | OPTIONAL | No | 2 | Term |
     | `partOfSpeech` | OPTIONAL → REQUIRED | No | 1→3 | Term |
     | `administrativeStatus` | REQUIRED | Yes | 1 | Term |
     | `supersededBy` | OPTIONAL | No | 2 | Term |
     | `note` | OPTIONAL | No | 2 | Term |
     | `source` | REQUIRED | Partial | 1 | Term |
     | `source.type` | REQUIRED | No | 1 | Term |
     | `source.title` | REQUIRED | No | 1 | Term |
     | `source.addedBy` | REQUIRED | Yes | 1 | Term |
     | `source.date` | REQUIRED | Yes | 1 | Term |
     | `source.page` | OPTIONAL | No | 1 | Term |
     | `source.chapter` | OPTIONAL | No | 1 | Term |
     | `source.url` | OPTIONAL | No | 1 | Term |
     | `source.publisher` | OPTIONAL | No | 1 | Term |
     | `source.edition` | OPTIONAL | No | 1 | Term |
     | `source.isbn` | OPTIONAL | No | 1 | Term |
     | `source.note` | OPTIONAL | No | 1 | Term |
     | `workflow` | OPTIONAL | No | 2 | Term |
     | `workflow.atlStatus` | OPTIONAL | No | 2 | Term |
     | `workflow.usageStatus` | OPTIONAL | No | 2 | Term |
     | `workflow.approvedBy` | CONDITIONAL | No | 2 | Term |
     | `workflow.approvedDate` | CONDITIONAL | Yes | 2 | Term |
     | `workflow.rejectedBy` | CONDITIONAL | No | 2 | Term |
     | `workflow.rejectedDate` | CONDITIONAL | Yes | 2 | Term |
     | `workflow.rejectedReason` | OPTIONAL | No | 2 | Term |
     | `workflow.firstUsedDate` | OPTIONAL | No | 2 | Term |
     | `usageExamples` | OPTIONAL | No | 2 | Term |
     | `transactions` | REQUIRED | Partial | 1 | Term |
     | `transactions[].type` | REQUIRED | No | 1 | Term |
     | `transactions[].actionType` | REQUIRED | No | 1 | Term |
     | `transactions[].responsibility` | REQUIRED | Yes | 1 | Term |
     | `transactions[].date` | REQUIRED | Yes | 1 | Term |
     | `transactions[].actionDescription` | OPTIONAL | No | 1 | Term |
     | `transactions[].statusChange` | OPTIONAL | No | 1 | Term |

     #### _metadata Level

     | Field | Status | Auto-generated | Phase | Level |
     |-------|--------|----------------|-------|-------|
     | `termComplexity` | REQUIRED | Yes | 1 | _metadata |
     | `componentTerms` | OPTIONAL | Yes | 1 | _metadata |
     | `isGlossaryTerm` | REQUIRED | Yes | 1 | _metadata |
     | `termType` | CONDITIONAL | Auto/Manual | 1 | _metadata |
     | `derivedFrom` | REQUIRED | Yes | 1 | _metadata |
     | `addedReason` | CONDITIONAL | No | 1 | _metadata |
     | `componentLookups` | OPTIONAL | No | 2 | _metadata |

     #### Legend

     **Status:**
     - REQUIRED: Must exist for valid entry
     - OPTIONAL: May be omitted
     - CONDITIONAL: Required only under specific conditions
     - OPTIONAL → REQUIRED: Currently optional, will become required in Phase 3

     **Auto-generated:**
     - Yes: Script automatically generates value
     - No: User must provide value
     - Partial: Some subfields auto-generated, some user-provided

     **Phase:**
     - 1: Initial extraction from WSO Glossary
     - 2: Enrichment (dictionaries, translations, review)
     - 3: Migration to stricter validation (partOfSpeech becomes REQUIRED)

     #### Conditional Requirements

     **`_metadata.termType`:**
     - REQUIRED if `isGlossaryTerm = false`
     - Must be `"component"` or `"communityAdded"`
     - `null` if `isGlossaryTerm = true`

     **`_metadata.addedReason`:**
     - REQUIRED if `termType = "communityAdded"`
     - Minimum 20 characters
     - Explains why community term was added

     **`workflow.approvedBy` + `workflow.approvedDate`:**
     - REQUIRED if `atlStatus = "atl_approved"`
     - Documents who approved and when

     **`workflow.rejectedBy` + `workflow.rejectedDate`:**
     - REQUIRED if `atlStatus = "rejected"`
     - Documents who rejected and when

     #### Summary Statistics

     **Total field count:** 52 fields (including all subfields)

     **By status:**
     - REQUIRED: 28 fields (54%)
     - OPTIONAL: 18 fields (35%)
     - CONDITIONAL: 6 fields (11%)

     **By auto-generation:**
     - Fully auto-generated: 15 fields
     - User-provided: 30 fields
     - Partial (mixed): 7 fields

     **By phase:**
     - Phase 1 (Initial extraction): 44 fields
     - Phase 2 (Enrichment): 7 fields
     - Phase 3 (Migration): 1 field (partOfSpeech OPTIONAL → REQUIRED)

     ---

     ## 3. Validation Rules

     Basic validation rules for the JSON structure. (Note: Complete JSON Schema validation file will be created separately as a machine-readable specification.)

     **Root level:**
     ```python
     assert "metadata" in data
     assert "concepts" in data
     assert isinstance(data["concepts"], list)
     assert len(data["concepts"]) > 0  # At least one concept
     ```

     **Metadata:**
     ```python
     assert all(field in data["metadata"] for field in ["created", "standard", "formatVersion", "author", "license"])
     ```

     **Concept level:**
     ```python
     for concept in data["concepts"]:
         assert "id" in concept
         assert "subjectField" in concept
         assert "languages" in concept
         assert "_metadata" in concept

         # EN language required
         assert "en" in concept["languages"]
         assert len(concept["languages"]["en"]["terms"]) > 0
     ```

     **Language level:**
     ```python
     for lang_code, lang_data in concept["languages"].items():
         assert "xml:lang" in lang_data
         assert lang_data["xml:lang"] == lang_code
         assert "terms" in lang_data
         assert len(lang_data["terms"]) > 0
     ```

     **Term level:**
     ```python
     for term in lang_data["terms"]:
         assert "term" in term
         assert "administrativeStatus" in term
         assert "source" in term
         assert "transactions" in term

         # Source validation
         assert all(field in term["source"] for field in ["type", "title", "addedBy", "date"])

         # Transactions validation
         assert len(term["transactions"]) >= 1
     ```

     **_metadata validation:**
     ```python
     assert all(field in concept["_metadata"] for field in ["termComplexity", "isGlossaryTerm", "derivedFrom"])

     # termType logic
     if concept["_metadata"]["isGlossaryTerm"]:
         assert concept["_metadata"].get("termType") is None
     else:
         assert "termType" in concept["_metadata"]
         assert concept["_metadata"]["termType"] in ["component", "communityAdded"]

         # addedReason for community terms
         if concept["_metadata"]["termType"] == "communityAdded":
             assert "addedReason" in concept["_metadata"]
             assert len(concept["_metadata"]["addedReason"]) >= 20
     ```

     ---

     ## 4. Enum Values Reference

     **source.type:**
     - `book`, `dictionary`, `website`, `manual_addition`, `conference`, `transcription`

     **administrativeStatus:**
     - `preferredTerm-admn-sts`, `admittedTerm-admn-sts`, `deprecatedTerm-admn-sts`, `supersededTerm-admn-sts`

     **termType (TBX-Basic, term level):**
     - `fullForm`, `acronym`, `abbreviation`, `shortForm`, `variant`

     **partOfSpeech:**
     - `noun`, `verb`, `adjective`, `adverb`, `phrase`, `null`

     **transactions.type:**
     - `origination`, `modification`

     **transactions.actionType:**
     - `originated`, `enriched`, `approved`, `rejected`, `modified`, `manual_addition`

     **workflow.atlStatus:**
     - `candidate`, `atl_approved`, `rejected`

     **workflow.usageStatus:**
     - `not_in_use`, `atl_in_use`, `formerly_in_use`

     **_metadata.termComplexity:**
     - `simple`, `complex`

     **_metadata.termType:**
     - `component`, `communityAdded`, `null`

     ---

     ## 5. Issue #13 Alignment

     This section confirms that all 3 key structural decisions from Issue #13 are properly implemented in the final JSON schema.

     **Background:** Issue #13 (TBX-Basic standards research) involved comprehensive research of TBX-Basic v1.2.1 standard and comparison with planned ATL workflow features. Three critical structural decisions were made that shape the entire database architecture.

     **Documentation created:**
     - `research/standards/TBX-Basic_FIELDS.md` - Complete TBX-Basic field reference (318 lines)
     - `research/standards/STRUCTURE_COMPARISON.md` - Current vs TBX-Basic comparison (296 lines)
     - `research/standards/TBX_vs_MY_PLANS.md` - TBX-Basic vs ATL workflow analysis (700+ lines)

     ---

     ### Decision 1: Transaction History ✅ IMPLEMENTED

     **Decision:** Full transaction history tracking (Variant B - Complete history)

     **Implementation in JSON schema:**
     - Field: `transactions` (REQUIRED array at term level)
     - Each transaction contains: `type`, `actionType`, `responsibility`, `date`, `actionDescription` (optional), `statusChange` (optional)
     - Minimum 1 transaction (origination)
     - All subsequent modifications appended to array

     **Rationale:**
     - ✅ Complete audit trail from origination to current state
     - ✅ Tracks who, when, what, and why for every change
     - ✅ Essential for collaborative workflow (ATL review team)
     - ✅ TBX-Basic compliant via `transacGrp` mapping

     **Reference:** Decision 12 (transactions field), Decision 15 (metadata wrapper)

     ---

     ### Decision 2: Status Tracking ✅ IMPLEMENTED

     **Decision:** Hybrid approach with dual status tracking (Variant C - Both separate)

     **Implementation in JSON schema:**
     - Field: `workflow` (OPTIONAL object at term level)
     - `workflow.atlStatus`: Review decision (`candidate`, `atl_approved`, `rejected`)
     - `workflow.usageStatus`: Actual usage (`not_in_use`, `atl_in_use`, `formerly_in_use`)
     - Field: `administrativeStatus` (REQUIRED): TBX-Basic standard status

     **Rationale:**
     - ✅ Distinguishes "de facto" (in use) vs "de jure" (approved)
     - ✅ ATL texts contain historical terms not yet reviewed
     - ✅ TBX-Basic compliant via `administrativeStatus`
     - ✅ ATL workflow tracked separately in custom `workflow` object
     - ✅ Supports 4 use cases: new approved, historical unreviewed, rejected but in use, approved but not yet used

     **Reference:** Decision 10 (workflow and administrativeStatus fields)

     ---

     ### Decision 3: Component Lookups ✅ IMPLEMENTED

     **Decision:** Hybrid approach - data in `_metadata`, optional reference at term level

     **Implementation in JSON schema:**
     - Field: `_metadata.componentLookups` (OPTIONAL object at concept level)
     - Structure: `{ "en": { "word": [variants...] }, "et": { "word": [variants...] } }`
     - Stores dictionary lookup results for all component words
     - Single source of truth - no duplication

     **Rationale:**
     - ✅ Component definitions stored once in parent concept
     - ✅ Smaller JSON size (no duplication across terms)
     - ✅ Clear relationship: parent concept owns component data

     **Reference:** Decision 17 Part 4 (componentLookups field)

     ---

     ## 6. TBX-Basic Compliance

     **TBX-Basic v1.2.1 (ISO 30042:2019):**

     **REQUIRED fields (all present):**
     - ✅ `id` (concept level)
     - ✅ `xml:lang` (language level)
     - ✅ `term` (term level)

     **Highly Recommended fields (all present):**
     - ✅ `subjectField` (concept level)
     - ✅ `definition` (language level, OPTIONAL but recommended)
     - ✅ `partOfSpeech` (term level, OPTIONAL initially → REQUIRED later)
     - ✅ `administrativeStatus` (term level)
     - ✅ `source` (term level, as object with detailed fields)
     - ✅ `note` (term level, OPTIONAL)
     - ✅ Transactions (term level, as `transactions` array)

     **Three-level hierarchy:**
     - ✅ Concept level (conceptEntry)
     - ✅ Language level (langSec)
     - ✅ Term level (termSec)

     **ACA Workflow Custom Extensions:**
     - `workflow` object (atlStatus, usageStatus) - Decision 10
     - `_metadata` object (7 custom fields) - Decision 17
     - `usageExamples` array - Decision 11
     - `transactions.actionType` enum - Decision 12
     - `metadata` top-level wrapper - Decision 15

     **Note:** Custom extensions are clearly marked (underscore prefix for `_metadata`, separate namespace for `workflow`) and documented. All custom fields are OPTIONAL or
     auto-generated, ensuring base TBX-Basic export remains possible.

     ---

     ### 6.1 TBX-Basic Field Coverage Analysis

     #### REQUIRED Fields (TBX-Basic minimum)

     | TBX-Basic Field | DRAFT Status | Level | Implementation |
     |----------------|--------------|-------|----------------|
     | `id` | ✅ REQUIRED | Concept | Format: "aca-0001" (Decision 2) |
     | `xml:lang` | ✅ REQUIRED | Language | ISO 639-1 codes (Decision 13) |
     | `term` | ✅ REQUIRED | Term | (Decision 5) |

     **✅ Coverage: 3/3 (100%)** - All TBX-Basic REQUIRED fields implemented

     ---

     #### Highly Recommended Fields (TBX-Basic)

     | TBX-Basic Field | DRAFT Status | Level | Implementation |
     |----------------|--------------|-------|----------------|
     | `subjectField` | ✅ REQUIRED | Concept | "ACA terminology" (Decision 3) |
     | `definition` | ✅ OPTIONAL | Language | Language-specific (Decision 14) |
     | `partOfSpeech` | ✅ OPTIONAL→REQUIRED | Term | Phase 1→3 migration (Decision 6) |
     | `administrativeStatus` | ✅ REQUIRED | Term | TBX standard values (Decision 10) |
     | `source` | ✅ REQUIRED (object) | Term | 4 REQUIRED + 7 OPTIONAL subfields (Decision 9) |
     | `note` | ✅ OPTIONAL | Term | (Decision 8) |
     | `transactions` | ✅ REQUIRED (array) | Term | Full history tracking (Decision 12) |

     **✅ Coverage: 7/7 (100%)** - All Highly Recommended fields implemented

     ---

     #### OPTIONAL Fields (TBX-Basic standard)

     **Implemented:**

     | TBX-Basic Field | DRAFT Status | Level | Implementation |
     |----------------|--------------|-------|----------------|
     | `termType` | ✅ OPTIONAL | Term | acronym/fullForm/etc (Decision 19) |
     | `supersededBy` | ✅ OPTIONAL | Term | Replacement tracking (Decision 7) |

     **Not Implemented (not needed for ACA project):**

     | TBX-Basic Field | Reason Not Included |
     |----------------|---------------------|
     | `grammaticalGender` | Not relevant for English/Estonian |
     | `geographicalUsage` | Single region per language |
     | `termLocation` | Not UI/software terminology |
     | `context` | Implemented via custom `usageExamples` array (Decision 11) |
     | `customerSubset` | Single customer (ATL) |
     | `projectSubset` | Implemented at root level as `metadata.project` (Decision 16) |
     | `crossReference` | Future enhancement (Issue #16) |
     | `externalCrossReference` | Not needed currently |
     | `xGraphic` | No graphics in terminology |

     **✅ Pragmatic approach:** Only relevant OPTIONAL fields implemented

     ---

     #### Custom Extensions (Beyond TBX-Basic)

     **ATL Workflow Extensions:**

     | Custom Field | Level | Decision | Purpose |
     |-------------|-------|----------|---------|
     | `workflow` object | Term | 10 | ATL review process tracking |
     | `workflow.atlStatus` | Term | 10 | Review decision (candidate/approved/rejected) |
     | `workflow.usageStatus` | Term | 10 | Actual usage in ATL texts |
     | `usageExamples` array | Term | 11 | Translation decision documentation |
     | `transactions.actionType` | Term | 12 | Action categorization for statistics |

     **_metadata Extensions (ISO 1087 + ATL workflow):**

     | Custom Field | Level | Decision | Purpose |
     |-------------|-------|----------|---------|
     | `_metadata` object | Concept | 17 | Term complexity & workflow metadata |
     | `termComplexity` | _metadata | 17 | simple/complex (ISO 1087) |
     | `componentTerms` | _metadata | 17 | Component word tracking |
     | `isGlossaryTerm` | _metadata | 17 | Term category classification |
     | `termType` (metadata) | _metadata | 17 | component/communityAdded |
     | `derivedFrom` | _metadata | 17 | Parent term relationships |
     | `addedReason` | _metadata | 17 | Community term justification |
     | `componentLookups` | _metadata | 17 | Dictionary lookup results storage |

     **Root Level Extensions:**

     | Custom Field | Decision | Purpose |
     |-------------|----------|---------|
     | `metadata` wrapper | 15 | File-level metadata (equivalent to TBX XML `<header>`) |

     ---

     #### Compliance Summary

     **TBX-Basic Standard Compliance:**
     - ✅ REQUIRED fields: 3/3 (100%)
     - ✅ Highly Recommended fields: 7/7 (100%)
     - ✅ OPTIONAL fields: 2 implemented (termType, supersededBy)
     - ✅ Three-level hierarchy: Concept → Language → Term maintained
     - ✅ Standard field names and values used (camelCase, TBX enums)

     **Custom Extensions:**
     - Clearly marked with underscore prefix (`_metadata`) or separate namespace (`workflow`)
     - All OPTIONAL or auto-generated (non-breaking for TBX export)
     - Support ATL collaborative workflow requirements
     - Enable ISO 1087 term complexity tracking
     - Provide audit trail and decision documentation

     **Export Compatibility:**
     - ✅ Base TBX-Basic XML export possible (strip custom fields)
     - ✅ CAT tools can import standard TBX fields
     - ✅ Custom fields preserved for ATL workflow
     - ✅ No conflicts with TBX-Basic standard

     ---

     ## 7. Migration Notes

     This section provides guidance for migrating from current structure to the TBX-Basic compliant structure, tracking schema changes, and planning future enhancements.

     ---

     ### 7.1 formatVersion Tracking Rules

     **Current version:** 1.0 (initial TBX-Basic compliant structure)

     **Versioning scheme:** Semantic versioning (MAJOR.MINOR)

     **Version increment rules:**

     **Minor version (1.0 → 1.1):**
     - Backward compatible changes only
     - New OPTIONAL field added
     - New enum value added to existing field
     - Documentation updates
     - Example: Adding optional `geographicalUsage` field

     **Major version (1.0 → 2.0):**
     - BREAKING changes
     - REQUIRED field changed or removed
     - Field renamed
     - Structure change (hierarchy level changed)
     - Enum value removed
     - Field type changed (string → object)
     - Example: Making `partOfSpeech` REQUIRED (Phase 3)

     **Implementation:**
     - Migration script updates `formatVersion` automatically
     - Old readers can detect incompatible versions
     - Clear migration path documented for each version

     ---

     ### 7.2 Current Structure → TBX-Basic Structure

     **Migration from pre-TBX structure (if applicable):**

     **Field name changes (camelCase alignment):**
     - `approved_by` → `approvedBy`
     - `approved_date` → `approvedDate`
     - `first_used_date` → `firstUsedDate`
     - `rejected_by` → `rejectedBy`
     - `rejected_date` → `rejectedDate`
     - `rejected_reason` → `rejectedReason`
     - `is_glossary_term` → `isGlossaryTerm`
     - `term_complexity` → `termComplexity`
     - `component_terms` → `componentTerms`
     - `derived_from` → `derivedFrom`
     - `added_reason` → `addedReason`
     - `component_lookups` → `componentLookups`

     **Structural changes:**
     - Add `metadata` wrapper at root level
     - Add `_metadata` object at concept level
     - Rename `atl_status` → `atlStatus`, `usage_status` → `usageStatus`
     - Change ID format: `"c001"` → `"aca-0001"`

     **Script:** `src/migrate_to_tbx_structure.py` (to be created)

     ---

     ### 7.3 Phase 2 Enrichment Plan

     **After initial WSO Glossary extraction (Phase 1), enrich with:**

     **Dictionary lookups:**
     - EN: Merriam-Webster, Oxford
     - ET: Sõnaveeb (includes EKI), aare.edu.ee
     - Add `definition` at language level
     - Populate `componentLookups` for complex terms

     **Estonian translations:**
     - Add ET language sections via dictionary lookups
     - ATL review team validates candidates
     - Update `workflow.atlStatus` and `workflow.usageStatus`
     - Add `usageExamples` from ATL texts

     **Community terms:**
     - Users add frequently discussed terms via `glossary_manager_via_terminal.py`
     - Set `_metadata.termType: "communityAdded"`
     - Require `addedReason` (min 20 chars)

     ---

     ### 7.4 Future Enhancements

     **Issue #15:** partOfSpeech vs termComplexity alignment review
     - Review edge cases ("at ease" - phrase or complex?)
     - Phase 3: Make `partOfSpeech` REQUIRED

     **Issue #16:** TBX-Basic crossReference field
     - Add semantic relationships between concepts
     - Use case: related concepts, see-also links

     **Issue #17:** ~~TBX-Basic termType field~~ ✅ COMPLETED
     - Implemented as Decision 19

     ---

