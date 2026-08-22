# TBX M1 Review — Consolidated Decisions (August 2026)

**Provenance:** All 7 decisions below were made by Anne on 2026-08-21/22 and
posted as comments to [GitHub Issue #44](https://github.com/Anne-dot/aca-translation-assistant/issues/44),
which is the official decision record. This file consolidates them into one
document for reading and for AI-assisted critique (NotebookLM round 2).
The questions came from [TBX_M1_CRITICAL_REVIEW.md](TBX_M1_CRITICAL_REVIEW.md)
(NotebookLM round 1, January 2026): 3 MUST + 3 SHOULD, plus one version
sub-decision discovered during the review.

**Method:** each question was worked through in a deep-dive dialogue (problem →
history of the original decision → what the standard says → options →
decision), with the explicit rule that old decisions earn no protection from
age, and every compliance claim needs a citation from the specification.

---

## The common thread

All seven decisions follow one principle discovered early in the review:

> **Original data is guarded; derived data is computed.**
> Original facts (terms, translations, definitions, sources, review decisions,
> history) live in exactly one place and are protected by validators. Derived
> facts (word counts, component lists, export statuses) are never stored —
> they are computed on demand by shared functions, so they can never drift.

Supporting rules that recur across decisions:

- **Boundary invariant:** no faulty data ever leaves a pipeline stage. Values
  downstream are validated enums or explicitly flagged absences — never free
  text, never a guess.
- **Status says WHAT, note says WHY** — notes never duplicate what a status
  already expresses.
- **The export never claims more than we know** (e.g. unreviewed terms export
  with no status rather than a fake "admitted").
- **Program/human cooperation contract:** automation does the deterministic
  95%, humans confirm and decide the exceptions, and `transactions` records
  who did which.

---

## Decision M1a — Target specification version: TBX-Basic Version 4 (2025-08-21)

The project targets **TBX-Basic Version 4** (TerminOrgs, November 2025) as the
TBX export compliance target, replacing the v1.2.1 assumption behind the
October 2025 schema decisions.

- V4 is the publisher's current spec; v1.2.1 is superseded.
- The full prose spec is freely available (entry structure + permitted
  elements included — previously only behind the ISO paywall).
- Validation files are in the repo (`TBX-Basic-V4-files/`,
  `iso-tr24633-2-schemas/`); version landscape in [TBX_VERSIONS.md](TBX_VERSIONS.md).
- Follow-up: one CAT-tool import sanity test in M2.

Key V4 changes affecting us: standard status field is now `usageStatus`
(`preferred`/`admitted`/`deprecated`, no "superseded"); transaction types are
`creation`/`modification`; partOfSpeech picklist gains `properNoun`, still has
no "phrase"; **partOfSpeech is mandatory per term for automated/CAT use (V4
§9)**; `transacGrp` admits no note.

---

## Decision MUST 1 — "TBX-Basic exportable", export mapping adopted (2026-08-22)

1. **The claim "100% TBX-Basic compliant" (old Decision 18) is replaced
   everywhere with "TBX-Basic exportable".** TBX-Basic is a closed dialect
   (V4 §9, Appendix B): a compliant file may use only the listed data
   categories, so `workflow`, `_metadata`, `usageExamples` can never appear in
   a TBX file. Our JSON is not a TBX file — it is the internal master; TBX is
   an export projection. `metadata.standard` becomes
   `"Internal format, exportable to TBX-Basic Version 4 (2025)"`.
2. **The export mapping table is adopted as the M1 decision** (script is M2):
   see the consolidated table below.
3. **JSON-only by design** (no standard slot): `translatorNote`,
   `workflow.communityTextUsage`, `transactions.actionType/actionDescription/
   statusChange`, `_metadata.isGlossaryTerm/termType(origin)/addedReason`.
4. Follow-ups: documentation pass (this file + spec update), consolidated
   mapping table in the spec, **early empirical check** (hand-crafted sample
   TBX validated against `core_schema` + `basic_schema.sch` before the export
   script is written), M2 CAT import test.

---

## Decision MUST 2 — Atomic component architecture (2026-08-22)

1. All content about a component word (definitions, ET candidates with
   sources) lives in the **component's own concept** — nowhere else.
2. The parent holds only its own term data; a complex term is its own concept
   and its translation is never assembled from component translations.
3. `_metadata.componentLookups` is **removed from the schema**; enrichment
   scripts may use lookup results in memory but persist them only into
   component concepts (create-if-missing).
4. The validator enforces referential integrity — a broken reference is a
   visible error, not silent rot.

Partially reverses Issue #13 Decision 3 / old Decision 17 Part 4: the
"store lookups once in the parent" rationale predated component concepts;
copy-on-create then produced 2+ copies with no declared master.

Standards basis: concept orientation (one concept, one entry); definitions at
concept/language level of the concept's own entry (V4 §6.5); relations via
`crossReference` (V4 §6.2); component markup is not part of TBX-Basic at all.

---

## Decision MUST 3 — Status: single source of truth, derived export status, renames (2026-08-22)

1. **`workflow` is the single source of truth for term status. The TBX status
   is NOT stored** — the export script derives it (DRY, one shared function).
   Old stored `administrativeStatus` is removed from the schema.
2. **Derivation rules (→ V4 `usageStatus`):**
   - `supersededBy` set → `deprecated` + crossReference to the replacement
   - review `rejected` → `deprecated`; `rejectedReason` exports as note
   - review `approved` → `preferred`
   - `candidate` / no workflow → **usageStatus omitted** + note
     "Candidate — awaiting ATL review"
   - EN glossary terms (no workflow) → `preferred`
3. **Renames (V4 name collision + context-rich, organisation-neutral naming):**
   - `workflow.atlStatus` → **`workflow.communityReviewStatus`**
     (`candidate` / `approved` / `rejected`)
   - `workflow.usageStatus` → **`workflow.communityTextUsage`**
     (`in_use` / `not_in_use` / `formerly_in_use`)
   - Rationale: V4 took the name `usageStatus` for its standard field; and
     organisation abbreviations go stale — ACA itself is transitioning to
     ACAD (2026 ABC, phased 5–10 years). "community" fits every future
     community (Milestone 4). Value prefixes (`atl_`) dropped.
4. Issue #13 Decision 2 (Variant C — review decision and text usage as two
   separate facts) is reaffirmed; `communityTextUsage` never affects the
   derived export status. TBX export is one-way: CAT tools send no usage data
   back; usage tracking remains our own process (text analysis, M3).

