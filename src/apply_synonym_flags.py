#!/usr/bin/env python3
"""
Apply AI synonym analysis results to foundation_raw.json.
Flags terms where synonyms field contains definitions.
"""

import json
from datetime import datetime
from ai_synonym_analysis_results import ANALYSIS_RESULTS

def main():
    input_file = "data/1_extracted/foundation_raw.json"

    print("🤖 Applying AI synonym analysis results...\n")

    # Load full JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        terms = json.load(f)

    flagged_count = 0
    skipped_count = 0

    # Apply flags
    for term in terms:
        term_name = term['term']

        if term_name not in ANALYSIS_RESULTS:
            continue

        should_flag, reason = ANALYSIS_RESULTS[term_name]

        if not should_flag:
            continue

        # Skip if already flagged or reviewed
        if term.get('reviewedAt') or term.get('needsReview'):
            skipped_count += 1
            print(f"⏭️  Skipped (already flagged/reviewed): {term_name}")
            continue

        # Flag it
        term['needsReview'] = True

        if 'reviewNotes' not in term:
            term['reviewNotes'] = []

        term['reviewNotes'].append({
            'date': datetime.now().isoformat(),
            'note': f'synonyms (AI): {reason}'
        })

        flagged_count += 1
        print(f"✅ Flagged: {term_name}")

    # Save
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"🎉 Done!")
    print(f"   Flagged: {flagged_count} terms")
    print(f"   Skipped: {skipped_count} terms (already flagged/reviewed)")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
