# TBX M1 Critical Review — Draft Analysis (Claude, Fable 5)

**Status:** DRAFT — working material only, NOT confirmed decisions.
**Date:** 2026-08-18, revised 2026-08-21 (TBX-Basic Version 4 findings)
**Purpose:** Full analysis of the 6 M1-critical open questions from
[TBX_M1_CRITICAL_REVIEW.md](TBX_M1_CRITICAL_REVIEW.md) (3 MUST + 3 SHOULD).
Confirmed decisions go to GitHub Issue #44 as comments; this file can be deleted
after all 6 are confirmed there.

**Revision note (2026-08-21):** After the first draft was written, we discovered
that TerminOrgs published **TBX-Basic Version 4 in November 2025** — a full,
free, 21-page prose specification that supersedes the v1.2.1 dialect package the
first draft cited, and closes the "no core prose available" gap (see
[TBX_VERSIONS.md](TBX_VERSIONS.md) for the version landscape and file
locations). This revision updates citations and adds V4-specific findings. It
also adds a new sub-decision to MUST 1: **which specification version the
project targets.** Citations below name the version explicitly: "v1.2.1" =
module files now in `deprecated/TBX-Basic_v1.2.1/`; "V4" = `TBX-Basic-V4.pdf`
(local file; download URL in TBX_VERSIONS.md).

**Scope note:** The 2 "CAN defer to M2" questions (Export Degradation Strategy,
Structural Complexity Naming) are intentionally NOT analysed here, per the review
document's own priority grouping.

---

## 0. What the standard actually is (evidence base for all citations)

Before the questions, one honest correction about the source material itself.

Issue #44 describes `TBX-Basic_Definition_v1.2.1.pdf` as "~50+ A4". **It is a
single page.** It is the dialect definition sheet, and its entire normative
content is:

> "Core: Core. Additional Required Module(s): Min, Basic. Use TermComp module:
> False." (TBX-Basic_Definition_v1.2.1.pdf, p. 1)

TBX-Basic v1.2.1 is therefore defined as: the TBX core structure (ISO 30042:2019)
plus exactly two data category modules, whose full definitions are in the same
downloaded package:

- `TBX-Basic_v1.2.1/Modules/TBX_min_module/Min Module Definition.pdf` (1 page)
  and machine-readable `Min.tbxmd`
- `TBX-Basic_v1.2.1/Modules/TBX_basic_module/Basic Module Definition.pdf`
  (2 pages) and machine-readable `Basic.tbxmd`
- Validation files: `DCA/TBX-Basic_DCA.sch`, `DCT/TBX-Basic_DCT.sch`,
  core RNG (referenced), plus a valid example file
  `DCA/Example_Astronomy_DCA_VALID.tbx`

All citations below are to these files. Where the ISO 30042:2019 core text itself
would be needed (we do not have the ISO document locally, only the RNG/schematron
derived from it), I say so explicitly rather than pretending to cite it.

**Update 2026-08-21:** the core-prose gap is now largely closed. TBX-Basic
**Version 4** (TerminOrgs, Nov 2025) includes the entry structure rules in prose
(V4 §7) and the complete list of permitted XML elements (V4 Appendix B), plus
the core structure schemas are freely published by ISO (TR 24633-2 Annex A, in
`iso-tr24633-2-schemas/`). Key V4 changes relative to v1.2.1 that affect the
questions below:

- `administrativeStatus` (4 values, `-admn-sts` suffixes) is **replaced by
  `usageStatus`** with values `preferred` / `admitted` / `deprecated` — no
  "superseded" value, and only one value per term (V4 §6.23).
- transactionType values are now `creation` / `modification` (was
  `origination` / `modification`) (V4 §6.22).
- partOfSpeech picklist is now noun, verb, adjective, adverb, **properNoun**,
  other (V4 §6.12) — still **no "phrase"**.
- **Part of speech is mandatory per term section for any resource used in
  automated processing (CAT tools);** for human-only resources it may be
  omitted if a definition or context is present (V4 §9).
- `transacGrp` contains one `transac` plus `transacNote` and/or `date` — and
  nothing else (V4 §7.1–7.3). This settles a point the first draft had to mark
  as interpretation: there is no slot for a free-text note inside a transaction
  group.
