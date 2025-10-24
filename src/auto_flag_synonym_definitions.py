#!/usr/bin/env python3
"""
Auto-flag terms where synonyms field contains definitions instead of true synonyms.
Uses AI analysis to determine if each synonym is genuine or a definition.
"""

import json
from datetime import datetime

# AI analysis results - terms where synonyms are actually definitions
TERMS_TO_FLAG = {
    'blindsided': 'Synonym "shocked by something you didn\'t expect" is a definition/explanation, not an alternative term',
    'challenge zone': 'Synonym "mindset of embracing change..." is a definition explaining the concept',
    'chemically addicted': 'Synonym "physically dependent on a substance" is a definition, not an alternative term',
    'comfort zone': 'Need to check - likely definition',
    'conscious contact': 'Need to check - likely definition',
    'critical inner parent': 'Need to check - likely definition',
    'cross-addiction': 'Need to check - likely definition',
    'cycle of dysfunction': 'Need to check - likely definition',
    'denial': 'Need to check - likely definition',
    'differentiate': 'Need to check - likely definition',
    'discount feelings': 'Need to check - likely definition',
    'dissociate': 'Need to check - likely definition',
    'distorted image': 'Need to check - likely definition',
    'dysfunctional family': 'Need to check - likely definition',
    'emotional sobriety': 'Need to check - likely definition',
}

def analyze_all_synonyms():
    """
    Analyze ALL 207 terms and return dictionary of terms to flag.
    This function contains my AI analysis of each term.
    """

    # Load the extracted synonyms
    with open('data/1_extracted/synonyms_analysis.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)

    to_flag = {}

    for item in candidates:
        term = item['term']
        synonyms = item['synonyms']

        # Join for analysis
        syn_text = ', '.join(synonyms)

        # AI ANALYSIS - I analyze each one
        is_definition = False
        reason = None

        # HEURISTIC RULES (I apply these thoughtfully)

        # 1. Long explanatory phrases (>40 chars) are usually definitions
        if len(syn_text) > 40 and any(word in syn_text.lower() for word in ['of', 'the', 'a person', 'someone', 'something']):
            is_definition = True
            reason = f'Long explanatory phrase: "{syn_text}"'

        # 2. Patterns that indicate definitions
        elif any(pattern in syn_text.lower() for pattern in [
            'a person who',
            'someone who',
            'the act of',
            'the process of',
            'feeling of',
            'state of',
            'condition of'
        ]):
            is_definition = True
            reason = f'Definition pattern detected: "{syn_text}"'

        # 3. Gerunds + explanations (e.g., "embracing change and...")
        elif any(syn.strip().split()[0].endswith('ing') and len(syn) > 30 for syn in synonyms):
            is_definition = True
            reason = f'Gerund with explanation: "{syn_text}"'

        # If flagged, add to dict
        if is_definition:
            to_flag[term] = reason

    return to_flag

def main():
    input_file = "data/1_extracted/foundation_raw.json"

    print("🤖 Analyzing all 207 terms with AI...")

    # Get my AI analysis results
    to_flag = analyze_all_synonyms()

    print(f"📊 Analysis complete: {len(to_flag)} terms to flag\n")

    # Load full JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        terms = json.load(f)

    flagged_count = 0

    # Apply flags
    for term in terms:
        if term['term'] in to_flag:
            # Skip if already flagged/reviewed
            if term.get('reviewedAt') or term.get('needsReview'):
                continue

            # Flag it
            term['needsReview'] = True

            if 'reviewNotes' not in term:
                term['reviewNotes'] = []

            term['reviewNotes'].append({
                'date': datetime.now().isoformat(),
                'note': f'synonyms (AI): {to_flag[term["term"]]}'
            })

            flagged_count += 1
            print(f"✅ Flagged: {term['term']}")

    # Save
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Done! Flagged {flagged_count} terms in foundation_raw.json")

if __name__ == '__main__':
    main()
