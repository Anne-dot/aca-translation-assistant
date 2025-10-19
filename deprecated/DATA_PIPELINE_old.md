# Data Pipeline Documentation

This document maps the complete data transformation pipeline from original ACA Glossary .docx to final JSON.

---

## Step 1: .docx Extraction → aca-glossary.json

**Goal:** Extract all terms and translations from original Word document, preserving everything as-is.

### Input

**File:** `data/Glossary_templatesonavara.docx`

**Structure:**
- Table 2 (terminite tabel)
- 874 rows (including header)
- 3 columns:
  1. Letter marker (A, B, C...) - **IGNORE**
  2. **"Term or Phrase"** - English term
  3. **"Translation/Other Alternatives"** - Estonian translation

### Process

1. Open .docx file
2. Read Table 2
3. Skip header row
4. For each row:
   - Ignore column 1 (letter marker)
   - Read column 2 → `english` field
   - Read column 3 → `estonian` field
5. **Preserve everything** - NO TRANSFORMATIONS

### Examples from .docx

**Example 1:**

.docx English (column 2):
```
Abandonment
(This can be physical or emotional abandonment. Shaming a child is abandoning a child.)
```

.docx Estonian (column 3):
```
hülgamine

(See võib olla füüsiline või emotsionaalne hülgamine. Lapse häbistamine on lapse hülgamine.)
```

**Example 2:**

.docx English (column 2):
```
About (is)
```

.docx Estonian (column 3):
```
Kohta
```

### Output

**File:** `data/aca-glossary.json`

**Structure:** Dictionary with English term as key

```json
{
  "Abandonment\n(This can be physical or emotional abandonment. Shaming a child is abandoning a child.)": {
    "english": "Abandonment\n(This can be physical or emotional abandonment. Shaming a child is abandoning a child.)",
    "estonian": "hülgamine\n\n(See võib olla füüsiline või emotsionaalne hülgamine. Lapse häbistamine on lapse hülgamine.)"
  },
  "About (is)": {
    "english": "About (is)",
    "estonian": "Kohta"
  }
}
```

---

**Last Updated:** 2025-10-16
