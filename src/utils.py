#!/usr/bin/env python3
"""
Shared utility functions for ACA Translation Assistant.
Following DRY principle - Single Source of Truth.
"""

import json


# ============================================================
# FILE OPERATIONS
# ============================================================

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
