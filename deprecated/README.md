# Deprecated Files

This folder contains deprecated code and data from the **EKI Collection Approach** (October 2025).

## Why Deprecated?

The original approach was to collect terminology data from 4 EKI terminology databases separately and match them with the ACA Glossary. This was replaced by **Sõnaveeb enrichment** (Issue #7), which includes all EKI databases automatically.

**Key insight:** Sõnaveeb already includes all EKI terminology databases, so separate collection is unnecessary.

## Deprecation Timeline

- **Issues #1, #3, #4:** EKI collection and matching implementation
- **Issue #7 (2025-10-15):** Sõnaveeb approach adopted, EKI approach deprecated
- **2025-10-16:** Scripts and data moved to `deprecated/` folder

## Contents

### Scripts (deprecated/)
- `eki_collector_deprecated.py` - EKI terminology collector (4 databases)
- `load_eki_data_deprecated.py` - EKI data loader and combiner
- `match_glossary_eki_deprecated.py` - Glossary-EKI matching algorithm

### Data (deprecated/data/)
- `eki_terms/` - 4 EKI terminology databases (1,278 terms total)
  - `eki_kriis_20251014.json` (82 terms)
  - `eki_skt_20251014.json` (250 terms)
  - `eki_dkt_20251014.json` (301 terms)
  - `eki_TAI_20251014.json` (645 terms)
- `eki_combined.json` - Combined EKI data (564 EN terms, 262 ET-only)
- `eki-terms.csv` - EKI terms review file
- `glossary-review.csv` - Glossary-EKI match review file

## What Was Preserved

Useful logic from deprecated scripts was extracted and preserved:

- **Term cleaning functions** → `src/term_cleaning.py` (Issue #11)
  - Normalize whitespace
  - Remove grammatical markers
  - Clean explanations

These functions are reused in the current Sõnaveeb enrichment workflow.

## Current Approach

See `src/sonaveeb_lookup.py` (Issue #7) for the current enrichment approach using Sõnaveeb API.

---

**For historical context, see:**
- [Issue #1](https://github.com/Anne-dot/aca-translation-assistant/issues/1) - EKI collection
- [Issue #3](https://github.com/Anne-dot/aca-translation-assistant/issues/3) - EKI data loading
- [Issue #4](https://github.com/Anne-dot/aca-translation-assistant/issues/4) - Glossary-EKI matching
- [Issue #7](https://github.com/Anne-dot/aca-translation-assistant/issues/7) - Sõnaveeb enrichment
- [Issue #11](https://github.com/Anne-dot/aca-translation-assistant/issues/11) - Term cleaning utilities
