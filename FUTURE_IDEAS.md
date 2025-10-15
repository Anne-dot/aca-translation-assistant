# Future Ideas

Ideas and improvements for future implementation.

## Auto-translate Notes Field

**What:** Automatically translate English notes/explanations to Estonian

**Example:**
- EN notes: "See page xx of the ACA BRB"
- ET notes: "Vaata lk xx ACA BRB raamatust"

**Why:** Better usability for Estonian translators

**When:** After basic terminology database complete

**How:** Not discussed yet

---

## Parse Grammatical Markers to Structured Field

**What:** Convert grammatical markers `(n.)`, `(v.)`, `(to)` from notes to structured `part_of_speech` field

**Current state:** 107 terms have markers in `notes` field as text

**Example:**
- Current: `notes: "n."`
- Future: `part_of_speech: "noun"`

**Why:** Machine-readable, enables filtering/search by part of speech

**When:** After variant status system implemented

**How:** Not discussed yet

---

## Create Interactive Glossary Manager Script

**What:** Terminal-based interactive script for adding/editing glossary terms

**Why:** Easier than manual JSON editing, reduces errors

**When:** Soon - needed for manual term additions

**How:** Issue #10 - `src/glossary_manager_via_terminal.py`

---

## Add ACA and Adult Child Terms

**What:** Add two core ATL terms to glossary:
- ACA → ATL (status: atl_approved)
- Adult Child → Täiskasvanud laps (status: atl_approved)

**Why:** Foundational terms, must exist before automated enrichment

**When:** Before full Sonaveeb lookup run

**How:** Manual JSON edit OR use glossary_manager_via_terminal.py (Issue #10)

---

## Variant Structure for Terminology Database

**What:** Data structure to support multiple translation variants per term with individual status tracking and metadata

**Current discussion:**
- `is_glossary_term` field - distinguish official ACA terms from component terms
- `derived_from` array - track source glossary terms
- Multiple variants per term - each with own status
- Status values: `atl_approved`, `atl_in_use`, `candidate`, `rejected`
- Metadata per status:
  - Approved: `approved_by`, `approved_date`
  - Rejected: `rejected_by`, `rejected_date`, `rejected_reason`

**Example:**
```json
{
  "variants": [
    {
      "estonian": "sõltuvuslik käitumine",
      "status": "rejected",
      "rejected_by": "ATL review team",
      "rejected_date": "2025-10-16",
      "rejected_reason": "Too clinical, not ACA tone"
    },
    {
      "estonian": "addiktiivne käitumine",
      "status": "atl_approved",
      "approved_by": "ATL consensus",
      "approved_date": "2025-10-16"
    }
  ]
}
```

**Research needed:** Best practices for collaborative terminology management and approval workflows

**Why:** Support ATL review workflow, track decisions, learn from rejections

**When:** Related to Issue #8 and #9

**How:** Not finalized - needs research + discussion
