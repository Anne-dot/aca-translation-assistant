#!/usr/bin/env python3
"""
EKI Terminology Collector

Collects terminology from Estonian Language Institute (EKI) Sõnaveeb terminology databases.
Saves terms in JSON format with references to sources.

Usage:
    python3 eki_collector.py <database_code>

Examples:
    python3 eki_collector.py skt        # Schema Therapy
    python3 eki_collector.py dkt        # DKT/DBT
    python3 eki_collector.py kriis      # Crisis Counseling
    python3 eki_collector.py TAI        # Health Terminology
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import List, Dict
from html.parser import HTMLParser
import urllib.parse
from bs4 import BeautifulSoup

# EKI terminology databases
TERM_DATABASES = {
    'skt': {
        'name': 'Schema Therapy Terminology',
        'url': 'https://sonaveeb.ee/ds/skt',
        'contact': 'Kaia Kastepõld-Tõrs (skeemiteraapia@gmail.com)'
    },
    'dkt': {
        'name': 'Dialectical Behavior Therapy Terminology',
        'url': 'https://sonaveeb.ee/ds/dkt',
        'contact': 'dkteesti@gmail.com'
    },
    'kriis': {
        'name': 'Crisis Counseling Terminology',
        'url': 'https://sonaveeb.ee/ds/kriis',
        'contact': 'Kirsti Talu (kirstit@gmail.com)'
    },
    'TAI': {
        'name': 'Health Terminology',
        'url': 'https://sonaveeb.ee/ds/TAI',
        'contact': 'Ruth Erm (ruth.erm@tai.ee)'
    }
}

# All possible letters (Estonian + Russian)
ALL_LETTERS = [
    # Estonian letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'õ', 'ä', 'ö', 'ü',
    # Russian letters (some databases contain these)
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н',
    'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я'
]


class TermParser(HTMLParser):
    """HTML parser for extracting terms from Sõnaveeb pages"""

    def __init__(self, database_code: str):
        super().__init__()
        self.database = database_code
        self.terms = []
        self.current_link = None
        self.in_term_link = False

    def handle_starttag(self, tag, attrs):
        """Find term links"""
        if tag == 'a':
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href', '')

            # Check if this is a term link
            # Format: /search/unif/dlall/DATABASE/TERM
            if f'/search/unif/dlall/{self.database}/' in href:
                self.in_term_link = True
                self.current_link = href

    def handle_data(self, data):
        """Extract term text"""
        if self.in_term_link and data.strip():
            self.terms.append({
                'term': data.strip(),
                'link': f"https://sonaveeb.ee{self.current_link}"
            })

    def handle_endtag(self, tag):
        """End term reading"""
        if tag == 'a':
            self.in_term_link = False
            self.current_link = None


def find_available_letters(database: str) -> List[str]:
    """
    Finds which letters are available in the database

    Args:
        database: Database code (e.g. 'skt')

    Returns:
        List of available letters
    """
    url = f"https://sonaveeb.ee/ds/{database}"

    try:
        print(f"  🔍 Checking available letters: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Find letter links in HTML
        # Format: <a href="/ds/DATABASE/LETTER">
        import re
        pattern = rf'href="/ds/{database}/([^"]+)"'
        matches = re.findall(pattern, response.text)

        letters = []
        for href_letter in matches:
            # Decode URL-encoded letter
            letter = urllib.parse.unquote(href_letter)
            # Take only single-character length (not "search" etc)
            # Keep uppercase too (EKI sometimes uses A, sometimes a)
            if len(letter) == 1 and (letter.lower() in ALL_LETTERS or letter in ALL_LETTERS):
                letters.append(letter)

        # Remove duplicates and sort
        letters = sorted(list(set(letters)))

        print(f"    ✓ Found {len(letters)} letters: {' '.join(letters)}")
        return letters

    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  Error finding letters: {e}")
        print(f"    ℹ️  Using all letters")
        return ALL_LETTERS


def collect_term_details(term_link: str) -> Dict:
    """
    Collects full term data from EKI page

    Args:
        term_link: Link to term page

    Returns:
        Dictionary with term details
    """
    try:
        response = requests.get(term_link, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        details = {
            'language': None,
            'synonyms': [],
            'definition': None
        }

        # Find homonym-list-item
        homonym = soup.find('li', class_='homonym-list-item')
        if homonym:
            # Find language code
            lang_code = homonym.find('span', class_='lang-code')
            if lang_code:
                details['language'] = lang_code.get('title', lang_code.get_text(strip=True))

            # Find synonyms
            matches = homonym.find('span', class_='homonym__matches')
            if matches:
                synonyms_text = matches.get_text(strip=True)
                if synonyms_text:
                    details['synonyms'] = [s.strip() for s in synonyms_text.split(',')]

            # Find definition
            definition = homonym.find('p')
            if definition:
                details['definition'] = definition.get_text(strip=True)

        return details

    except Exception as e:
        print(f"      ⚠️  Error loading details: {e}")
        return {
            'language': None,
            'synonyms': [],
            'definition': None
        }


def collect_terms_by_letter(database: str, letter: str, collect_details: bool = True) -> List[Dict]:
    """
    Collects terms from one letter

    Args:
        database: Database code (e.g. 'skt')
        letter: Letter (e.g. 'a')
        collect_details: Whether to collect term details (slower)

    Returns:
        List of terms with all data
    """
    url = f"https://sonaveeb.ee/ds/{database}/{letter}"

    try:
        print(f"  Loading: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        parser = TermParser(database)
        parser.feed(response.text)

        # Decode Estonian letters and collect details
        terms = []
        for item in parser.terms:
            term_name = urllib.parse.unquote(item['term'])
            term_link = item['link']

            term_dict = {
                'term': term_name,
                'link': term_link,
                'letter': letter
            }

            # If requested, collect details too
            if collect_details:
                print(f"    → {term_name}", end='', flush=True)
                details = collect_term_details(term_link)
                term_dict.update(details)

                # Show what was found
                if details.get('definition'):
                    def_preview = details['definition'][:50] + '...' if len(details['definition']) > 50 else details['definition']
                    print(f" ✓ ({details.get('language', '?')}) {def_preview}")
                else:
                    print(f" ⚠ (no definition)")

                # Small pause to not overload server
                time.sleep(0.3)

            terms.append(term_dict)

        print(f"    ✓ Found {len(terms)} terms" + (" (with details)" if collect_details else ""))
        return terms

    except requests.exceptions.RequestException as e:
        print(f"    ✗ Error: {e}")
        return []


def collect_all_terms(database_code: str) -> Dict:
    """
    Collects all terms from database

    Args:
        database_code: Database code (e.g. 'skt', 'dkt')

    Returns:
        Dictionary with all terms and metadata
    """
    if database_code not in TERM_DATABASES:
        print(f"❌ Error: Unknown database '{database_code}'")
        print(f"Available options: {', '.join(TERM_DATABASES.keys())}")
        sys.exit(1)

    info = TERM_DATABASES[database_code]
    print(f"\n🔍 Collecting terms: {info['name']}")
    print(f"📍 URL: {info['url']}")
    print(f"📧 Contact: {info['contact']}\n")

    # Find available letters
    available_letters = find_available_letters(database_code)
    print()

    all_terms = []

    # Go through only available letters
    for letter in available_letters:
        terms = collect_terms_by_letter(database_code, letter)
        all_terms.extend(terms)

        # Small pause to not overload server
        time.sleep(0.5)

    # Remove duplicates (if any)
    unique = {}
    for t in all_terms:
        if t['term'] not in unique:
            unique[t['term']] = t

    all_terms = list(unique.values())

    # Sort alphabetically
    all_terms.sort(key=lambda x: x['term'].lower())

    print(f"\n✅ Total collected: {len(all_terms)} unique terms")

    # Build result with metadata
    result = {
        'metadata': {
            'database_code': database_code,
            'database_name': info['name'],
            'database_url': info['url'],
            'contact': info['contact'],
            'collection_date': datetime.now().isoformat(),
            'term_count': len(all_terms)
        },
        'terms': all_terms
    }

    return result


def save_json(data: Dict, database_code: str) -> str:
    """
    Saves terms to JSON file

    Args:
        data: Term data with metadata
        database_code: Database code

    Returns:
        Saved file path
    """
    import os

    # Create output folder if needed
    output_dir = '../data/eki_terms'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    date = datetime.now().strftime('%Y%m%d')
    filename = f"{output_dir}/eki_{database_code}_{date}.json"

    # Save JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Saved: {filename}")

    return filename


def main():
    """Main function"""

    if len(sys.argv) < 2:
        print("Usage: python3 eki_collector.py <database_code>")
        print(f"\nAvailable databases:")
        for code, info in TERM_DATABASES.items():
            print(f"  {code:6} - {info['name']}")
        sys.exit(1)

    database_code = sys.argv[1]

    # Collect terms
    data = collect_all_terms(database_code)

    # Save JSON
    filepath = save_json(data, database_code)

    print(f"\n✅ Done!")
    print(f"📊 Collected {data['metadata']['term_count']} terms")
    print(f"📁 File: {filepath}")


if __name__ == '__main__':
    main()