---

## Decision SHOULD 1 — Part-of-speech quality: cooperation contract with hard gates (2026-08-22)

**Master invariant: no faulty data ever leaves the extraction/derivation
stage.**

1. **Program:** closed-vocabulary parser splits the raw source marker
   (`grammaticalType`, e.g. "v, idiom, informal") into three homes:
   PoS → `partOfSpeech`; idiom/saying → `termType: "phrase"`; register →
   `note`. Unknown tokens fail loudly to needs-human state; multi-PoS combos
   (e.g. "adj, n") go to human decision. Auto-derivation recorded in
   `transactions`.
2. **Human (M1 work):** fill the 17 empty entries, resolve flagged cases —
   including splitting merged homonyms into separate concepts (finite source,
   splits will not recur in bulk) — and verify; recorded in `transactions`.
   Phase 2 enrichment cross-checks against Sõnaveeb (which supplies PoS for
   ET terms under the same rules).
3. **Schema fix:** `partOfSpeech` ∈ {noun, verb, adjective, adverb,
   properNoun, other} (+ null until the gate). "phrase" removed (wrong axis);
   pronoun/preposition/conjunction → `other`.
4. **Two hard gates:** OPTIONAL→REQUIRED flip only at zero empty/unverified;
   TBX export refuses to run if any exported term lacks PoS (V4 §9).
5. **Forward rule (M2 CLI, M3 platform):** every entry point enforces closed
   vocabularies at input time ("computer says no"); one shared validation
   ruleset serves extraction, review, and manual entry.

**Census instead of pilot:** current data (334 entries) has 317 (94.9%) raw
markers present, 17 (5.1%) empty — below the critique's 10% alarm threshold.
The old "826/826 null" came from the deprecated pipeline.

---

## Decision SHOULD 2 — Orthogonal axes; termComplexity computed, not stored (2026-08-22)

1. The "at ease" collision never was one: with "phrase" moved to `termType`,
   three independent axes remain — *structure* (multiword: mechanical string
   fact), *form* (`termType`), *grammar* (`partOfSpeech`). The validator
   raises **no cross-field errors**; no hierarchy of definition is needed.
