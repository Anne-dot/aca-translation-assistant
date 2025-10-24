#!/usr/bin/env python3
"""
Shared utility functions for ACA Translation Assistant.
Following DRY principle - Single Source of Truth.
"""

import json
import csv
import re
from pathlib import Path


# ============================================================
# DIRECTORY OPERATIONS
# ============================================================

def ensure_output_dir(file_path):
    """
    Ensure output directory exists.

    Args:
        file_path: Path to file (directory will be created)
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# FILE OPERATIONS
# ============================================================

def read_csv_file(file_path, delimiter='\t'):
    """
    Read CSV file with specified delimiter.

    Args:
        file_path: Path to CSV file
        delimiter: CSV delimiter (default: tab)

    Yields:
        Each row as list
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            yield row


def load_json_file(file_path):
    """
    Load JSON file. Single source for file loading.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data (dict or list)

    Raises:
        FileNotFoundError: If file doesn't exist
        JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data, file_path, indent=2):
    """
    Save data to JSON file.

    Args:
        data: Data to save (dict or list)
        file_path: Path where to save
        indent: JSON indentation (default: 2)
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


# ============================================================
# TEXT PROCESSING
# ============================================================

def normalize_term(term):
    """
    Normalize term for matching: lowercase, strip whitespace.

    Args:
        term: Term to normalize

    Returns:
        Normalized term string
    """
    return term.lower().strip()


def clean_text_for_csv(text):
    """
    Clean text for CSV: remove newlines, trim whitespace.

    Args:
        text: Text to clean

    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    # Replace newlines with pipe separator
    cleaned = text.replace('\n', ' | ')
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    return cleaned


def shorten_text(text, max_length=100):
    """
    Shorten long text for display/CSV readability.

    Args:
        text: Text to shorten
        max_length: Maximum length (default: 100)

    Returns:
        Shortened text with "..." if truncated
    """
    if not text:
        return ""
    cleaned = clean_text_for_csv(text)
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[:max_length] + "..."


def clean_text(text):
    """
    Remove non-breaking spaces and clean whitespace.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""
    return text.replace('\u00a0', ' ').strip()


def parse_list_from_text(text, delimiter=','):
    """
    Parse comma-separated text into list.

    Args:
        text: Text with delimited items
        delimiter: Delimiter (default: comma)

    Returns:
        List of cleaned items
    """
    if not text or not text.strip():
        return []
    return [item.strip() for item in text.split(delimiter) if item.strip()]


def detect_numbered_meanings(text):
    """
    Detect if text has numbered meanings (1., 2., etc.)

    Args:
        text: Text to check

    Returns:
        True if numbered meanings detected
    """
    if not text:
        return False
    # Pattern: starts with "1." or has "\n1." followed by space
    return bool(re.search(r'(^|\n)\d+\.\s+', text))


def split_numbered_text(text):
    """
    Split text by numbered items (1., 2., 3., etc.)

    Args:
        text: Text with numbered items

    Returns:
        List of text chunks (one per number)
    """
    if not text:
        return []

    # Split by pattern: number followed by period and space
    parts = re.split(r'\n?(\d+)\.\s+', text)

    # parts format: ['prefix', '1', 'text1', '2', 'text2', ...]
    result = []
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            result.append(parts[i + 1].strip())

    return result if result else [text]


# ============================================================
# NORMALIZATION DETECTION - Issue #25
# ============================================================

