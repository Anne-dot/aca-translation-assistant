#!/usr/bin/env python3
"""
Generate CSV files for manual review.
Part of Issue #4.
"""

import csv
from pathlib import Path

from utils import load_json_file, clean_text_for_csv, shorten_text


# ============================================================
# CONSTANTS
# ============================================================

GLOSSARY_CSV_COLUMNS = [
    'English', 'Match_Status', 'ET_Translation',
    'Source', 'Domain', 'Notes', 'Glossary_Row'
]

EKI_CSV_COLUMNS = [
    'English', 'Estonian', 'Source', 'Domain',
    'Definition_Short', 'Link'
]


# ============================================================
# CSV WRITING HELPERS
# ============================================================

def write_csv_header(writer, columns):
    """Write CSV header row for DictWriter."""
    writer.writeheader()


# ============================================================
# GLOSSARY CSV GENERATION
# ============================================================

def extract_glossary_row_data(term_key, term_data):
    """
    Extract data from enriched term for CSV row.

    Returns:
        Dict with all CSV column values
    """
    sense = term_data['senses'][0]

    # Get first Estonian variant (if exists)
    et_translation = ""
    source = ""
    if sense['eki_variants']:
        first_variant = sense['eki_variants'][0]
        et_translation = first_variant.get('estonian') or "(definition only)"
        source = first_variant.get('source', '')

    return {
        'English': clean_text_for_csv(term_data.get('english', '')),
        'Match_Status': sense.get('match_status', ''),
        'ET_Translation': clean_text_for_csv(et_translation),
        'Source': source,
        'Domain': sense.get('domain', ''),
        'Notes': shorten_text(sense.get('notes', '')),
        'Glossary_Row': term_data.get('glossary_row', '')
    }


def generate_glossary_review_csv(enriched_data, output_path):
    """Generate Glossary review CSV with match info."""
    print(f"📝 Generating Glossary review CSV: {output_path}")

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=GLOSSARY_CSV_COLUMNS)

        write_csv_header(writer, GLOSSARY_CSV_COLUMNS)

        # Sort terms alphabetically by English
        sorted_terms = sorted(
            enriched_data['terms'].items(),
            key=lambda x: x[1]['english'].lower()
        )

        for term_key, term_data in sorted_terms:
            row_data = extract_glossary_row_data(term_key, term_data)
            writer.writerow(row_data)

    print(f"✅ Glossary CSV saved ({len(enriched_data['terms'])} terms)\n")


# ============================================================
# EKI CSV GENERATION
# ============================================================

def extract_eki_row_data(term_key, term_data):
    """
    Extract data from EKI combined for CSV row.

    Returns:
        Dict with all CSV column values
    """
    # Get first source for domain and definition
    domain = ""
    definition = ""
    link = ""
    if term_data.get('en_sources'):
        first_source = term_data['en_sources'][0]
        source_name = first_source.get('source_name', '')
        definition = first_source.get('definition', '')
        link = first_source.get('link', '')

        # Extract domain
        if 'therapy' in source_name.lower():
            domain = "psychology/therapy"
        elif 'health' in source_name.lower():
            domain = "health"
        elif 'crisis' in source_name.lower():
            domain = "crisis"

    # Get Estonian term (first match)
    estonian = ""
    source_code = ""
    if term_data.get('et_matches'):
        first_et = term_data['et_matches'][0]
        estonian = first_et.get('term', '')
        source_code = first_et.get('source', '')
    else:
        source_code = term_data['en_sources'][0].get('source', '') if term_data.get('en_sources') else ""
        estonian = "(no ET term)"

    return {
        'English': term_key,
        'Estonian': estonian,
        'Source': f"eki_{source_code}",
        'Domain': domain,
        'Definition_Short': shorten_text(definition, 150),
        'Link': link
    }


def generate_eki_terms_csv(eki_data, output_path):
    """Generate EKI terms CSV alphabetically."""
    print(f"📝 Generating EKI terms CSV: {output_path}")

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EKI_CSV_COLUMNS)

        write_csv_header(writer, EKI_CSV_COLUMNS)

        # Sort EKI terms alphabetically
        sorted_terms = sorted(
            eki_data['en'].items(),
            key=lambda x: x[0].lower()
        )

        for term_key, term_data in sorted_terms:
            row_data = extract_eki_row_data(term_key, term_data)
            writer.writerow(row_data)

    print(f"✅ EKI CSV saved ({len(eki_data['en'])} terms)\n")


# ============================================================
# MAIN
# ============================================================

def main():
    """Generate both CSV files for manual review."""
    print("\n" + "="*60)
    print("  Generate CSV Files for Manual Review")
    print("  Issue #4")
    print("="*60 + "\n")

    data_dir = Path("data")

    # Load enriched Glossary
    enriched_path = data_dir / "aca-glossary-eki.json"
    print(f"📖 Loading: {enriched_path}")
    enriched_data = load_json_file(enriched_path)
    print(f"✅ Loaded\n")

    # Load EKI combined
    eki_path = data_dir / "eki_combined.json"
    print(f"📖 Loading: {eki_path}")
    eki_data = load_json_file(eki_path)
    print(f"✅ Loaded\n")

    # Generate CSVs
    glossary_csv = data_dir / "glossary-review.csv"
    eki_csv = data_dir / "eki-terms.csv"

    generate_glossary_review_csv(enriched_data, glossary_csv)
    generate_eki_terms_csv(eki_data, eki_csv)

    print("="*60)
    print("  ✨ Done! CSV files ready for manual review")
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
