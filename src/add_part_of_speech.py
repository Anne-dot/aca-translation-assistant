#!/usr/bin/env python3
"""
Add part_of_speech field to all senses in terminology database.
Issue #6 - ISO 704 compliance for structured grammatical metadata.
"""

from pathlib import Path
from utils import load_json_file, save_json_file


# ==============================================================================
# CONFIGURATION
# ==============================================================================

DATA_FILE = Path(__file__).parent.parent / "data" / "aca-glossary-eki.json"


# ==============================================================================
# MIGRATION FUNCTIONS
# ==============================================================================

def add_part_of_speech_to_senses(data):
    """Add part_of_speech: null to all senses."""

    if 'terms' not in data:
        raise KeyError("❌ ERROR: 'terms' key not found in data!")

    print("🔄 Processing terms...\n")

    terms_count = 0
    senses_count = 0

    for term_key, term_data in data['terms'].items():
        if 'senses' not in term_data:
            print(f"⚠️  WARNING: Term '{term_key}' has no senses array!")
            continue

        for sense in term_data['senses']:
            if 'part_of_speech' not in sense:
                sense['part_of_speech'] = None
                senses_count += 1

        terms_count += 1

        # ADHD-friendly progress feedback every 100 terms
        if terms_count % 100 == 0:
            print(f"   ✓ Processed {terms_count} terms...")

    print(f"\n✅ Done! Updated {senses_count} senses in {terms_count} terms\n")

    return data


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main():
    """Main migration function."""

    print("\n" + "=" * 60)
    print("  Add part_of_speech Field - Issue #6")
    print("=" * 60 + "\n")

    # Load data
    print(f"📖 Loading: {DATA_FILE}")
    try:
        data = load_json_file(DATA_FILE)
        print(f"✅ Loaded {len(data.get('terms', {}))} terms\n")
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {DATA_FILE}\n")
        raise
    except Exception as e:
        print(f"❌ ERROR loading file: {e}\n")
        raise

    # Add part_of_speech field
    data = add_part_of_speech_to_senses(data)

    # Save updated data
    print(f"💾 Saving: {DATA_FILE}")
    try:
        save_json_file(data, DATA_FILE)
        print(f"✅ Saved!\n")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}\n")
        raise

    print("=" * 60)
    print("  ✨ Migration Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
