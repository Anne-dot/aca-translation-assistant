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
