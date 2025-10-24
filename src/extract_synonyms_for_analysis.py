#!/usr/bin/env python3
"""
Extract terms with synonyms for AI analysis.
Output: Lightweight JSON with only term and synonyms fields.
"""

import json

def main():
    input_file = "data/1_extracted/foundation_raw.json"
    output_file = "data/1_extracted/synonyms_analysis.json"

    with open(input_file, 'r', encoding='utf-8') as f:
        terms = json.load(f)

    # Extract terms with synonyms (not reviewed, not flagged)
    candidates = []

    for term in terms:
        # Skip already reviewed or flagged
        if term.get('reviewedAt') or term.get('needsReview'):
            continue

        # Check if has synonyms
        has_synonyms = False
        synonyms_text = []

        for meaning in term.get('meanings', []):
            if meaning.get('synonyms'):
                has_synonyms = True
                synonyms_text.extend(meaning.get('synonyms', []))

        if has_synonyms:
            candidates.append({
                'term': term['term'],
                'synonyms': synonyms_text
            })

    # Save lightweight version
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    print(f"✅ Extracted {len(candidates)} terms with synonyms")
    print(f"📄 Saved to: {output_file}")

    # Show first 5 as preview
    print(f"\nPreview (first 5):")
    for i, c in enumerate(candidates[:5], 1):
        print(f"\n{i}. {c['term']}")
        print(f"   Synonyms: {c['synonyms']}")

if __name__ == '__main__':
    main()
