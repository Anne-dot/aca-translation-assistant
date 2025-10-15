#!/usr/bin/env python3
"""
Add term_complexity field to all senses

Following ISO 1087 standard:
- simple: single-word term
- complex: multi-word term (space-separated)
- compound: hyphenated/blended term

Also adds component_terms array for complex terms.

Issue: https://github.com/Anne-dot/aca-translation-assistant/issues/7
"""

from pathlib import Path
from utils import load_json_file, save_json_file


INPUT_FILE = Path("data") / "aca-glossary-eki.json"
OUTPUT_FILE = Path("data") / "aca-glossary-eki.json"  # Overwrite


def classify_term_complexity(term: str) -> str:
    """
    Classify term complexity following ISO 1087.

    Args:
        term: English term to classify

    Returns:
        "simple" | "complex" | "compound"
    """
    # Complex: contains space (multi-word)
    if ' ' in term:
        return "complex"

    # Compound: contains hyphen (but not al-anon which is proper name)
    if '-' in term and term.lower() != 'al-anon':
        return "compound"

    # Simple: single word
    return "simple"


def extract_component_terms(term: str) -> list:
    """
    Extract component words from complex term.

    Args:
        term: Multi-word term

    Returns:
        List of component words (lowercased, cleaned)
    """
    # Remove punctuation and split
    import re

    # Remove common punctuation (keep hyphens in words like "self-esteem")
    cleaned = re.sub(r'[,:;.!?]', ' ', term)

    # Split and clean
    components = []
    for word in cleaned.split():
        word = word.strip().lower()
        if word and len(word) > 1:  # Skip single letters
            components.append(word)

    return components


def add_term_complexity(data: dict) -> dict:
    """
    Add term_complexity field to all senses.

    Modifies data in place and returns it.
    """
    terms = data.get('terms', {})

    stats = {
        'simple': 0,
        'complex': 0,
        'compound': 0
    }

    print("🔄 Adding term_complexity field...\n")

    for term_key, term_data in terms.items():
        # Classify term
        complexity = classify_term_complexity(term_key)
        stats[complexity] += 1

        # Add to all senses
        for sense in term_data.get('senses', []):
            sense['term_complexity'] = complexity

            # Add component_terms for complex terms
            if complexity == 'complex':
                components = extract_component_terms(term_key)
                sense['component_terms'] = components
            else:
                sense['component_terms'] = None

    print(f"✅ Classified {len(terms)} terms:")
    print(f"   - Simple: {stats['simple']} ({stats['simple']/len(terms)*100:.1f}%)")
    print(f"   - Complex: {stats['complex']} ({stats['complex']/len(terms)*100:.1f}%)")
    print(f"   - Compound: {stats['compound']} ({stats['compound']/len(terms)*100:.1f}%)\n")

    return data


def main():
    """Main execution."""
    print("\n" + "="*60)
    print("  Add term_complexity Field")
    print("  ISO 1087 Compliance")
    print("="*60 + "\n")

    # Load data
    print(f"📖 Loading: {INPUT_FILE}")
    data = load_json_file(INPUT_FILE)
    term_count = len(data.get('terms', {}))
    print(f"✅ Loaded {term_count} terms\n")

    # Add term_complexity
    data = add_term_complexity(data)

    # Update metadata
    from datetime import datetime
    if 'metadata' not in data:
        data['metadata'] = {}
    data['metadata']['term_complexity_added'] = datetime.now().isoformat()

    # Save
    print(f"💾 Saving: {OUTPUT_FILE}")
    save_json_file(data, OUTPUT_FILE)
    print(f"✅ Saved successfully!\n")

    # Show examples
    print("="*60)
    print("  Examples")
    print("="*60)

    examples = {
        'simple': [],
        'complex': [],
        'compound': []
    }

    for term_key, term_data in list(data['terms'].items())[:100]:
        complexity = term_data['senses'][0]['term_complexity']
        if len(examples[complexity]) < 3:
            examples[complexity].append({
                'term': term_key,
                'components': term_data['senses'][0].get('component_terms')
            })

    print("\nSIMPLE:")
    for ex in examples['simple']:
        print(f"  - {ex['term']}")

    print("\nCOMPLEX:")
    for ex in examples['complex']:
        print(f"  - {ex['term']}")
        print(f"    → components: {ex['components']}")

    print("\nCOMPOUND:")
    for ex in examples['compound']:
        print(f"  - {ex['term']}")

    print("\n" + "="*60)
    print("  ✨ Done!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
