# Future Ideas

Ideas and improvements for future implementation.

**Purpose:** Strategy, rationale, and open questions for future work
**Actionable Tasks:** See [TODO.md](TODO.md) for concrete next steps and execution plan

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

---

## Component Terms Extraction (formerly Issue #8)

**Overview:**
Extract component terms from multi-word ACA glossary terms to improve translation assistance. Split into multiple parts for ADHD-friendly implementation.

**Background:**
Multi-word ACA terms (e.g., "addictive thinking", "shame-based") rarely exist in standard terminology databases, but their components might ("addictive", "thinking", "shame", "based"). After Sonaveeb lookup (Issue #7), we have 826 terms classified by complexity using ISO 1087 standard.

**Statistics:**
- **Complex terms:** 187 (22.6%) - multi-word phrases like "addictive thinking", "aca counselor"
- **Compound terms:** 26 (3.1%) - hyphenated like "shame-based", "self-esteem"
- **Total candidates:** 213 terms for component lookup

**Key Concepts:**

**Two Types of Terms:**

1. **ACA Glossary Terms** (Official)
   - Source: ACA WSO Glossary (826 terms)
   - Must be translated consistently across all materials
   - Marker: `is_glossary_term: true`
   - Example: "addictive behavior"

2. **Component Terms** (Helper/Added Terms)
   - Derived from glossary terms during extraction
   - Useful for understanding context and building translations
   - Marker: `is_glossary_term: false`
   - Field: `derived_from: ["addictive behavior", "addictive thinking"]` (array - can have multiple sources)
   - Example: "addictive", "behavior" (extracted from "addictive behavior")

**How Components Become Separate Terms:**
When "addictive behavior" is processed:
- "addictive behavior" stays in glossary (is_glossary_term: true)
- "addictive" is ADDED as new term to glossary (is_glossary_term: false, derived_from: ["addictive behavior"])
- "behavior" is ADDED as new term to glossary (is_glossary_term: false, derived_from: ["addictive behavior"])

If "addictive thinking" is also processed:
- "addictive" already exists → update derived_from: ["addictive behavior", "addictive thinking"]

**Three-Part Implementation (ADHD-friendly breakdown):**

### PART 1: Generate Component Terms List

**Goal:** Extract all possible components and see what emerges

**Input:**
- `data/aca-glossary-eki.json` OR clean version (needs clarification - see Data Flow Questions below)
- Filter: `term_complexity in ['complex', 'compound']` (213 terms)
- Use existing: `component_terms` array (already exists from Issue #7)

**Process:**
1. Load glossary
2. Filter complex/compound terms
3. Extract components from `component_terms` array
4. Count frequency (how many glossary terms each component appears in)
5. Generate CSV for manual review

**Output:**
- CSV file with columns: component, frequency, derived_from (list of source terms)
- Example row: "addictive" | 3 | "addictive behavior, addictive thinking, addictive life"

**No filtering yet** - generate ALL components, review manually

### PART 2: Review and Filter Components

**Goal:** Manual review to decide which components to keep/exclude

**Input:** CSV from Part 1

**Process:**
1. Review all generated components
2. Identify generic words to exclude:
   - Prepositions: "of", "in", "at", "to"
   - Articles: "a", "an", "the"
   - Very generic: "self" (?), "about" (?), "based" (?)
   - Decision needed: hard-coded list OR minimum word length (e.g., <3 letters)?
3. Mark approved components

**Output:**
- Approved components list
- Rejected components list (with reason)

**Tool:** Could use glossary_manager_via_terminal.py (Issue #10) or manual CSV editing

### PART 3: Add Components to Glossary

**Goal:** Add approved components as separate terms in glossary

**Input:**
- Approved components list from Part 2
- Current glossary

**Process:**
1. For each approved component:
   - Check if already exists in glossary
   - If exists as glossary term → skip (don't override official terms)
   - If exists as component term → update `derived_from` array
   - If new → add with `is_glossary_term: false` and `derived_from` array

**Output:**
- Glossary with component terms added
- Ready for Sonaveeb lookup

### PART 4: Sonaveeb Lookup for Components (separate from above)

**Goal:** Get translations for component terms

**Input:** Glossary with component terms

**Process:** Same as Issue #7 Sonaveeb lookup, but for component terms

**Output:** Component terms with translations

**Open Questions:**

1. **Data Flow Clarification:**
   - What is current "clean" glossary version?
   - `aca-glossary-eki.json` has EKI data (deprecated) + term_complexity field
   - Should we create new version without EKI data?
   - Where does add_term_complexity.py output currently live?
   - What should be input for component extraction?

2. **Generic Words Filtering:**
   - Which words are "too generic" to include?
   - Hard-coded exclusion list vs minimum word length?
   - Should "self" be excluded? (appears in 17 compound terms)
   - Should "based" be excluded? (appears in "shame-based", "evidence-based")

3. **Component Term Status:**
   - Should component terms have status field?
   - Or only when they get Sonaveeb translations?

4. **Lookup Strategy:**
   - For main term: check glossary first (3-tier: glossary → if not found → Sonaveeb)
   - For component term: same 3-tier approach?
   - Or always Sonaveeb for components?

5. **Priority and Timing:**
   - Run Part 1-3 before Sonaveeb lookup?
   - Or after main Sonaveeb lookup is complete?
   - Manual review before automation?

**Why This Matters:**
- Improves translation coverage (+60-75 useful terms estimated)
- Helps translators understand components even when full phrase unknown
- Components reusable across multiple glossary terms
- Makes lookup more helpful for translation work

**When:** After Sonaveeb lookup (Issue #7) or in parallel

**Related:**
- Issue #7: Sonaveeb lookup and term_complexity field
- Issue #10: glossary_manager_via_terminal.py for manual additions
- ISO 1087: Simple/complex/compound term classification
