#!/usr/bin/env python3
"""
EKI Terminology Data Loader and Combiner

Reads all 4 EKI JSON files and combines them into a unified structure
with English terms as keys.
"""

from pathlib import Path
from typing import Dict, List, Any

from utils import load_json_file, save_json_file

# ==============================================================================
# CONFIGURATION
# ==============================================================================

DATA_DIR = Path(__file__).parent.parent / "data" / "eki_terms"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "eki_combined.json"

EKI_FILES = [
    "eki_skt_20251014.json",
    "eki_dkt_20251014.json",
    "eki_kriis_20251014.json",
    "eki_TAI_20251014.json"
]


# ==============================================================================
# DATA LOADING AND PROCESSING
# ==============================================================================

def load_eki_file(filename: str) -> Dict[str, Any]:
    """Loads one EKI JSON file"""
    filepath = DATA_DIR / filename

    print(f"📖 Loading file: {filename}")

    try:
        data = load_json_file(filepath)
        term_count = len(data.get('terms', []))
        print(f"   ✅ Loaded {term_count} terms\n")
        return data

    except FileNotFoundError:
        print(f"   ❌ ERROR: File not found: {filepath}\n")
        raise
    except Exception as e:
        print(f"   ❌ ERROR: {e}\n")
        raise


def combine_eki_data(eki_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combines all EKI data into unified structure"""

    print("🔄 Combining EKI data...\n")

    combined = {
        "meta": {},
        "en": {},  # English terms as keys
        "et_without_en": {}
    }

    # Save metadata
    for data in eki_data_list:
        meta = data.get('metadata', {})
        code = meta.get('database_code')
        if code:
            combined["meta"][code] = meta

    # Process terms
    for data in eki_data_list:
        source_code = data.get('metadata', {}).get('database_code', 'unknown')
        source_name = data.get('metadata', {}).get('database_name', 'Unknown')

        for term_data in data.get('terms', []):
            language = term_data.get('language', '').lower()
            term = term_data.get('term', '')

            if not term:
                continue

            # English terms
            if language == 'inglise':
                if term not in combined["en"]:
                    combined["en"][term] = {
                        "en_sources": [],
                        "et_matches": []
                    }

                combined["en"][term]["en_sources"].append({
                    "source": source_code,
                    "source_name": source_name,
                    "link": term_data.get('link', ''),
                    "definition": term_data.get('definition', ''),
                    "synonyms": term_data.get('synonyms', [])
                })

            # Estonian terms
            elif language == 'eesti':
                # Look for English pair
                # Check if there's an English term with same definition or link pattern
                en_match = None

                # Try to find matching English term by checking if definition matches
                term_link = term_data.get('link', '')
                for other_data in data.get('terms', []):
                    if other_data.get('language', '').lower() == 'inglise':
                        other_link = other_data.get('link', '')
                        # Same definition or related link
                        if term_data.get('definition') == other_data.get('definition'):
                            en_match = other_data.get('term')
                            break

                if en_match:
                    # Add under English term
                    if en_match not in combined["en"]:
                        combined["en"][en_match] = {
                            "en_sources": [],
                            "et_matches": []
                        }

                    combined["en"][en_match]["et_matches"].append({
                        "term": term,
                        "source": source_code,
                        "link": term_data.get('link', ''),
                        "definition": term_data.get('definition', '')
                    })
                else:
                    # Estonian term without English match
                    if term not in combined["et_without_en"]:
                        combined["et_without_en"][term] = {
                            "sources": []
                        }

                    combined["et_without_en"][term]["sources"].append({
                        "source": source_code,
                        "source_name": source_name,
                        "link": term_data.get('link', ''),
                        "definition": term_data.get('definition', '')
                    })

    return combined


def save_json(data: Dict[str, Any], filepath: Path):
    """Saves combined data to JSON file"""

    print(f"💾 Saving file: {filepath}")

    try:
        save_json_file(data, filepath)
        print(f"   ✅ Saved!\n")

    except Exception as e:
        print(f"   ❌ ERROR saving: {e}\n")
        raise


def print_statistics(data: Dict[str, Any]):
    """Prints summary of combined data"""

    en_terms = len(data.get("en", {}))
    et_without_en = len(data.get("et_without_en", {}))
    sources = len(data.get("meta", {}))

    print("=" * 60)
    print("📊 STATISTICS")
    print("=" * 60)
    print(f"English terms: {en_terms}")
    print(f"Estonian terms without English match: {et_without_en}")
    print(f"Total sources: {sources}")
    print("=" * 60)


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main():
    """Main function - loads and combines EKI data"""

    print("\n" + "=" * 60)
    print("🚀 EKI DATA LOADING AND COMBINING")
    print("=" * 60 + "\n")

    try:
        # Load all EKI files
        eki_data_list = []
        for file in EKI_FILES:
            data = load_eki_file(file)
            eki_data_list.append(data)

        # Combine data
        combined = combine_eki_data(eki_data_list)

        # Save result
        save_json(combined, OUTPUT_FILE)

        # Print statistics
        print_statistics(combined)

        print("\n✨ Done!\n")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}\n")
        raise


if __name__ == "__main__":
    main()