- Compliance is defined explicitly: a resource complies only if it "uses only
  the DCs that are defined in this document" and validates against
  core schema + basic_schema.sch (V4 §9).

**The complete, closed list of TBX-Basic data categories** (Min.tbxmd +
Basic.tbxmd):

| Category | Kind | Levels | Values |
|---|---|---|---|
| administrativeStatus | termNote | term | preferred/admitted/deprecated/superseded `-admn-sts` |
| partOfSpeech | termNote | term | adjective, noun, other, verb, adverb |
| subjectField | descrip | conceptEntry | string |
| customerSubset | admin | conceptEntry, termSec | string |
| definition | descrip | conceptEntry, langSec | noteText |
| context | descrip | termSec | noteText |
| source | admin | conceptEntry, langSec, termSec | string |
| crossReference | ref | conceptEntry, termSec | string |
| externalCrossReference | xref | conceptEntry, termSec | string |
| projectSubset | admin | conceptEntry, termSec | string |
| termType | termNote | term | fullForm, acronym, abbreviation, shortForm, variant, **phrase** |
| transactionType | transac | all 3 levels | origination, modification |
| responsibility | transacNote | all 3 levels | string |
| grammaticalGender, geographicalUsage, termLocation, xGraphic | termNote/xref | (see Basic.tbxmd) | — |

Plus core-structure elements: `conceptEntry` (id), `langSec` (xml:lang),
`termSec` (term), `note`, `transacGrp`, `date` (seen in the valid example file).

Two facts from this table drive several answers below (both confirmed unchanged
in V4):

1. **partOfSpeech has NO "phrase" value** — but termType DOES have "phrase"
   (v1.2.1: Basic.tbxmd; V4: §6.12 and §6.21).
2. **Term decomposition markup is excluded.** The v1.2.1 dialect sheet states
   "Use TermComp module: False"; V4's closed permitted-element list (Appendix B)
   likewise contains no component markup. Component relationships can only be
   expressed as separate concepts linked with `crossReference` (V4 §6.2: concept
   level points to another entry's concept ID, term level to a term ID in
   another entry).

---

## MUST 1 — TBX Standard Compliance Audit (are `workflow` and `_metadata` legal?)

### Problem

