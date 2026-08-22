# JSON Schema Specification — Internal Terminology Database, TBX-Basic Exportable

**Version:** 2.0
**Standard relationship:** Internal format, exportable to TBX-Basic Version 4 (2025)
**Date:** 2026-08-22 (v1.0: 2025-10-20)
**Based on:** Issue #14 Decisions 1–19 and Issue #13 structural decisions, as
revised by the 7 decisions of the [Issue #44 TBX review](https://github.com/Anne-dot/aca-translation-assistant/issues/44)
(August 2026) — consolidated in [TBX_M1_DECISIONS_2026-08.md](TBX_M1_DECISIONS_2026-08.md).

---

## Document Overview

This document is the authoritative specification of the ACA Translation
Assistant terminology database format. The database is a JSON file that serves
as the **internal master**: it holds the community's full, rich truth about
every term (translations, review decisions, usage, sources, history). It is
**not** a TBX file; instead, it is designed so that a valid TBX-Basic Version 4
file can always be produced from it by a deterministic export (see Section 6).

Version 2.0 incorporates the August 2026 review decisions. The main changes
from 1.0: the compliance claim is reworded ("exportable", not "compliant");
`administrativeStatus`, `termComplexity`, `componentTerms` and
`componentLookups` are no longer stored (they are derived — computed on
demand); the workflow status fields are renamed
(`communityReviewStatus`, `communityTextUsage`); and the `partOfSpeech` enum
follows the TBX-Basic V4 picklist. Full change list in Section 9.

---

## 1. Design Principles

These principles govern every field decision in this specification.

**1. Concept orientation (ISO 704 / TBX).** One concept = one entry. A
multiword term ("addictive behavior") designates one concept as a whole; its
component words ("addictive") are *different* concepts with their own entries.
Entries never store another concept's content.

**2. Original data is guarded; derived data is computed.** Original facts
(term texts, translations, definitions, sources, review decisions, usage
records, history) live in exactly one place and are protected by the
validator. Derived facts (whether a term is multiword, its component word
list, its TBX export status) contain zero original information and are
**never stored** — shared functions compute them on demand, so they can never
drift out of sync.

**3. Boundary invariant.** No faulty data ever leaves a pipeline stage. Every
value downstream is either a validated enum value or an explicitly flagged
absence — never free text on a closed field, never a guess. Unknown input
fails loudly into a needs-human state.

**4. Program/human cooperation.** Automation performs the deterministic work
and records itself in `transactions`; humans confirm, decide exceptions, and
are recorded likewise. Every future write path (M2 CLI, M3 platform) enforces
the same closed vocabularies at input time ("computer says no"), using one
shared validation ruleset.

**5. Status says WHAT, note says WHY.** Notes never duplicate what a status
already expresses; they carry reasons, context, and nuance.

**6. The export never claims more than we know.** An unreviewed term exports
with *no* status plus an explanatory note — never as a false "admitted".

---

## 2. Complete Structure Examples

### 2.1 Example 1: Simple Glossary Term

**Term:** "abandonment" (single word, official WSO glossary term)

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
    "isGlossaryTerm": true,
    "termType": null,
    "derivedFrom": []
  }
}
```

Note what is **absent** compared to v1.0: no `administrativeStatus` (derived at
export: EN glossary term → `preferred`), no `termComplexity` (computed:
single word), no `componentTerms` (computed: none).

### 2.2 Example 2: Complex Term with Estonian Translation

**Term:** "addictive behavior" (multiword; ET section with an approved and a
rejected variant; usage example)

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
          "source": {
            "type": "dictionary",
            "title": "Sõnaveeb",
            "url": "https://sonaveeb.ee/search/unif/dlall/dsall/addiktiivne",
            "addedBy": "Anne Ruusmann",
            "date": "2025-10-20"
          },
          "workflow": {
            "communityReviewStatus": "approved",
            "communityTextUsage": "in_use",
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
              "statusChange": "candidate → approved"
            }
          ]
        },
        {
          "term": "sõltuvuslik käitumine",
          "partOfSpeech": "noun",
          "source": {
            "type": "dictionary",
            "title": "Sõnaveeb",
            "url": "https://sonaveeb.ee/search/unif/dlall/dsall/sõltuvuslik",
            "addedBy": "Anne Ruusmann",
            "date": "2025-10-20"
          },
          "workflow": {
            "communityReviewStatus": "rejected",
            "communityTextUsage": "not_in_use",
            "rejectedBy": "ATL review team",
            "rejectedDate": "2025-10-20",
            "rejectedReason": "Too clinical, not ACA tone"
          },
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
    "isGlossaryTerm": true,
    "termType": null,
    "derivedFrom": []
  }
}
```

