#!/usr/bin/env python3
"""
Generate CSV file for Estonian-only terms (no English equivalent).
For manual review and printing.
"""

import csv
from pathlib import Path
from utils import load_json_file, clean_text_for_csv, shorten_text


# ==============================================================================
# CONFIGURATION
# ==============================================================================

INPUT_FILE = Path(__file__).parent.parent / "data" / "eki_combined.json"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "estonian-only-terms.csv"


# ==============================================================================
# CSV GENERATION
# ==============================================================================

def generate_estonian_only_csv():
    """Generate CSV with Estonian-only terms."""

    print("\n" + "=" * 60)
    print("  Generate Estonian-Only Terms CSV")
    print("=" * 60 + "\n")

    # Load data
    print(f"📖 Loading: {INPUT_FILE}")
    data = load_json_file(INPUT_FILE)

    et_only = data.get('et_without_en', {})
    print(f"✅ Found {len(et_only)} Estonian-only terms\n")

    # Prepare CSV data
    print("🔄 Processing terms...\n")

    csv_data = []
    for et_term, term_data in sorted(et_only.items()):
        sources = term_data.get('sources', [])

        for source in sources:
            row = {
                'Estonian': et_term,
                'Source': source.get('source', ''),
                'Source_Name': source.get('source_name', ''),
                'Definition': shorten_text(source.get('definition', ''), max_length=200),
                'Link': source.get('link', '')
            }
            csv_data.append(row)

    print(f"   Prepared {len(csv_data)} rows (some terms have multiple sources)\n")

    # Write CSV
    print(f"💾 Writing: {OUTPUT_FILE}")

    columns = ['Estonian', 'Source', 'Source_Name', 'Definition', 'Link']

    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"✅ Saved!\n")

    print("=" * 60)
    print(f"  ✨ CSV Ready! {len(csv_data)} rows")
    print("=" * 60 + "\n")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    try:
        generate_estonian_only_csv()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
