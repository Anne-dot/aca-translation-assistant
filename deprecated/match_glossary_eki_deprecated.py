#!/usr/bin/env python3
"""
DEPRECATED: Use sonaveeb_lookup.py instead

EKI terms are already included in Sonaveeb.
Use sonaveeb_lookup.py for comprehensive terminology lookup.

---

Match Glossary terms with EKI combined data.
Following ISO 704 lexicography standards.

Issue: https://github.com/Anne-dot/aca-translation-assistant/issues/4
"""

import json
import re
from pathlib import Path
from datetime import datetime

from utils import load_json_file, save_json_file, normalize_term


# ============================================================
# CONSTANTS
# ============================================================

PROGRESS_INTERVAL = 100  # Show progress every N terms
PARENTHESES_PATTERN = r'\(([^)]+)\)'  # Regex for extracting parentheses content


def load_glossary(file_path):
    """Load and validate ACA Glossary."""
    print(f"📖 Loading Glossary: {file_path}")
    data = load_json_file(file_path)

    filled_count = len(data.get('täidetud_terminid', []))
    empty_count = len(data.get('tühjad_terminid', []))
    total_count = filled_count + empty_count

    print(f"✅ {total_count} terms ({filled_count} filled, {empty_count} empty)\n")
    return data


def load_eki_combined(file_path):
    """Load EKI combined terminology database."""
    print(f"📖 Loading EKI combined: {file_path}")
    data = load_json_file(file_path)

    en_count = len(data.get('en', {}))
    et_only_count = len(data.get('et_without_en', {}))

    print(f"✅ {en_count} English terms, {et_only_count} Estonian-only\n")
    return data


def save_enriched_data(enriched_terms, stats, glossary_data, eki_data, output_path):
    """Save enriched Glossary data with metadata."""
    print(f"💾 Saving enriched data: {output_path}")

    output_data = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "source_files": ["aca-glossary.json", "eki_combined.json"],
            "glossary_total": stats['total_count'],
            "eki_total": len(eki_data.get('en', {})),
            "matched_count": stats['matched_count'],
            "unmatched_count": stats['unmatched_count'],
            "match_rate": round(stats['matched_count'] / stats['total_count'] * 100, 2)
        },
        "terms": enriched_terms
    }

    save_json_file(output_data, output_path)
    print(f"✅ Saved successfully!\n")


# ============================================================
# TERM CLEANING (Glossary-specific)
# ============================================================

def extract_base_term(term_with_markers):
    """
    Remove parentheses markers from term.

    Example: "Abuse (n.)" → "Abuse"
    """
    return re.sub(PARENTHESES_PATTERN, '', term_with_markers).strip()


def extract_notes(term):
    """
    Extract all explanatory text from Glossary term.

    Returns combined notes from parentheses and newline text.
    """
    # Get text after newline (explanation)
    explanation = ""
    if '\n' in term:
        explanation = term.split('\n', 1)[1].strip()

    # Get parentheses markers like (n.), (v.), (to)
    markers = re.findall(PARENTHESES_PATTERN, term)
    markers_text = ', '.join(markers) if markers else ""

    # Combine notes
    notes_parts = [markers_text, explanation]
    combined_notes = ' | '.join(part for part in notes_parts if part)

    return combined_notes


def clean_glossary_term(term):
    """
    Clean Glossary term for matching and extract notes.

    Examples:
        "Abandonment\\n(This can be...)" → ("Abandonment", "(This can be...)")
        "Abuse (n.)" → ("Abuse", "(n.)")
        "Balk (to)" → ("Balk", "(to)")

    Returns:
        Tuple of (clean_term, notes)
    """
    # Get first line (remove explanation after newline)
    first_line = term.split('\n', 1)[0].strip()

    # Extract notes before cleaning
    notes = extract_notes(term)

    # Remove parentheses to get base term
    clean_term = extract_base_term(first_line)

    return clean_term, notes


# ============================================================
# TERM MATCHING
# ============================================================

def exact_match(glossary_term, eki_terms):
    """
    Find exact match between Glossary term and EKI terms.

    Args:
        glossary_term: English term from Glossary
        eki_terms: Dict of normalized EKI terms

    Returns:
        EKI data dict if match found, None otherwise
    """
    normalized = normalize_term(glossary_term)

    if normalized in eki_terms:
        return eki_terms[normalized]

    return None


# ============================================================
# DOMAIN & VARIANT EXTRACTION
# ============================================================

def extract_domain(source_name):
    """
    Extract domain/subject field from EKI source name.

    Args:
        source_name: EKI database name (e.g., "Schema Therapy Terminology")

    Returns:
        Domain string (e.g., "psychology/therapy")
    """
    source_lower = source_name.lower()

    if 'therapy' in source_lower or 'schema' in source_lower:
        return "psychology/therapy"
    elif 'health' in source_lower:
        return "health"
    elif 'crisis' in source_lower:
        return "crisis/counseling"
    else:
        return "unknown"


def build_eki_variants(et_matches, en_sources):
    """
    Build Estonian variant list from EKI et_matches.
    Also includes English definition from en_sources.

    Args:
        et_matches: List of Estonian term matches from EKI
        en_sources: List of English source entries (for definitions)

    Returns:
        List of variant dicts with estonian, source, link, definition
    """
    variants = []

    # Get English definition from first source
    en_definition = ""
    en_link = ""
    if en_sources:
        first_source = en_sources[0]
        en_definition = first_source.get('definition', '')
        en_link = first_source.get('link', '')

    for et_match in et_matches:
        variant = {
            "estonian": et_match.get('term', ''),
            "source": f"eki_{et_match.get('source', '')}",
            "link": et_match.get('link', ''),
            "definition": et_match.get('definition', ''),
        }
        variants.append(variant)

    # If no Estonian matches but we have English source, add EN definition
    if not variants and en_sources:
        variants.append({
            "estonian": None,
            "source": f"eki_{en_sources[0].get('source', '')}",
            "link": en_link,
            "definition": en_definition,
        })

    return variants