def detect_parentheses_notation(term):
    """
    Detect parentheses notation like (s), (ren), (es).

    Issue #25 Category 5: Singular/Plural
    Examples: caregiver(s), foster child(ren)
    Decision: Split into separate terms

    Args:
        term: Term string to check

    Returns:
        Dict with category and suggestion, or None
    """
    if '(' not in term or ')' not in term:
        return None

    if '(s)' in term:
        base = term.replace('(s)', '').strip()
        plural = base + 's'
        return {
            'category': 'split_parentheses',
            'pattern': '(s)',
            'suggestion': [base, plural]
        }

    if '(ren)' in term:
        base = term.replace('(ren)', '').strip()
        plural = base + 'ren'
        return {
            'category': 'split_parentheses',
            'pattern': '(ren)',
            'suggestion': [base, plural]
        }

    if '(es)' in term:
        base = term.replace('(es)', '').strip()
        plural = base + 'es'
        return {
            'category': 'split_parentheses',
            'pattern': '(es)',
            'suggestion': [base, plural]
        }

    return None


def detect_asterisk(term):
    """
    Detect asterisk footnote markers.

    Issue #25 Category 7: Asterisks
    Examples: counseling*, para-alcoholic*
    Decision: Remove asterisk, move explanation to note field

    Args:
        term: Term string to check

    Returns:
        Dict with category and suggestion, or None
    """
    if '*' not in term:
        return None

    clean_term = term.replace('*', '').strip()
    return {
        'category': 'remove_asterisk',
        'suggestion': {'cleanTerm': clean_term}
    }


def detect_multiple_terms_comma(term):
    """
    Detect multiple terms separated by comma.

    Issue #25 Category 4: Multiple terms
    Examples: hero, hero child
    Decision: Split into separate terms

    Args:
        term: Term string to check

    Returns:
        Dict with category and suggestion, or None
    """
    if '(' in term or ', ' not in term:
        return None

    parts = [p.strip() for p in term.split(',')]
    if len(parts) > 1:
        return {
            'category': 'split_multiple_comma',
            'suggestion': parts
        }

    return None


def detect_multiple_terms_slash(term):
    """
    Detect multiple terms separated by slash.

    Issue #25 Category 4: Multiple terms
    Examples: Annual Business Conference/ABC
    Decision: Split into separate terms

    Args:
        term: Term string to check

    Returns:
        Dict with category and suggestion, or None
    """
    if '/' not in term:
        return None

    parts = [p.strip() for p in term.split('/')]
    if len(parts) > 1:
        return {
            'category': 'split_multiple_slash',
            'suggestion': parts
        }

    return None


def detect_seealso_issues(term_data):
    """
    Detect seeAlso with explanations instead of terms.

    Issue #25 Category 8: "See also" format
    Example: "trauma for further references in the literature"
    Decision: Flag for manual review, extract term only

    Args:
        term_data: Full term dict with seeAlso field

    Returns:
        Dict with category and suggestion, or None
    """
    see_also = term_data.get('seeAlso', [])
    if not see_also:
        return None

    issues = []
    for entry in see_also:
        word_count = len(entry.split())
        if word_count > 4:
            issues.append({
                'entry': entry,
                'reason': f'Too long ({word_count} words)'
            })

    if issues:
        return {
            'category': 'clean_seealso',
            'suggestion': issues
        }

    return None


def collect_normalization_issues(term_data):
    """
    Collect all normalization issues for a term.

    Issue #25: Term normalization policy decisions
    Detects Categories 4, 5, 7, 8 issues.

    Args:
        term_data: Full term dict

    Returns:
        List of issue dicts (empty if no issues)
    """
    issues = []
    term = term_data['term']

    # Category 5: Parentheses
    parentheses = detect_parentheses_notation(term)
    if parentheses:
        issues.append(parentheses)

    # Category 7: Asterisk
    asterisk = detect_asterisk(term)
    if asterisk:
        issues.append(asterisk)

    # Category 4: Multiple terms (comma)
    comma = detect_multiple_terms_comma(term)
    if comma:
        issues.append(comma)

    # Category 4: Multiple terms (slash)
    slash = detect_multiple_terms_slash(term)
    if slash:
        issues.append(slash)

    # Category 8: seeAlso format
    seealso = detect_seealso_issues(term_data)
    if seealso:
        issues.append(seealso)

    return issues