2. **`_metadata.termComplexity` is removed as a stored field** — pure
   derivation (word count), computed on demand by a shared function.
   Real-world verification: TBX has no complexity data category in any
   version; IATE (8M terms) manages multiword terms with no such field.
3. Consequences: the deferred "rename to structuralComplexity" question
   dissolves; the split rule can mature without migrations (hyphen handling,
   e.g. "self-esteem", deliberately still open); Issue #15 resolved;
   DECISIONS.md's old 3-value statistics to be cleaned up.

---

## Decision SHOULD 3 — Component sync dissolved; componentTerms computed (2026-08-22)

1. **`_metadata.componentTerms` is NOT stored** — pure derivation (whitespace
   split of the parent term), computed on demand by the same shared function
   (refines the MUST 2 comment's wording; the reference model is unchanged).
2. Component concepts are fully editable, never read-only; nothing flows back
   to the parent (it stores no component content).
3. Creation is one-time and one-directional during M1 Phase 2 enrichment
   (create-if-missing, recorded in `transactions`); `derivedFrom` stays
   stored — it is provenance (original data), not a derivable mirror.
4. Validator: every component word **that the enrichment rule designates**
   must resolve to an existing component concept. Which words qualify
   (function words like "of"/"at"? only words with dictionary hits?) is an
   **open Phase 2 design question** — old "no stop-word filtering" stance
   will be revisited then.

No sync engine, no refresh flags — the "multiverse of truths" was a property
of the copy model, not of the data.

---

## Consolidated export mapping table (JSON → TBX-Basic V4)

| JSON (internal master) | TBX-Basic V4 export | Basis |
|---|---|---|
| concept | `conceptEntry id="…"` | core |
| `languages.xx` | `langSec xml:lang="xx"` | §6.10 |
| term | `termSec` → `term` | §6.19 |
| `subjectField` | `descrip type="subjectField"` (concept level) | §6.18 |
| language-level `definition` | `descrip type="definition"` (language level) | §6.5 |
| `partOfSpeech` | `termNote type="partOfSpeech"` — **mandatory per exported term** (export refuses otherwise) | §6.12, §9 |
| `termType` (fullForm/acronym/…/phrase) | `termNote type="termType"` | §6.21 |
| `workflow.communityReviewStatus` | `termNote type="usageStatus"`: approved→`preferred`; rejected→`deprecated`; candidate→**omitted** + note "Candidate — awaiting ATL review"; EN glossary terms→`preferred` | §6.23 |
| `supersededBy` | `deprecated` + `ref type="crossReference"` to the replacing term | §6.23, §6.2 |
| `workflow.rejectedReason` | `note` on the term | §6.11 |
| register info (informal, slang, …) | `note` | §6.11 |
| `usageExamples.enContext` / `.etTranslation` | `descrip type="context"` on the EN / ET term; example source via `descripGrp` + `admin type="source"` | §6.1, §6.15 |
| `source` object | `admin type="source"` flattened to one string; full structure stays in JSON | §6.17 |
| `transactions` (type, responsibility, date) | `transacGrp`; **`origination` exports as `creation`** | §6.22, §7.1–7.3 |
| component / seeAlso relations (computed from `derivedFrom` / stored seeAlso) | `ref type="crossReference"` | §6.2 |
| root `metadata` | `tbxHeader`: `titleStmt` + `publicationStmt`/`sourceDesc` free text | App. B |
| people (addedBy, approvedBy, responsibility) | back-matter `respPerson` registry; transaction responsibility references person ids. **Privacy: name + role only; e-mail only with consent** | §7.4, §6.14 |
| `translatorNote`, `communityTextUsage`, `actionType`/`actionDescription`/`statusChange`, `isGlossaryTerm`/`termType`(origin)/`addedReason` | **not exported** (JSON-only by design) | — |

---

## Open sub-questions carried forward (deliberate, not forgotten)

1. **Text vs ID references** (`derivedFrom`, `supersededBy`): text references
   break silently on rename — unacceptable; robust solution needed (IDs, or
   script-managed renames + validator referential checks). Decide before the
   migration script.
2. **Which component words deserve concepts** (stop-words, dictionary-hit
   filtering) — Phase 2 enrichment design.
3. **Hyphenated terms** ("self-esteem"): current whitespace rule calls them
   single-word; ISO 1087 calls them compounds — revisit when the shared
   split function is written.
4. **V4 Appendix B detailed walkthrough** — done during MUST 1 (file
   skeleton + element map); revisit at export-script design.