def extract_synonyms(en_sources):
    """
    Extract and deduplicate synonyms from EKI English sources.

    Args:
        en_sources: List of English source entries from EKI

    Returns:
        Deduplicated list of synonyms
    """
    all_synonyms = []

    for en_source in en_sources:
        synonyms = en_source.get('synonyms', [])
        all_synonyms.extend(synonyms)

    return list(set(all_synonyms))  # Remove duplicates


def create_sense_from_eki(eki_data, match_confidence):
    """
    Create sense structure from EKI matched data.

    Args:
        eki_data: EKI term data (en_sources, et_matches)
        match_confidence: "exact" or "fuzzy"

    Returns:
        Sense dict with all required fields
    """
    # Extract domain from first source
    domain = "unknown"
    if eki_data.get('en_sources'):
        first_source = eki_data['en_sources'][0]
        source_name = first_source.get('source_name', '')
        domain = extract_domain(source_name)

    # Build variants and synonyms
    eki_variants = build_eki_variants(
        eki_data.get('et_matches', []),
        eki_data.get('en_sources', [])
    )
    synonyms = extract_synonyms(eki_data.get('en_sources', []))

    sense = {
        "sense_id": 1,
        "match_status": "matched",
        "match_confidence": match_confidence,
        "domain": domain,
        "eki_variants": eki_variants,
        "synonyms": synonyms,
        "preferred_variant": None,
        "notes": ""
    }

    return sense


def create_unmatched_sense():
    """Create empty sense structure for unmatched terms."""
    return {
        "sense_id": 1,
        "match_status": "unmatched",
        "match_confidence": "none",
        "domain": "",
        "eki_variants": [],
        "synonyms": [],
        "preferred_variant": None,
        "notes": ""
    }


# ============================================================
# GLOSSARY TERM PROCESSING
# ============================================================

def process_glossary_term(term_entry, eki_en_normalized):
    """
    Process single Glossary term: clean, match, create sense.

    Returns:
        Tuple of (normalized_key, term_data, matched: bool)
    """
    english_raw = term_entry.get('english', '')
    letter = term_entry.get('letter', '')
    row = term_entry.get('row', 0)

    # Clean term and extract notes
    english_clean, glossary_notes = clean_glossary_term(english_raw)

    # Try exact match
    eki_match = exact_match(english_clean, eki_en_normalized)

    if eki_match:
        sense = create_sense_from_eki(eki_match, "exact")
        sense['notes'] = glossary_notes
        matched = True
    else:
        sense = create_unmatched_sense()
        sense['notes'] = glossary_notes
        matched = False

    normalized_key = normalize_term(english_clean)
    term_data = {
        "english": english_raw,  # Keep original with markers
        "letter": letter,
        "glossary_row": row,
        "senses": [sense]
    }

    return normalized_key, term_data, matched


# ============================================================
# MATCHING ALGORITHM
# ============================================================

def match_glossary_with_eki(glossary_data, eki_data):
    """
    Match Glossary terms with EKI combined data.

    Args:
        glossary_data: ACA Glossary dict
        eki_data: EKI combined dict

    Returns:
        Tuple of (enriched_terms dict, statistics dict)
    """
    print("🔄 Matching Glossary terms with EKI...\n")

    # Prepare EKI lookup dict (normalized keys)
    eki_en_normalized = {
        normalize_term(term): data
        for term, data in eki_data.get('en', {}).items()
    }

    enriched_terms = {}
    matched_count = 0
    unmatched_count = 0

    # Combine all Glossary terms
    all_terms = (
        glossary_data.get('täidetud_terminid', []) +
        glossary_data.get('tühjad_terminid', [])
    )

    for term_entry in all_terms:
        normalized_key, term_data, matched = process_glossary_term(
            term_entry, eki_en_normalized
        )

        enriched_terms[normalized_key] = term_data

        if matched:
            matched_count += 1
        else:
            unmatched_count += 1

        # Progress indicator
        total_processed = matched_count + unmatched_count
        if total_processed % PROGRESS_INTERVAL == 0:
            print(f"  Processed {total_processed} terms...")

    print(f"\n✅ Matching complete!")
    print(f"   📊 Matched: {matched_count}")
    print(f"   📊 Unmatched: {unmatched_count}\n")

    stats = {
        "matched_count": matched_count,
        "unmatched_count": unmatched_count,
        "total_count": len(all_terms)
    }

    return enriched_terms, stats


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  ACA Glossary + EKI Matching")
    print("  Issue #4: Match Glossary terms with EKI data")
    print("="*60 + "\n")

    # Define paths
    data_dir = Path("data")
    glossary_path = data_dir / "aca-glossary.json"
    eki_path = data_dir / "eki_combined.json"
    output_path = data_dir / "aca-glossary-eki.json"

    # Load data
    glossary_data = load_glossary(glossary_path)
    eki_data = load_eki_combined(eki_path)

    # Match terms
    enriched_terms, stats = match_glossary_with_eki(glossary_data, eki_data)

    # Save results
    save_enriched_data(enriched_terms, stats, glossary_data, eki_data, output_path)

    print("="*60)
    print(f"  ✨ Done! Match rate: {stats['matched_count']}/{stats['total_count']} "
          f"({round(stats['matched_count']/stats['total_count']*100, 1)}%)")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