Notes:
- Whether this term is multiword, and its component word list, are **computed**
  from the term string by the shared derivation function — not stored.
- Component words get their **own concepts** (Example 3); this entry stores
  nothing about them. At export, the relation appears as `crossReference`.
- The rejected variant exports as `deprecated` + note; the approved one as
  `preferred`; a `candidate` would export with **no status** + note
  "Candidate — awaiting ATL review".

### 2.3 Example 3: Component Term

**Term:** "addictive" (its own concept; created during Phase 2 enrichment
because it appears in the glossary terms "addictive behavior" and "addictive
thinking")

```json
{
  "id": "aca-0003",
  "subjectField": "ACA terminology",
  "languages": {
    "en": {
      "xml:lang": "en",
      "definition": "Causing or tending to cause addiction",
      "terms": [{
        "term": "addictive",
        "partOfSpeech": "adjective",
        "source": {
          "type": "dictionary",
          "title": "Merriam-Webster",
          "url": "https://www.merriam-webster.com/dictionary/addictive",
          "addedBy": "Anne Ruusmann",
          "date": "2025-10-20"
        },
        "transactions": [{
          "type": "origination",
          "actionType": "enriched",
          "responsibility": "System",
          "date": "2025-10-20"
        }]
      }]
    },
    "et": {
      "xml:lang": "et",
      "definition": "Sõltuvust tekitav",
      "terms": [{
        "term": "addiktiivne",
        "partOfSpeech": "adjective",
        "source": {
          "type": "dictionary",
          "title": "Sõnaveeb",
          "url": "https://sonaveeb.ee/search/unif/dlall/dsall/addiktiivne",
          "addedBy": "Anne Ruusmann",
          "date": "2025-10-20"
        },
        "workflow": {
          "communityReviewStatus": "candidate"
        },
        "transactions": [{
          "type": "origination",
          "actionType": "enriched",
          "responsibility": "System",
          "date": "2025-10-20"
        }]
      }]
    }
  },
  "_metadata": {
    "isGlossaryTerm": false,
    "termType": "component",
    "derivedFrom": ["addictive behavior", "addictive thinking"]
  }
}
```

Notes:
- **This concept is the single home** for everything about the word
  "addictive". The parent concepts store no copy of it.
- `derivedFrom` is **provenance** (why this concept exists) — original data,
  stored; it is not a derivable mirror.
- The concept is fully editable: a future Finnish section is added here.
- Creation is one-time and one-directional (create-if-missing during
  enrichment, recorded in `transactions`); nothing flows back to the parents.

### 2.4 Example 4: Community Added Term

**Term:** "tervenemistee" (community-added, frequently discussed in ATL)

```json
{
  "id": "aca-0004",
  "subjectField": "ACA terminology",
  "languages": {
    "et": {
      "xml:lang": "et",
      "definition": "Tervistumise ja enesearengu protsess ACA kontekstis",
      "terms": [{
        "term": "tervenemistee",
        "partOfSpeech": "noun",
        "source": {
          "type": "manual_addition",
          "title": "ATL kogukonna ettepanek",
          "addedBy": "Mari K",
          "date": "2025-11-20"
        },
        "workflow": {
          "communityReviewStatus": "candidate",
          "communityTextUsage": "in_use"
        },
        "transactions": [{
          "type": "origination",
          "actionType": "manual_addition",
          "responsibility": "Mari K",
          "date": "2025-11-20"
        }]
      }]
    }
  },
  "_metadata": {
    "isGlossaryTerm": false,
    "termType": "communityAdded",
    "derivedFrom": [],
    "addedReason": "Kordub sageli ATL tekstides ja tekitab arutelusid tõlkimisel. Vajab kokkulepet eelistatud variandi osas."
  }
}
```

> **⚠️ OPEN QUESTION (found during the v2.0 documentation pass):** this
> example has an ET-only concept, but the validation rule inherited from
> Decision 4 says the EN language section is always REQUIRED. The two have
> contradicted each other since v1.0. Options: (a) relax the rule — EN
> required except for `termType: "communityAdded"` concepts; (b) require an
> EN gloss for every community term. **Not yet decided** — needs an Issue #44
> follow-up decision. Until decided, the validator treats EN-missing as a
> warning (not an error) for communityAdded concepts only.

### 2.5 Example 5: Acronym + Full Form

**Terms:** "ACA" + "Adult Children of Alcoholics" (EN), "ATL" + "Alkohooliku
Täiskasvanud Lapsed" (ET) — one concept, multiple term variants

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
          "note": "Lühend - Alkohooliku Täiskasvanud Lapsed",
          "source": {
            "type": "website",
            "title": "ATL koduleht",
            "url": "https://atl.ee",
            "addedBy": "Anne Ruusmann",
            "date": "2025-10-20"
          },
          "workflow": {
            "communityReviewStatus": "approved",
            "communityTextUsage": "in_use",
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
          "note": "Täisnimi, harva kasutatav",
          "source": {
            "type": "website",
            "title": "ATL koduleht",
            "url": "https://atl.ee",
            "addedBy": "Anne Ruusmann",
            "date": "2025-10-20"
          },
          "workflow": {
            "communityReviewStatus": "approved",
            "communityTextUsage": "in_use",
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
    "isGlossaryTerm": true,
    "termType": null,
    "derivedFrom": []
  }
}
```

Notes:
- TBX-standard `termType` (term level: acronym/fullForm/…) and our
  `_metadata.termType` (concept level: origin category) are different fields
  with different purposes; both may coexist.
- Note the ACA → ACAD transition (2026 ABC, phased 5–10 years): when WSO
  materials adopt ACAD, `supersededBy` handles the term-level succession.

> **⚠️ OPEN QUESTION (found during the v2.0 documentation pass):** the MUST 3
> derivation rule "EN glossary terms → `preferred`" is too coarse when one
> concept has several EN variants ("ACA" and its full form cannot both be
> `preferred`; V4 §6.23 allows one value per term and expects preferences to
> differ). A refinement is needed — e.g. derive `preferred` for the glossary's
> primary form and `admitted` for other EN variants (primary = first listed,
> or an explicit small marker). **Not yet decided** — needs an Issue #44
> follow-up decision. Until decided, the exporter emits `preferred` for the
> first EN term of a concept and `admitted` for subsequent EN variants, and
> this behaviour is marked provisional.

---

## 3. Field Reference by Level

**Hierarchy:**
```
Root (file wrapper)
  └─ metadata (file-level information)
  └─ concepts[]
      └─ Concept level (id, subjectField, languages, _metadata)
          └─ Language level (xml:lang, definition, terms)
              └─ Term level (term, …, workflow, usageExamples, transactions)
```

### 3.1 Root Level

**`metadata`** (REQUIRED object):
- `created` (REQUIRED, auto) — ISO date
- `standard` (REQUIRED, fixed) — `"Internal format, exportable to TBX-Basic Version 4 (2025)"`
- `formatVersion` (REQUIRED, auto) — `"2.0"`; rules in Section 9
- `author` (REQUIRED) — `"Anne Ruusmann"`
- `project` (OPTIONAL) — `"ACA Translation Assistant"`
- `license` (REQUIRED) — `"CC BY-SA 4.0"` (free use incl. commercial so WSO
  can publish; ShareAlike keeps improvements open; author credited)

**`concepts`** (REQUIRED array, at least one concept).

### 3.2 Concept Level

- **`id`** (REQUIRED, auto): `"aca-"` + zero-padded number (`"aca-0001"`).
  Future-proof for multi-community use (Milestone 4).
- **`subjectField`** (REQUIRED): currently `"ACA terminology"` for all
  concepts. Domain classification, NOT term-origin categorisation (that is
  `_metadata`).
- **`languages`** (REQUIRED object): keys are ISO 639-1 codes (`"en"`,
  `"et"`); EN section REQUIRED (but see Example 4's open question for
  communityAdded concepts), others optional, filled during enrichment.
- **`_metadata`** (REQUIRED object): see 3.5.

### 3.3 Language Level

- **`xml:lang`** (REQUIRED): must equal the key. Needed for TBX export
  (`<langSec xml:lang="…">`).
- **`definition`** (OPTIONAL): language-specific definition. Exported as
  `descrip type="definition"` at language level (V4 §6.5 allows concept or
  language level; this termbase consistently uses the **language level**, per
  V4 Appendix A's pick-one-level recommendation).
- **`terms`** (REQUIRED array, at least one term object).

### 3.4 Term Level

**REQUIRED:** `term`, `source`, `transactions`
**OPTIONAL:** `termType`, `partOfSpeech` (→ REQUIRED at the gate), `supersededBy`, `note`, `workflow`, `usageExamples`

- **`term`** (REQUIRED): the term text. Base form only (lemma); CAT tools
  handle inflection matching.
- **`termType`** (OPTIONAL, TBX picklist): `fullForm`, `acronym`,
  `abbreviation`, `shortForm`, `variant`, `phrase`. "phrase" marks fixed
  expressions/idioms/sayings (this is the FORM axis — see Section 5).
- **`partOfSpeech`** (OPTIONAL now → REQUIRED at the gate): `noun`, `verb`,
  `adjective`, `adverb`, `properNoun`, `other`, or null. Matches the V4
  picklist exactly; **"phrase" is not a partOfSpeech value** (wrong axis).
  Source markers pronoun/preposition/conjunction map to `other`.
  Gate: flips to REQUIRED only when the validator counts zero
  empty/unverified; the TBX export refuses to run while any exported term
  lacks it (V4 §9).
- **`supersededBy`** (OPTIONAL): term text of the replacement within the same
  language section. Exported as `deprecated` + crossReference. (Text-vs-ID
  referencing is an open decision — see Section 10.)
- **`note`** (OPTIONAL): explanations, register info ("Informal register"),
  usage guidance. Never duplicates a status (Principle 5).
- **`source`** (REQUIRED object): provenance of this term.
  REQUIRED subfields: `type` (enum: book/dictionary/website/manual_addition/
  conference/transcription), `title`, `addedBy` (auto), `date` (auto, ISO).
  OPTIONAL: `chapter`, `page`, `edition`, `isbn`, `publisher`, `url`, `note`.
- **`workflow`** (OPTIONAL object) — the community's status truth (single
  source of truth; the TBX status is derived from it at export and never
  stored):
  - `communityReviewStatus` (enum): `candidate` | `approved` | `rejected`
  - `communityTextUsage` (enum): `in_use` | `not_in_use` | `formerly_in_use`
    — de facto usage in community texts; never affects the derived export
    status (de facto vs de jure are separate facts)
  - IF approved: `approvedBy`, `approvedDate` REQUIRED
  - IF rejected: `rejectedBy`, `rejectedDate` REQUIRED; `rejectedReason`
    OPTIONAL (exports as note)
  - `firstUsedDate` (OPTIONAL)
- **`usageExamples`** (OPTIONAL array): each with `source` (REQUIRED, WSO
  materials only), `enContext` (REQUIRED), `etTranslation` (REQUIRED),
  `translatorNote` (OPTIONAL object: author/date/explanation/keyInsight —
  JSON-only, never exported).
- **`transactions`** (REQUIRED array, min 1): each with `type`
  (origination|modification), `actionType` (originated|enriched|approved|
  rejected|modified|manual_addition), `responsibility`, `date` (auto),
  `actionDescription` (OPTIONAL), `statusChange` (OPTIONAL, e.g.
  "candidate → approved"). At export only type/responsibility/date survive
  (as `transacGrp`; `origination` exports as `creation`); the actionType
  system is the internal statistics/audit layer.

### 3.5 _metadata Level (concept-level custom extension)

Four fields remain (v1.0 had seven — see Section 9):

- **`isGlossaryTerm`** (REQUIRED, auto): true for WSO glossary imports,
  false for components and community additions.
- **`termType`** (CONDITIONAL): `"component"` | `"communityAdded"` when
  `isGlossaryTerm` is false; null otherwise. (Origin category — distinct from
  the TBX term-level termType.)
- **`derivedFrom`** (REQUIRED array): parent term texts for component
  concepts (provenance — original data, stored); empty for glossary and
  community terms. Component concepts must have ≥ 1 entry.
- **`addedReason`** (CONDITIONAL): REQUIRED (min 20 chars) when
  `termType: "communityAdded"`.

**Removed in 2.0 (now computed, never stored):** `termComplexity`,
`componentTerms`, `componentLookups`. See Section 4.

---

## 4. Derived Values (computed, not stored)

One shared module (single source of truth for these rules) provides:

| Function | Derives | From | Used by |
|---|---|---|---|
| `is_multiword(term)` | whether a term is a multiword unit | term string (whitespace; parenthetical content stripped first) | enrichment (should components be created?), statistics |
| `component_words(term)` | the component word list | term string (whitespace split, lowercase) | enrichment (create-if-missing component concepts), export (crossReference), display |
| `export_status(term_obj)` | TBX `usageStatus` value or "omit" | workflow + supersededBy (+ isGlossaryTerm) | export, display |

Derivation rules for `export_status` (deterministic):
1. `supersededBy` set → `deprecated` (+ crossReference to the replacement)
2. `communityReviewStatus: rejected` → `deprecated`
3. `communityReviewStatus: approved` → `preferred`
4. `candidate` / no workflow → **no status** + note "Candidate — awaiting ATL
   review"
   - exception: EN glossary terms → `preferred` (see Example 5's open question
     for multi-variant EN concepts)

Rationale: these values contain zero original information; storing them would
create copies that can drift (the v1.0 componentLookups problem). Professional
practice agrees: neither TBX (any version) nor IATE has a term-complexity or
component-list field — multiword-ness is an analysis you run, not a column you
maintain. Hyphen handling ("self-esteem") is deliberately open — the rule can
mature inside the shared function without any data migration.

---

## 5. The Three Axes (no cross-field conflicts)

| Axis | Question | Where | Example: "at ease" |
|---|---|---|---|
| Structure | is it multiword? | computed (`is_multiword`) | yes |
| Form | what kind of unit? | `termType` | `"phrase"` |
| Grammar | what word class? | `partOfSpeech` | `"other"` |

These are independent facts and may combine freely; the validator raises **no
cross-field errors** between them. (Source markers mix all three in one string
— "v, idiom, informal" — and the extraction parser splits them into their
homes: PoS → partOfSpeech, idiom/saying → termType "phrase", register → note.)

---

## 6. Export Mapping (JSON → TBX-Basic V4)

The export script (M2) is a deterministic projection. The exported file uses
the skeleton of V4 Appendix B: `<tbx type="TBX-Basic" style="dca">` root,
`tbxHeader`, `text/body` with one `conceptEntry` per concept, optional back
matter, validated by `core_schema.rng|xsd` + `basic_schema.sch`.

| JSON (internal master) | TBX-Basic V4 export | Basis |
|---|---|---|
| concept | `conceptEntry id="…"` | core |
| `languages.xx` | `langSec xml:lang="xx"` | §6.10 |
| term | `termSec` → `term` | §6.19 |
| `subjectField` | `descrip type="subjectField"` (concept level) | §6.18 |
| language `definition` | `descrip type="definition"` (language level) | §6.5 |
| `partOfSpeech` | `termNote type="partOfSpeech"` — mandatory per exported term; export refuses otherwise | §6.12, §9 |
| `termType` | `termNote type="termType"` | §6.21 |
| `workflow.communityReviewStatus` | `termNote type="usageStatus"` via `export_status()` (Section 4) | §6.23 |
| `supersededBy` | `deprecated` + `ref type="crossReference"` | §6.23, §6.2 |
| `workflow.rejectedReason`; register notes | `note` | §6.11 |
| `usageExamples.enContext` / `.etTranslation` | `descrip type="context"` on the EN / ET term; source via `descripGrp` + `admin type="source"` | §6.1, §6.15 |
| `source` object | `admin type="source"`, flattened to one string | §6.17 |
| `transactions` | `transacGrp` (transac + transacNote + date); `origination` → `creation` | §6.22, §7.1–7.3 |
| component / seeAlso relations | `ref type="crossReference"` (computed from derivedFrom / stored seeAlso) | §6.2 |
| root `metadata` | `tbxHeader` (titleStmt + publicationStmt/sourceDesc) | App. B |
| people (addedBy/approvedBy/responsibility) | back-matter `respPerson`; transactions reference person ids. **Privacy: name + role only; e-mail only with consent** | §7.4, §6.14 |

**JSON-only by design (never exported):** `translatorNote`,
`workflow.communityTextUsage`, `transactions.actionType/actionDescription/
statusChange`, `_metadata.isGlossaryTerm/termType/addedReason`. The CAT
export serves translators (status, definitions, contexts, PoS, sources,
rejection reasons); community process knowledge lives in the master and the
M2/M3 tools. Export is one-way: CAT tools send nothing back.

---

## 7. Validation Rules

**Root:** `metadata` (with all REQUIRED subfields) and non-empty `concepts`.

**Concept:** `id` (pattern `aca-\d{4}`), `subjectField`, `languages`,
`_metadata` present. EN section required (warning-only for communityAdded —
open question, Example 4). `_metadata` logic:
```python
if md["isGlossaryTerm"]:
    assert md.get("termType") is None
    assert md["derivedFrom"] == []
else:
    assert md["termType"] in ("component", "communityAdded")
    if md["termType"] == "component":
        assert len(md["derivedFrom"]) >= 1
    if md["termType"] == "communityAdded":
        assert len(md.get("addedReason", "")) >= 20
```

**Language:** `xml:lang` equals its key; non-empty `terms`.

**Term:** `term` non-empty; `source` with type/title/addedBy/date (type in
enum; date ISO); `transactions` ≥ 1 (types and actionTypes in enums; dates
ISO). If `partOfSpeech` present: in enum. If `workflow` present: enums +
conditional requirements (approvedBy/approvedDate; rejectedBy/rejectedDate).
If `supersededBy` present: target term exists in the same language section.

**Referential integrity:** every `derivedFrom` entry names an existing
glossary term; after Phase 2 enrichment, every component word designated by
the enrichment rule resolves to an existing component concept.

**Derived-value identity:** no stored field may duplicate a derived value
(the schema simply has no such fields — this rule guards against their
reintroduction).

**Boundary invariant (parser + entry tools):** closed vocabularies; unknown
input → needs-human state, never guessed; multi-PoS source markers → human
decision (possible homonym split).

**Gates:** partOfSpeech REQUIRED-flip only at zero empty/unverified; export
precondition: every exported term has partOfSpeech.

---

## 8. Enum Values Reference

- **source.type:** `book`, `dictionary`, `website`, `manual_addition`,
  `conference`, `transcription`
- **partOfSpeech:** `noun`, `verb`, `adjective`, `adverb`, `properNoun`,
  `other` (+ null until the gate)
- **termType (term level, TBX):** `fullForm`, `acronym`, `abbreviation`,
  `shortForm`, `variant`, `phrase`
- **transactions.type:** `origination`, `modification` (exported as
  `creation`/`modification`)
- **transactions.actionType:** `originated`, `enriched`, `approved`,
  `rejected`, `modified`, `manual_addition`
- **workflow.communityReviewStatus:** `candidate`, `approved`, `rejected`
- **workflow.communityTextUsage:** `in_use`, `not_in_use`, `formerly_in_use`
- **_metadata.termType:** `component`, `communityAdded`, null

Removed in 2.0: `administrativeStatus` enum (derived at export),
`termComplexity` enum (computed).

---

## 9. Version History and Migration Notes

**formatVersion rules:** minor (2.0 → 2.1) = backward compatible (new
OPTIONAL field/enum value); major = breaking (REQUIRED field changed/removed,
rename, structure change). The entire August 2026 review is **one** major bump
(1.0 → 2.0).

**Changes 1.0 → 2.0** (all from the [Issue #44 review](https://github.com/Anne-dot/aca-translation-assistant/issues/44)):

| Change | Decision |
|---|---|
| `metadata.standard` reworded to "Internal format, exportable to TBX-Basic Version 4 (2025)" | MUST 1, M1a |
| `administrativeStatus` removed (derived at export; never stored) | MUST 3 |
| `workflow.atlStatus` → `workflow.communityReviewStatus`; values lose `atl_` prefix | MUST 3 |
| `workflow.usageStatus` → `workflow.communityTextUsage`; values lose `atl_` prefix | MUST 3 |
| `partOfSpeech` enum: − `phrase`, + `properNoun`, + `other` | SHOULD 1 |
| `_metadata.componentLookups` removed | MUST 2 |
| `_metadata.termComplexity` removed (computed) | SHOULD 2 |
| `_metadata.componentTerms` removed (computed) | SHOULD 3 |
| Export mapping table adopted (Section 6) | MUST 1 |
| Design principles codified (Section 1) | all |

No data migration is required: no data file in the 1.0 TBX structure was ever
produced (the migration script had not been written), and the current
extraction data (`data/1_extracted/`) predates this structure entirely.

**Phases (unchanged in spirit):** Phase 1 extraction → Phase 2 enrichment
(definitions, ET candidates, component concepts, PoS filling + verification)
→ Phase 3 gates (partOfSpeech REQUIRED; export enabled).

---

## 10. Open Questions (deliberate, tracked)

1. **Text vs ID references** (`derivedFrom`, `supersededBy`): silent breakage
   on rename is unacceptable; choose IDs or script-managed renames +
   referential validation. Decide before the migration script.
2. **EN-required rule vs ET-only community terms** (Example 4) — needs an
   Issue #44 follow-up decision.
3. **Status derivation for multi-variant EN concepts** (Example 5) — needs an
   Issue #44 follow-up decision; provisional rule documented there.
4. **Which component words deserve concepts** (stop-words / dictionary-hit
   filtering) — Phase 2 enrichment design.
5. **Hyphenated terms** ("self-esteem") in the shared split function.