Decision 18 (Issue #14) claims "100% TBX-Basic compliance". The critique asks:
are the custom objects (`workflow`, `_metadata`, `usageExamples`,
`transactions.actionType`, root `metadata`) legally permitted in TBX-Basic, or
will CAT tools reject the files or silently scrub them?

### Sub-decision (new, 2026-08-21): which specification version do we target?

The schema decisions (Oct 2025) were made against the v1.2.1 dialect package;
TerminOrgs published Version 4 in Nov 2025. The export target must name one.

**Option V4 (recommended):** current TerminOrgs specification; free full prose
spec; simpler status values; clear compliance rules (§9); validation files in
the repo (`TBX-Basic-V4-files/`, `iso-tr24633-2-schemas/`).
- Minus: newest version — CAT-tool support may lag (worth one verification test
  in M2 against Trados/memoQ import; the Trados 2024 manual is in
  `research/terminology_normalization/`). Renames touch our schema enums
  (see MUST 3, SHOULD 1).

**Option v1.2.1:** what the schema was written against; era-matched to ISO
30042:2019 tooling.
- Minus: superseded by its own publisher; 1-page definition + module files only
  (no prose spec); keeps the clunkier `administrativeStatus` values.

Since our JSON is the master and TBX is an export projection (see below), this
choice mostly affects the **export mapping and enum spellings**, not the
architecture — which also means it is cheap to decide now and revisit in M2 if
CAT-tool testing surprises us.

### What the standard says

TBX-Basic is a **closed dialect**: core + Min + Basic modules, nothing else
(TBX-Basic_Definition_v1.2.1.pdf, p. 1). V4 states it directly in its
compliance clause: a resource is compliant only if it "uses only the DCs that
are defined in this document" and only the elements in the Appendix B list
(V4 §9, Appendix B). There is no extension mechanism inside TBX-Basic. A TBX
file containing a `workflow` or `_metadata` data category would fail schematron
validation and would simply not be a TBX-Basic file. So:

- **As a claim about a TBX file:** "workflow and _metadata are TBX-Basic
  compliant" would be FALSE.
- **But our database is not a TBX file.** It is JSON. TBX-Basic defines an XML
  exchange format; it says nothing about how you store data internally. The
  meaningful, honest claim is: *"the JSON database is losslessly mappable to
  TBX-Basic; custom fields are internal-only and are mapped or dropped at
  export."* The current wording ("100% compliant", `metadata.standard:
  "TBX-Basic v1.2.1 + ACA workflow custom fields"`) blurs this.

The critique's fear ("CAT tools silently scrub custom metadata") is thus
half-right: anything without a standard slot **will** vanish in export. The fix
is not to delete the custom fields but to know exactly which ones have a
standard home. From the table in §0:

| Our field | Standard home at export (v1.2.1 → V4) | Citation |
|---|---|---|
| workflow.atlStatus | administrativeStatus (Decision 10 mapping) → **usageStatus** (preferred/admitted/deprecated) | Min.tbxmd; V4 §6.23 |
| workflow.rejectedReason | `note` on the term (both versions) | V4 §6.11: note at concept/language/term |
| usageExamples.enContext / etTranslation | `context` (descrip, termSec) on the EN / ET term (both versions) | Basic.tbxmd; V4 §6.1 |
| source object | `admin type="source"` (flattened to string); V4 also defines nesting in `descripGrp` for definition/context sources | Basic.tbxmd; V4 §6.15–6.17 |
| transactions (type, responsibility, date) | `transacGrp`; type value `origination` must be exported as `creation` if V4 targeted | Basic.tbxmd; V4 §6.22, §7.1–7.3 |
| transactions.actionType / actionDescription / statusChange | no slot — drop at export (history stays in JSON master); confirmed: `transacGrp` admits no note | V4 §7.1–7.3 |
| root `metadata` | `tbxHeader/fileDesc` (free-text `<p>`) | example file; V4 Appendix B step 3 |
| metadata.project | `projectSubset` (admin, conceptEntry/termSec) if wanted per-entry | Basic.tbxmd; V4 §6.13 |
| supersededBy | v1.2.1: `supersededTerm-admn-sts`; **V4 has no superseded value** — export as `deprecated` + term-level `crossReference` to the replacing term, or note | V4 §6.23, §6.2 |
| `_metadata.*` (all 7 fields) | no slot — internal only (componentTerms partially via crossReference, see MUST 2) | V4 §9, Appendix B |

Interesting detail: JSON_SCHEMA_SPECIFICATION.md §6.1 lists `context` as "Not
implemented (implemented via custom usageExamples)". In reality usageExamples'
core payload maps cleanly onto standard `context` — so this data is NOT doomed
to vanish, contrary to the critique's worry. Only translatorNote extras would
drop.

### Options

**Option A — Reframe the claim + adopt an export mapping table (recommended).**
Keep the JSON structure. Change the compliance language everywhere ("TBX-Basic
compliant" → "TBX-Basic exportable / TBX-Basic-mappable"), adopt the mapping
table above as the M1 decision, and leave writing the actual export script to M2
(that is the deferred "Export Degradation Strategy" question — the M1 decision
is only *that* the mapping exists and *what* it is).
- Plus: honest, zero rework of data; every fear in the critique gets a concrete
  answer; CAT tool import works on the exported subset.
- Minus: requires touching wording in spec/DECISIONS.md/schema `standard` string.

**Option B — Restrict the schema to pure TBX-Basic categories only.**
- Plus: trivially exportable.
- Minus: loses the entire ATL review workflow, usage tracking, audit extras —
  the reason this database exists. Rejected by project goals.

**Option C — Define a custom TBX dialect (ISO 30042:2019 permits new dialects
with own modules).**
- Plus: theoretically fully standard.
- Minus: heavy (write .tbxmd modules + schematron), and no CAT tool would
  support the custom dialect anyway — you'd still export TBX-Basic for tools.
  Over-engineering for M1; could be revisited in M3/M4 if ever needed.

### Honest verdict

The architecture is fine; the **claim** was overstated. Decision 18's "100%
compliance" verification checked that all TBX-Basic required/recommended fields
are *present in our schema* — it never checked (and could not, from the 1-page
PDF) whether our extras are *permitted in a TBX file*. They are not, and that's
OK, as long as we say "exportable" instead of "compliant" and fix the small
genuine deviations found below (partOfSpeech enum — see SHOULD 1/2).

---

## MUST 2 — Atomic Concept Architecture for Components

### Problem

Decision 17 Part 4 (+ Issue #13 Decision 3) stores dictionary lookups for
component words inside the **parent** concept's `_metadata.componentLookups`.
Spec Example 3 additionally creates a separate concept per component whose
`definition` is **copied from** the parent's componentLookups. Critique: violates
concept atomicity; component data is "held hostage" inside the parent; a future
Finnish translation of "addictive" has no clean place to go.

### What the standard says

- One concept = one `conceptEntry`; a concept's definitions live in its own
  entry at conceptEntry or langSec level (Basic.tbxmd; V4 §6.5). V4 adds a
  best-practice note that a termbase should even **choose a single definition
  level** and stick to it (V4 Appendix A note). There is no mechanism for entry
  X to carry entry Y's definitions.
- Term-decomposition markup is excluded in both versions ("Use TermComp module:
  False", v1.2.1 dialect sheet; no component elements in V4's Appendix B list).
  The only standard way to relate parent and component concepts is
  `crossReference` — concept level pointing to another entry's concept ID, term
  level to a term's ID in another entry (Basic.tbxmd; V4 §6.2, §7.1, §7.3).
- Consequence: `componentLookups` has no export path at all; it is invisible to
  any standard consumer.

### The internal contradiction (worth stating plainly)

Issue #13 Decision 3 chose the hybrid "to avoid duplication". But spec Example 3
then copies definitions from parent componentLookups into the component
concepts. **Both copies now exist** — the original anti-duplication rationale no
longer holds. After any later edit to the component concept, the parent's copy
is stale. The critique's "single source of confusion" is factually correct
about the design as specified. This is a case where an old decision is
genuinely at odds with the standard's concept orientation — age doesn't make it
right, and the original justification has been silently invalidated by a later
decision.

### Options

**Option A — Component concept is the single home (recommended).**
Component lookup data (definitions, ET candidate variants with sources) is
written **directly into the component's own concept**: definitions at language
level, candidate translations as terms with their `source` objects (standard
slot: admin source at termSec — Basic.tbxmd). Parent keeps only
`_metadata.componentTerms` (list of words, auto-regenerable from the term
string). Component keeps `derivedFrom` (already in schema). Drop
`componentLookups` from the schema entirely; enrichment scripts may use such a
structure in memory while running, but never persist it.
- Plus: atomic, TBX-exportable (definitions + sources land in standard slots;
  parent↔component linkable via crossReference at export), scalable to new
  languages, kills the duplication and the sync problem (see SHOULD 3).
- Plus: cheapest moment ever — the migration script to the final TBX structure
  has NOT been written yet, and no component concepts have been generated in
  data. This is a spec/schema edit, not a data migration.
- Minus: schema + spec Example 3 need updating; formatVersion bump.

**Option B — Keep componentLookups as a persistent cache, declare component
concept authoritative.** Validator flags divergence.
- Plus: enrichment scripts keep a convenient read location.
- Minus: still duplicated, still non-exportable, now plus a validator rule and a
  staleness concept. Complexity without benefit over A.

**Option C — Status quo.**
- Minus: duplication with no declared master; invisible to export; multi-language
  scaling blocked. Rejected.

### Honest verdict

The critique is right. Option A. This reverses part of Issue #13 Decision 3 —
explicitly acknowledge that in the #44 comment so the history is clean.

---

## MUST 3 — Automated Status Synchronisation

### Problem

Dual status: standard `administrativeStatus` (REQUIRED) and custom
`workflow.atlStatus`/`usageStatus`. Undecided whether workflow changes
automatically drive administrativeStatus, or humans maintain both. Risk:
a term "rejected" in workflow still showing "preferredTerm-admn-sts".

### What the standard says

The status field is an optional term-level picklist in both versions
(v1.2.1: `administrativeStatus`, 4 values; V4: **`usageStatus`** with
`preferred` / `admitted` / `deprecated`, exactly one value per term — V4 §6.23).
Only `term` itself is required at termSec. **The standard says nothing about
synchronisation with external workflow state** — this is a data-engineering
decision, not a compliance one. My interpretation, stated as such: since
Decision 10 already defines a deterministic ATL→TBX mapping, storing two
independently editable copies of derivable information is redundant data — a
textbook desync source.

**V4 complication worth deciding consciously (new):** V4 renamed the standard
field to `usageStatus` — which **collides with our custom
`workflow.usageStatus`** (not_in_use / atl_in_use / formerly_in_use). Two
different meanings, one name. If we target V4, I recommend renaming our custom
field (e.g. `workflow.atlUsage` or `workflow.textUsage`) to prevent permanent
confusion; the rename is cheap now (migration script not yet written). This
touches the deferred M2 naming question but cannot wait for M2 if V4 is the
target.

The mapping needs one completion to be fully deterministic (proposed; V4 value
names, v1.2.1 equivalents in brackets):

1. `supersededBy` set → `deprecated` + crossReference to replacing term
   [v1.2.1: `supersededTerm-admn-sts`]
2. else `atlStatus = rejected` → `deprecated` [`deprecatedTerm-admn-sts`]
3. else `atlStatus = atl_approved` → `preferred` [`preferredTerm-admn-sts`]
4. else (candidate / no workflow) → `admitted` [`admittedTerm-admn-sts`]
   - exception: EN glossary terms (isGlossaryTerm true, no workflow) →
     `preferred` (WSO's own term is by definition the preferred EN form)

Note our custom usage-tracking field (`workflow.usageStatus`, possibly renamed
per above) deliberately does NOT affect the derived standard status — usage is
a fact, not an approval judgement (consistent with Issue #13 Variant C
"de facto vs de jure" reasoning).

### Options

**Option A1 — Don't store administrativeStatus at all; compute at export/display.**
- Plus: desync structurally impossible.
- Minus: JSON no longer self-describing for a human reader; every consumer must
  know the mapping; schema REQUIRED field removed (major version bump).

**Option A2 — Store it, but only scripts write it (recommended).**
administrativeStatus stays in the JSON, but is **derived**: every save/update
recomputes it from the rules above; the validator errors on any mismatch. Humans
edit only `workflow` (+ `supersededBy`).
- Plus: single source of truth (workflow) with the standard field still visible
  in the data; validator makes silent drift impossible; matches "rigid,
  unidirectional automated inheritance" that the critique asks about; no schema
  shape change at all.
- Minus: rule must live in one shared function (utils) so all scripts agree.

**Option B — Two independent fields + humans keep them aligned, validator only
warns.**
- Minus: this is exactly the desync scenario the critique predicts. Rejected.

### Honest verdict

Option A2. One sentence for the #44 comment: *administrativeStatus is a derived
field; workflow (+ supersededBy) is authoritative; derivation rule 1–4 above;
validator enforces.*

---

## SHOULD 1 — Data Quality Gate for Part of Speech

### Problem

Decision 6: partOfSpeech OPTIONAL in Phase 1, REQUIRED in Phase 3. Critique:
run a ~50-term pilot now to measure the null rate; >10% nulls means heavy data
debt and a Phase-3 crash risk.

### Reality check (the pilot already happened, at full scale)

Issue #6's implementation note: **826/826 senses were created with
`part_of_speech: null`.** The source .docx has no systematic PoS markers; only a
subset carries "(n.)", "(v.)", "(to)" markers, preserved in notes during
normalization (Issue #4, aggressive normalization). So the failure rate of the
raw source is already known — effectively 100% unfilled as structured data. A
50-term pilot would tell us nothing new. The real decision is what the Phase-3
promise means, and there is also a genuine standards bug in the enum.

### Standards findings (this part is new information)

partOfSpeech picklist — v1.2.1: `adjective, noun, other, verb, adverb`
(Min.tbxmd); V4: `noun, verb, adjective, adverb, properNoun, other` (V4 §6.12).
Our schema enum: `noun, verb, adjective, adverb, phrase, null`. Deviations:

1. **"phrase" is not a legal TBX-Basic partOfSpeech value in either version.**
   The standard handles multiword items via **termType = "phrase"**
   (Basic.tbxmd; V4 §6.21). Exporting partOfSpeech="phrase" would fail
   validation (V4 ships a test file for exactly this error:
   `TBX-Basic-sample-badPOS.tbx`).
2. **"other" is missing from our enum** — the standard's own escape hatch,
   which we will need for edge cases ("at ease"). If V4 is targeted,
   `properNoun` is also worth adding (useful for names like "ACA WSO").

3. **V4 gives the quality gate normative teeth (V4 §9):** a resource used in
   automated processing (CAT tools — our declared M2+ goal) is compliant only
   if **every term section has an explicit part of speech**; a human-only
   resource may omit it where a definition or context exists. So "fill
   partOfSpeech before CAT export" is no longer just good practice — it is the
   compliance boundary itself.

### Options

**Option A — Keep phased plan, add a measurable gate + fix the enum
(recommended).**
- Enum fix now: partOfSpeech ∈ {noun, verb, adjective, adverb, other, null}
  (+ properNoun if V4 targeted); multiword items get termType:"phrase" instead.
  Zero-cost today because every stored value is null (nothing to migrate).
- Phase 2 enrichment (marker extraction + Sõnaveeb + manual review) proceeds as
  planned (Decision 6 already sketches it).
- The gate: Phase 3 (REQUIRED flip) only after validator reports 0 nulls;
  the flip script from Decision 6 already implements exactly this check.
- Plus: unblocks nothing/blocks nothing; converts vague "data debt" fear into
  one number the validator prints.
- Minus: none of substance.

**Option B — Make partOfSpeech REQUIRED now.** Blocks all 826 terms. Rejected.

**Option C — Abandon the Phase-3 REQUIRED promise.** Simpler, but gives up ISO
704 alignment ambition and homonym support quality. Not recommended, and not
necessary — the gate in A already protects against a premature flip.

### Honest verdict

Option A. The critique's pilot recommendation is moot (full-scale numbers
exist); its underlying worry (crash at Phase 3) is already answered by Decision
6's own verification script. The actionable new items are the two enum fixes.

---

## SHOULD 2 — Linguistic vs Structural Conflict Resolution ("at ease")

### Problem

Decision 17 (word count → termComplexity) vs Decision 6 (partOfSpeech).
"at ease": mechanically "complex", grammatically a "phrase". Critique asks for a
hierarchy of definition and whether the validator should error.

### What the standard says

The standard itself dissolves this collision, because it never puts "phrase"
in partOfSpeech at all:

- partOfSpeech = grammatical category, picklist without "phrase" (Min.tbxmd;
  V4 §6.12);
- termType = form of the term, picklist **with** "phrase" (Basic.tbxmd;
  V4 §6.21 — V4 even ships error samples for termType misuse);
- structural complexity (ISO 1087 simple/complex term) has no TBX-Basic data
  category — our termComplexity is a custom, mechanical, auto-generated fact.

So "at ease" cleanly becomes three orthogonal statements:
`termComplexity: "complex"` (it contains a space — mechanical fact),
`termType: "phrase"` (its form — standard slot),
`partOfSpeech: "other"` (or "adverb" if the reviewer prefers precision —
grammatical function; "other" is the standard's own value for this).

The perceived conflict existed only because our schema misused partOfSpeech to
carry "phrase". With the SHOULD-1 enum fix, there is nothing left to collide.

### Hierarchy of definition (proposed rule for the validator)

1. **termComplexity** — mechanical, auto-generated from the term string, never
   edited by humans, makes no linguistic claim. (Validator: must equal what the
   generator function returns — that's the only check.)
2. **termType** — form classification, standard picklist, human-set.
3. **partOfSpeech** — grammatical category, standard picklist, human-set.

No cross-field error states: complex + any partOfSpeech + any termType may
coexist. The validator never adjudicates linguistics; it only enforces enums
and the auto-generation identity for termComplexity.

### Options

**Option A — Orthogonal-axes rule above, no cross-field validator errors
(recommended).** Depends on the SHOULD-1 enum fix.

**Option B — Validator error when termComplexity="complex" and partOfSpeech is
a single-word category.** Rejected: "adult child" is complex AND legitimately a
noun — this rule would flag correct data constantly (data noise, the exact
thing the critique fears, but caused by the validator itself).

**Option C — One field takes precedence over the other.** Meaningless — they
measure different dimensions; precedence implies they compete, which they don't
once "phrase" moves to termType.

### Honest verdict

Option A. Note for later (M2, deliberately not decided now): the deferred
"rename termComplexity → structuralComplexity" question becomes even more
sensible under this rule, and DECISIONS.md still shows the old 3-value
simple/complex/compound statistics while the schema has 2 values (hyphenated
"self-esteem" now counts as "simple" — 1 whitespace-token). Worth a cleanup
note in #44, but not an M1 decision.

---

## SHOULD 3 — Component Sync Directionality

### Problem

Parent → child data flow is defined (componentLookups → component concept
definition), reverse is not. Are children read-only? Does a child edit raise a
"needs refresh" flag on the parent? Risk: "multiverse of truths".

### Analysis

This question only exists because of the MUST-2 duplication. Under MUST-2
Option A (component concept is the single home, parent holds no copy), there is
**nothing to synchronise**:

- Component concept: the only editable home of component data (definitions,
  candidate translations, workflow, future Finnish/Slovak sections).
- Parent `_metadata.componentTerms`: a derived list of words, regenerated from
  the parent term string by the same auto-generation function — never edited.
- Component `derivedFrom`: set at generation; only changes if a parent term
  itself is renamed (rare, script-handled, logged as a transaction).
- Generation is one-directional and one-time: parent term string → create
  component concepts if missing (transaction actionType "enriched"/"originated"
  records this). After birth, components live their own life; nothing flows
  back to the parent, because the parent no longer stores component content.

The standard has no position on any of this (internal workflow); the relevant
standard constraint is only that each concept owns its data (see MUST 2
citations) — which this rule satisfies. My interpretation, stated as such.

### Options

**Option A — Resolve by MUST-2A; adopt the "single home, one-way generation at
birth" rule; no sync machinery (recommended).**
- Plus: zero moving parts; the "multiverse of truths" cannot arise because
  there is exactly one truth location per concept.

**Option B — Transaction-log "needs refresh" flags between parent and child.**
- Minus: builds a mini synchronisation engine for a problem Option A deletes.
  Over-engineering for M1 (and for M2, frankly).

**Option C — Children read-only forever.**
- Minus: directly contradicts the scalability goal that motivated MUST 2 (a
  Slovak translator must be able to enrich "addictive"). Rejected.

### Honest verdict

Option A. If Anne chooses differently on MUST 2 (keeps a persistent parent
cache), then this question reopens and Option B's flag becomes the least-bad
choice — but the clean fix is upstream.

---

## Summary table (for the walkthrough)

| # | Question | Recommendation | Reverses an old decision? |
|---|---|---|---|
| M1 | Compliance audit | A: reclaim as "TBX-Basic exportable" + adopt export mapping table | Rewords Decision 18's claim; keeps architecture |
| M1a | Target spec version (new) | V4 (Nov 2025); one CAT-import sanity test in M2 | Updates the version the Oct 2025 decisions assumed |
| M2 | Atomic components | A: component concept = single home; drop componentLookups | Partly reverses Issue #13 Decision 3 / Decision 17 Part 4 |
| M3 | Status sync | A2: standard status field derived, script-written, validator-enforced; if V4: values preferred/admitted/deprecated + rename custom workflow.usageStatus (name collision) | Tightens Decision 10; renames one Decision 10 field |
| S1 | PoS quality gate | A: keep phased plan + 0-null gate; fix enum (drop "phrase", add "other" (+properNoun if V4)); V4 §9 makes PoS mandatory for CAT use | Amends Decision 6 enum |
| S2 | Linguistic vs structural | A: orthogonal axes; "phrase" moves to termType; no cross-field errors | Amends Decision 6/17 interaction; resolves Issue #15's question |
| S3 | Component sync | A: single home + one-way generation at birth; no sync engine | Follows from M2 |

Cross-cutting root cause, honestly stated: most of the MUST-level anxiety traces
to one overstated phrase — "100% TBX-Basic compliant" — made from summary
documents without the module definitions in hand. Once the claim is corrected to
"TBX-Basic exportable", Q-M1 resolves by wording + mapping table, and the two
real design defects that remain (component duplication, dual-status drift) have
cheap fixes because the migration script was never written.
