# TBX M1 Critical Review — Draft Analysis (Claude, Fable 5)

**Status:** DRAFT — working material only, NOT confirmed decisions.
**Date:** 2026-08-18
**Purpose:** Full analysis of the 6 M1-critical open questions from
[TBX_M1_CRITICAL_REVIEW.md](TBX_M1_CRITICAL_REVIEW.md) (3 MUST + 3 SHOULD).
Confirmed decisions go to GitHub Issue #44 as comments; this file can be deleted
after all 6 are confirmed there.

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

Two facts from this table drive several answers below:

1. **partOfSpeech has NO "phrase" value** — but termType DOES have "phrase"
   (Basic.tbxmd, termType picklist; Basic Module Definition.pdf, p. 2).
2. **"Use TermComp module: False"** — TBX-Basic explicitly excludes the ISO
   30042 module for term decomposition. Component relationships can only be
   expressed as separate concepts linked with `crossReference`.

---

## MUST 1 — TBX Standard Compliance Audit (are `workflow` and `_metadata` legal?)

### Problem

Decision 18 (Issue #14) claims "100% TBX-Basic compliance". The critique asks:
are the custom objects (`workflow`, `_metadata`, `usageExamples`,
`transactions.actionType`, root `metadata`) legally permitted in TBX-Basic, or
will CAT tools reject the files or silently scrub them?

### What the standard says

TBX-Basic is a **closed dialect**: core + Min + Basic modules, nothing else
(TBX-Basic_Definition_v1.2.1.pdf, p. 1). There is no extension mechanism inside
TBX-Basic. A TBX file containing a `workflow` or `_metadata` data category would
fail schematron validation and would simply not be a TBX-Basic file. So:

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

| Our field | Standard home at export | Citation |
|---|---|---|
| workflow.atlStatus | administrativeStatus (mapping already in Decision 10) | Min.tbxmd picklist |
| workflow.rejectedReason | `note` on the term | core; seen in valid example |
| usageExamples.enContext / etTranslation | `context` (descrip, termSec) on the EN / ET term | Basic.tbxmd: context, termSec, noteText |
| source object | `admin type="source"` (flattened to string) | Basic.tbxmd: source, all levels |
| transactions (type, responsibility, date) | `transacGrp` | Basic.tbxmd: transactionType, responsibility; example file |
| transactions.actionType / actionDescription / statusChange | no slot — drop at export (history stays in JSON master) | — |
| root `metadata` | `tbxHeader/fileDesc` (free-text `<p>`) | example file header |
| metadata.project | `projectSubset` (admin, conceptEntry/termSec) if wanted per-entry | Basic.tbxmd |
| `_metadata.*` (all 7 fields) | no slot — internal only (componentTerms partially via crossReference, see MUST 2) | — |

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
  entry at conceptEntry or langSec level (Basic.tbxmd: definition levels).
  There is no mechanism for entry X to carry entry Y's definitions.
- TBX-Basic **excludes** the TermComp module ("Use TermComp module: False",
  dialect definition p. 1) — even the standard's own term-decomposition markup
  is not available. The only standard way to relate parent and component
  concepts is `crossReference` (ref; conceptEntry/termSec — Basic.tbxmd).
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

administrativeStatus is an optional term-level picklist (Min.tbxmd; only `term`
itself is required at termSec). **The standard says nothing about
synchronisation with external workflow state** — this is a data-engineering
decision, not a compliance one. My interpretation, stated as such: since
Decision 10 already defines a deterministic ATL→TBX mapping, storing two
independently editable copies of derivable information is redundant data — a
textbook desync source.

The mapping needs one completion to be fully deterministic (proposed):

1. `supersededBy` set → `supersededTerm-admn-sts`
2. else `atlStatus = rejected` → `deprecatedTerm-admn-sts`
3. else `atlStatus = atl_approved` → `preferredTerm-admn-sts`
4. else (candidate / no workflow) → `admittedTerm-admn-sts`
   - exception: EN glossary terms (isGlossaryTerm true, no workflow) →
     `preferredTerm-admn-sts` (WSO's own term is by definition the preferred EN
     form)

Note `usageStatus` deliberately does NOT affect administrativeStatus — usage is
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

Min.tbxmd partOfSpeech picklist: `adjective, noun, other, verb, adverb`.
Our schema enum: `noun, verb, adjective, adverb, phrase, null`. Two deviations:

1. **"phrase" is not a legal TBX-Basic partOfSpeech value.** The standard
   handles multiword items via **termType = "phrase"** (Basic.tbxmd). Exporting
   partOfSpeech="phrase" would fail validation.
2. **"other" is missing from our enum** — the standard's own escape hatch,
   which we will need for edge cases ("at ease").

### Options

**Option A — Keep phased plan, add a measurable gate + fix the enum
(recommended).**
- Enum fix now: partOfSpeech ∈ {noun, verb, adjective, adverb, other, null};
  multiword items get termType:"phrase" instead. Zero-cost today because every
  stored value is null (nothing to migrate).
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

- partOfSpeech = grammatical category, picklist without "phrase" (Min.tbxmd);
- termType = form of the term, picklist **with** "phrase" (Basic.tbxmd);
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
| M2 | Atomic components | A: component concept = single home; drop componentLookups | Partly reverses Issue #13 Decision 3 / Decision 17 Part 4 |
| M3 | Status sync | A2: administrativeStatus derived, script-written, validator-enforced | Tightens Decision 10 (no shape change) |
| S1 | PoS quality gate | A: keep phased plan + 0-null gate; fix enum (drop "phrase", add "other") | Amends Decision 6 enum |
| S2 | Linguistic vs structural | A: orthogonal axes; "phrase" moves to termType; no cross-field errors | Amends Decision 6/17 interaction; resolves Issue #15's question |
| S3 | Component sync | A: single home + one-way generation at birth; no sync engine | Follows from M2 |

Cross-cutting root cause, honestly stated: most of the MUST-level anxiety traces
to one overstated phrase — "100% TBX-Basic compliant" — made from summary
documents without the module definitions in hand. Once the claim is corrected to
"TBX-Basic exportable", Q-M1 resolves by wording + mapping table, and the two
real design defects that remain (component duplication, dual-status drift) have
cheap fixes because the migration script was never written.
