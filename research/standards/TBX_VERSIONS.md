# TBX-Basic Version Landscape

**Purpose:** Track which versions of the TBX-Basic specification exist, where each
one lives in this repository, and where to re-download them. Created during the
Issue #44 standards review (2026-08-21), when we discovered that a new major
version of the specification had been published after our schema decisions were
made.

---

## Versions at a glance

| Version | Year | Publisher | Status here | Location |
|---|---|---|---|---|
| TBX-Basic (original) | 2009 | LISA Term SIG | Deprecated | `deprecated/TBXBasic/` |
| TBX-Basic dialect v1.2.1 | 2023 | LTAC Global | Deprecated (restorable) | `deprecated/TBX-Basic_v1.2.1/` |
| **TBX-Basic Version 4** | **Nov 2025** | **TerminOrgs** | **Current reference** | see below |

**Which version does the project target?** Not decided yet — this is part of the
Issue #44 MUST-question walkthrough. The v1.2.1 package was moved to
`deprecated/` for tidiness on 2026-08-21 and can be restored if the decision
lands on targeting v1.2.1.

---

## Version 4 files (current reference set)

| File / folder | What it is | Committed? |
|---|---|---|
| `TBX-Basic-V4.pdf` | Full 21-page prose specification (data categories, entry structure, permitted elements, compliance rules) | **NO — gitignored.** TerminOrgs copyright forbids redistribution. Re-download: https://www.terminorgs.net/downloads/TBX-Basic-V4.pdf |
| `TBX-Basic-V4-files/` | `basic_schema.sch` (TBX-Basic constraints) + 1 valid and 8 invalid sample `.tbx` files | Yes |
| `iso-tr24633-2-schemas/` | `core_schema.rng`, `core_schema.xsd`, `xml.xsd` — the TBX core structure schemas, published free of charge by ISO as TR 24633-2 Annex A | Yes |

**Re-download URLs:**
- Spec PDF: https://www.terminorgs.net/downloads/TBX-Basic-V4.pdf
- Samples + schematron package: https://www.terminorgs.net/downloads/TBX-Basic-V4-files.zip
- ISO core schemas: https://standards.iso.org/iso/tr/24633/-2/ed-1/en/ (Annex A zip)
- Spec landing page: https://www.terminorgs.net/TBX-Basic.html

A valid V4 file is validated with three files together: `core_schema.xsd` (or
`.rng`) + `xml.xsd` + `basic_schema.sch` (V4 spec, Appendix C).

---

## Key differences: v1.2.1 → Version 4

These matter for our schema decisions (Issue #44):

| Topic | v1.2.1 (2023) | Version 4 (2025) |
|---|---|---|
| Term status field | `administrativeStatus`, values `preferredTerm-admn-sts`, `admittedTerm-admn-sts`, `deprecatedTerm-admn-sts`, `supersededTerm-admn-sts` | `usageStatus`, values `preferred`, `admitted`, `deprecated` (no "superseded"; only one value per term) |
| Transaction types | `origination`, `modification` | `creation`, `modification` |
| partOfSpeech values | adjective, noun, other, verb, adverb | noun, verb, adjective, adverb, **properNoun**, other |
| partOfSpeech requirement | optional | **Mandatory per term for any automated processing (CAT tools);** for human-only resources may be omitted if a definition or context is present (V4 §9) |
| Module structure | Core + Min module + Basic module (separate .tbxmd files) | Single consolidated spec + one schematron |
| Core prose availability | Only via paywalled ISO 30042:2019 | Entry structure + permitted element list included in the free spec (§7, Appendix B) |

Unchanged and relevant: partOfSpeech still has **no "phrase" value** —
multiword items are marked with `termType="phrase"` instead. `definition`
belongs at concept or language level (pick one per termbase), `context` at term
level. Custom data categories are still not permitted in a compliant file
(V4 §9: "uses only the DCs that are defined in this document").

---

## Older packages (in `deprecated/`)

**`deprecated/TBXBasic/` (2009, LISA):** full 20-page prose spec
(`TBX_Basic_datacategoriesV23.pdf`), old core structure schemas
(`TBXBasiccoreStructV02.dtd`, `TBXBasicRNGV02.rng`), XCS files, samples. Uses
the pre-2019 element names (`termEntry`, `langSet`, `tig`). Historical
reference only.

**`deprecated/TBX-Basic_v1.2.1/` (2023, LTAC Global):** the ISO 30042:2019-era
dialect package — 1-page dialect definition, Min/Basic module definitions
(PDF + machine-readable `.tbxmd`), DCA/DCT schematron, valid example files.
This was the citation basis for the first version of
`TBX_M1_CLAUDE_DRAFT_ANALYSIS.md`. Source:
https://github.com/LTAC-Global/TBX-Basic_dialect
