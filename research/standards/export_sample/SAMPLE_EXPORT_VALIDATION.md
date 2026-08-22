# Sample Export Validation Report

**Date:** 2026-08-22
**Purpose:** Empirical check required by the MUST 1 decision
([Issue #44](https://github.com/Anne-dot/aca-translation-assistant/issues/44)):
before the export script is written, prove with the official validators that
our reading of the TBX-Basic V4 specification — the adopted export mapping —
actually produces a valid file.

---

## What was validated

`sample_export.tbx` — a hand-crafted export of 3 concepts, exercising every
row of the adopted mapping table:

- concept → conceptEntry with id, subjectField (aca-0001 "abandonment",
  aca-0002 "addictive behavior", aca-0003 "addictive")
- language-level definitions with sources (`descripGrp` + `admin
  type="source"`)
- partOfSpeech and usageStatus term notes; derived status values:
  `preferred` (approved / EN glossary), `deprecated` + reason note
  (rejected), and **no status + "Candidate — awaiting ATL review" note**
  (candidate — the export-never-claims-more rule)
- usage example as `descrip type="context"` with its own source
- flattened `admin type="source"` strings on terms
- `transacGrp` with `creation` / `modification`, responsibility, date
- parent ↔ component `crossReference` in both directions (aca-0002 ↔ aca-0003)
- `tbxHeader` with license/author (publicationStmt) and title
- back-matter `respPerson` registry (name + role only — privacy rule);
  transaction responsibilities reference person ids via `target` (IDREF)

## Tools

- lxml 6.0.1 (RelaxNG + XSD validation)
- pyschematron in a scratch venv (ISO Schematron with xslt2 query binding,
  which lxml's built-in isoschematron cannot process)
- Official validation artifacts from the repo:
  `iso-tr24633-2-schemas/core_schema.rng`, `core_schema.xsd` (ISO TR 24633-2
  Annex A) and `TBX-Basic-V4-files/basic_schema.sch` (TerminOrgs V4)

## Results

| Check | Result |
|---|---|
| XML well-formedness | ✅ OK |
| TBX core structure, RelaxNG (`core_schema.rng`) | ✅ VALID |
| TBX core structure, XSD (`core_schema.xsd`) | ✅ VALID |
| TBX-Basic constraints, Schematron (`basic_schema.sch`) | ✅ VALID — 0 failed asserts |
| **Negative control:** `TBX-Basic-sample-badPOS.tbx` | ✅ correctly INVALID ("partOfSpeech must take one of: noun, verb, adjective, adverb, properNoun or other") |
| **Negative control:** `TBX-Basic-sample-bad-termtype.tbx` | ✅ correctly INVALID ("termType must take one of: fullForm, acronym, abbreviation, shortForm, variant, phrase") |

The negative controls confirm the schematron actually enforces the picklists —
and their error messages independently confirm the exact enum values our
SHOULD 1 / SHOULD 2 decisions adopted.

## Findings (bugs the validator caught in the first draft of the sample)

1. **`fileDesc` child order:** the core schema requires
   `publicationStmt? , titleStmt? , sourceDesc+` — publicationStmt comes
   BEFORE titleStmt. (First draft had them reversed.)
2. **`back` placement:** back matter is a **sibling of `body` inside
   `text`** (`<text><body>…</body><back>…</back></text>`), not a child of
   body. Notably, **TBX-Basic V4's own Appendix B snippet shows `<back>`
   inside `<body>` — that snippet contradicts the official schemas.** The
   schemas are authoritative; the export script must follow them, not the
   Appendix B snippet.
3. IDREF discipline works as designed: `transacNote/@target` values must
   resolve to `refObject/@id` entries in the back matter — the validator
   enforces the person-registry linkage for free.

## Conclusion

The adopted export mapping produces a fully valid TBX-Basic V4 file. The
export script (M2) can be written against this sample as its reference
output. Finding 2 must be encoded in the script (schemas over Appendix B
snippet).
