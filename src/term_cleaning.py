#!/usr/bin/env python3
"""
Term Cleaning Functions

Extracts and cleans ACA Glossary terms by removing grammatical markers,
extracting notes, and normalizing term format.

Issue: https://github.com/Anne-dot/aca-translation-assistant/issues/11
"""

import re


# ==============================================================================
# CONSTANTS
# ==============================================================================

PARENTHESES_PATTERN = r'\(([^)]+)\)'  # Regex for extracting parentheses content


# ==============================================================================
# TERM CLEANING
# ==============================================================================

def extract_base_term(term_with_markers):
    """
    Remove parentheses markers from term.

    Args:
        term_with_markers: Term with grammatical markers

    Returns:
        Clean term without markers

    Example:
        "Abuse (n.)" → "Abuse"
        "Balk (to)" → "Balk"
    """
    return re.sub(PARENTHESES_PATTERN, '', term_with_markers).strip()


def extract_notes(term):
    """
    Extract all explanatory text from Glossary term.

    Combines grammatical markers (n., v., to) and explanatory text
    after newline into single notes string.

    Args:
        term: Full Glossary term with markers and explanations

    Returns:
        Combined notes string (markers | explanation)

    Example:
        "Abuse (n.)\n(Physical harm)" → "n. | Physical harm"
        "Balk (to)" → "to"
    """
    # Get text after newline (explanation)
    explanation = ""
    if '\n' in term:
        explanation = term.split('\n', 1)[1].strip()
        # Remove outer parentheses from explanation if present
        explanation = re.sub(r'^\((.+)\)$', r'\1', explanation)

    # Get parentheses markers like (n.), (v.), (to) from first line only
    first_line = term.split('\n', 1)[0].strip()
    markers = re.findall(PARENTHESES_PATTERN, first_line)
    markers_text = ', '.join(markers) if markers else ""

    # Combine notes
    notes_parts = [markers_text, explanation]
    combined_notes = ' | '.join(part for part in notes_parts if part)

    return combined_notes


def clean_glossary_term(term):
    """
    Clean Glossary term for matching and extract notes.

    Removes grammatical markers and newline explanations from term,
    preserving them in separate notes field.

    Args:
        term: Raw Glossary term

    Returns:
        Tuple of (clean_term, notes)

    Examples:
        "Abandonment\n(This can be...)" → ("Abandonment", "This can be...")
        "Abuse (n.)" → ("Abuse", "n.")
        "Balk (to)" → ("Balk", "to")
    """
    # Get first line (remove explanation after newline)
    first_line = term.split('\n', 1)[0].strip()

    # Extract notes before cleaning
    notes = extract_notes(term)

    # Remove parentheses to get base term
    clean_term = extract_base_term(first_line)

    return clean_term, notes
