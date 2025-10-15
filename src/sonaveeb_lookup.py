#!/usr/bin/env python3
"""
Sonaveeb Lookup Script

Lookup 845 Glossary terms in Sonaveeb and collect COMPLETE data.
Following ISO 704 lexicography standards.

Issue: https://github.com/Anne-dot/aca-translation-assistant/issues/7

Key differences from eki_collector.py:
- LOOKUP (search specific terms), not COLLECTOR (get all terms)
- Extracts COMPLETE data: ET equivalents, definitions, "Hea teada", domains
- Handles multiple databases per term
- ET terms as ARRAY, EN definitions as ARRAY

HTML structure reference: eki_analüüs/sõnaveeb_page_abandonment.txt
"""

import time
import signal
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utils import load_json_file, save_json_file

# Global flag for graceful shutdown
shutdown_requested = False


# ==============================================================================
# CONFIGURATION
# ==============================================================================

INPUT_FILE = Path("data") / "aca-glossary-eki.json"
OUTPUT_FILE = Path("data") / "aca-glossary-eki-sonaveeb.json"

SONAVEEB_BASE_URL = "https://sonaveeb.ee"
SEARCH_URL_PATTERN = f"{SONAVEEB_BASE_URL}/search/unif/dlall/dsall/{{term}}/1/eng"

# Rate limiting - be nice to Sonaveeb server
REQUEST_DELAY = 2  # seconds between requests (increased for Selenium)

# Page load wait time
PAGE_LOAD_WAIT = 3  # seconds to wait for JavaScript to load content

# Progress feedback
PROGRESS_INTERVAL = 50  # Show progress every N terms

# Checkpoint settings
CHECKPOINT_INTERVAL = 50  # Save progress every N terms

# Test mode - set to True to test with only first N terms
TEST_MODE = False
TEST_LIMIT = 10


# ==============================================================================
# SIGNAL HANDLING
# ==============================================================================

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    print("\n\n⚠️  Shutdown requested. Finishing current term...")
    print("⚠️  Progress will be saved. You can resume later.\n")
    shutdown_requested = True


# ==============================================================================
# HTML PARSING - DATABASE INFO
# ==============================================================================

def extract_database_code(block_soup) -> Optional[str]:
    """
    Extract database code from search block.

    Looks for links with two patterns:
    - /dlall/skt/term (older HTML structure)
    - /ds/har (newer Selenium HTML structure)

    Returns: 'skt', 'har', etc. or None
    """
    links = block_soup.find_all('a', href=True)
    for link in links:
        href = link['href']

        # Pattern 1: /dlall/{db_code}/term
        if '/dlall/' in href:
            parts = href.split('/')
            try:
                dlall_index = parts.index('dlall')
                if dlall_index + 1 < len(parts):
                    db_code = parts[dlall_index + 1]
                    # Skip 'dsall' (general search parameter)
                    if db_code and db_code != 'dsall':
                        return db_code
            except (ValueError, IndexError):
                continue

        # Pattern 2: /ds/{db_code} (database collection link)
        if href.startswith('/ds/') and '/ds/' in href:
            parts = href.split('/')
            if len(parts) >= 3:
                db_code = parts[2]
                # Valid database codes are short (2-6 chars)
                if db_code and 2 <= len(db_code) <= 6:
                    return db_code

    return None


def extract_database_name(block_soup) -> Optional[str]:
    """Extract database full name from block title."""
    title_elem = block_soup.find('span', class_='search__block-title')
    if title_elem:
        return title_elem.get_text(strip=True)
    return None


def extract_source_id(block_soup) -> Optional[str]:
    """Extract source entry ID from metadata section."""
    id_section = block_soup.find('div', class_='meaning-data__modified')
    if id_section:
        spans = id_section.find_all('span')
        for i, span in enumerate(spans):
            if span.get_text(strip=True) == 'ID' and i + 1 < len(spans):
                return spans[i + 1].get_text(strip=True)
    return None


def extract_last_modified(block_soup) -> Optional[str]:
    """Extract last modified date."""
    date_elem = block_soup.find('span', class_='meaning-data__date')
    if date_elem:
        return date_elem.get_text(strip=True)
    return None


# ==============================================================================
# HTML PARSING - DEFINITIONS
# ==============================================================================

def extract_definitions_by_lang(block_soup, lang_code: str) -> List[str]:
    """
    Extract all definitions for given language code.

    Args:
        block_soup: BeautifulSoup block element
        lang_code: 'est' for Estonian, 'eng' for English

    Returns:
        List of definition strings (can be multiple!)
    """
    definitions = []

    # Find all definition sections
    sections = block_soup.find_all('section', class_='d-flex')

    for section in sections:
        # Check if this section is for our language
        lang_span = section.find('span', class_='lang-code')
        if lang_span and lang_code in lang_span.get('data-original-title', ''):
            # Find all definition values in this section
            def_values = section.find_all('span', class_='definition-value')
            for def_val in def_values:
                definition = def_val.get_text(strip=True)
                if definition:
                    definitions.append(definition)

    return definitions


def extract_et_definitions(block_soup) -> List[str]:
    """Extract Estonian definitions."""
    return extract_definitions_by_lang(block_soup, 'est')


def extract_en_definitions(block_soup) -> List[str]:
    """Extract English definitions."""
    return extract_definitions_by_lang(block_soup, 'eng')


# ==============================================================================
# HTML PARSING - TERMS (ET equivalents)
# ==============================================================================

def extract_et_terms(block_soup) -> List[str]:
    """
    Extract Estonian equivalent terms (not definitions!).

    These are the actual ET translations, shown as links.
    Example: "hüljatus", "ebastabiilsus"
    """
    et_terms = []

    # Find the section with ET terms (has lang-code "eesti")
    # These are shown as <a> links to term pages
    meaning_div = block_soup.find('div', class_='meaning')
    if not meaning_div:
        return et_terms

    # Find all link sections
    link_sections = meaning_div.find_all('div', class_='d-flex')

    for section in link_sections:
        # Check if this section is for Estonian terms
        lang_code = section.find('span', class_='lang-code')
        if lang_code and 'eesti' in lang_code.get('data-original-title', ''):
            # Find all term links
            links = section.find_all('a')
            for link in links:
                term = link.get_text(strip=True)
                if term:
                    et_terms.append(term)

    return et_terms


def extract_en_synonyms(block_soup) -> List[str]:
    """
    Extract English synonyms.

    Example: For "abandonment", synonym is "instability"
    """
    en_synonyms = []

    meaning_div = block_soup.find('div', class_='meaning')
    if not meaning_div:
        return en_synonyms

    link_sections = meaning_div.find_all('div', class_='d-flex')

    for section in link_sections:
        lang_code = section.find('span', class_='lang-code')
        if lang_code and 'inglise' in lang_code.get('data-original-title', ''):
            links = section.find_all('a')
            for link in links:
                synonym = link.get_text(strip=True)
                # Don't include the search term itself
                if synonym:
                    en_synonyms.append(synonym)

    return en_synonyms


# ==============================================================================
# HTML PARSING - NOTES
# ==============================================================================

def extract_hea_teada(block_soup) -> Optional[str]:
    """
    Extract "Hea teada" (Good to know) advisory notes.

    Example: "Väldi: hülgamine/ebastabiilsus, mahajäetus/ebastabiilsus"
    """
    # Find section with "Hea teada" header
    note_sections = block_soup.find_all('section', class_='lang-code__border')

    for section in note_sections:
        note_header = section.find('span', class_='word-notes__note')
        if note_header and 'Hea teada' in note_header.get_text():
            # Find note text
            note_items = section.find_all('li', class_='word-notes__note')
            notes = []
            for item in note_items:
                note_text = item.get_text(strip=True)
                if note_text and note_text != 'Hea teada':
                    notes.append(note_text)

            if notes:
                return ' | '.join(notes)

    return None


# ==============================================================================
# HTML PARSING - MAIN
# ==============================================================================

def parse_search_block(block_soup, search_term: str) -> Optional[Dict]:
    """
    Parse one search block (one database entry).

    Returns variant dict with all extracted data.
    """
    # Extract basic info
    db_code = extract_database_code(block_soup)
    db_name = extract_database_name(block_soup)
    source_id = extract_source_id(block_soup)
    last_modified = extract_last_modified(block_soup)

    if not db_code or not db_name:
        return None

    # Extract terms and definitions
    et_terms = extract_et_terms(block_soup)
    et_definitions = extract_et_definitions(block_soup)
    en_definitions = extract_en_definitions(block_soup)
    en_synonyms = extract_en_synonyms(block_soup)

    # Extract notes
    hea_teada = extract_hea_teada(block_soup)

    # Build variant dict
    variant = {
        "estonian": et_terms if et_terms else [],
        "source": f"sonaveeb_{db_code}",
        "source_name": db_name,
        "source_id": source_id,
        "link": f"{SONAVEEB_BASE_URL}/search/unif/dlall/{db_code}/{search_term}/1/eng",
        "definition_et": et_definitions[0] if et_definitions else None,
        "definitions_et": et_definitions,
        "definitions_en": en_definitions,
        "synonyms_en": en_synonyms,
        "hea_teada": hea_teada,
        "last_modified": last_modified
    }

    return variant


def parse_sonaveeb_page(html_content: str, search_term: str) -> List[Dict]:
    """
    Parse Sonaveeb search results page.

    Returns list of variants (one per database that has this term).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    variants = []

    # Find all search blocks
    blocks = soup.find_all('div', class_='search__block')

    for block in blocks:
        variant = parse_search_block(block, search_term)
        if variant:
            variants.append(variant)

    return variants


# ==============================================================================
# SONAVEEB LOOKUP
# ==============================================================================

def lookup_term_in_sonaveeb(term: str, driver) -> List[Dict]:
    """
    Lookup single term in Sonaveeb using Selenium.

    Args:
        term: English term to search
        driver: Selenium WebDriver instance (reused for efficiency)

    Returns:
        List of variants from all databases.
    """
    search_url = SEARCH_URL_PATTERN.format(term=term)

    try:
        # Load page with Selenium
        driver.get(search_url)

        # Wait for JavaScript to load content
        time.sleep(PAGE_LOAD_WAIT)

        # Get page source after JavaScript execution
        html_content = driver.page_source

        # Parse loaded HTML
        variants = parse_sonaveeb_page(html_content, term)
        return variants

    except Exception as e:
        print(f"      ⚠️  Error looking up {term}: {e}")
        return []


# ==============================================================================
# DATA INTEGRATION
# ==============================================================================

def add_sonaveeb_to_sense(sense: Dict, sonaveeb_variants: List[Dict]):
    """Add Sonaveeb variants to existing sense."""
    if 'sonaveeb_variants' not in sense:
        sense['sonaveeb_variants'] = []

    sense['sonaveeb_variants'].extend(sonaveeb_variants)

    # Update match status if was unmatched
    if sense['match_status'] == 'unmatched' and sonaveeb_variants:
        sense['match_status'] = 'matched'
        sense['match_confidence'] = 'sonaveeb'


def count_already_enriched(glossary_data: Dict) -> int:
    """Count how many terms already have sonaveeb_variants."""
    count = 0
    for term_data in glossary_data.get('terms', {}).values():
        for sense in term_data.get('senses', []):
            if sense.get('sonaveeb_variants'):
                count += 1
                break  # Count term once
    return count


def enrich_with_sonaveeb(glossary_data: Dict) -> Dict:
    """
    Enrich Glossary data with Sonaveeb lookups.

    Supports resume: skips terms that already have sonaveeb_variants.
    Saves progress every CHECKPOINT_INTERVAL terms.

    Args:
        glossary_data: Loaded aca-glossary-eki.json

    Returns:
        Enriched data with sonaveeb_variants added
    """
    global shutdown_requested

    print("🔄 Looking up terms in Sonaveeb...\n")

    terms = glossary_data.get('terms', {})
    total_terms = len(terms)

    # Check if resuming
    already_enriched = count_already_enriched(glossary_data)
    if already_enriched > 0:
        print(f"📍 RESUMING: {already_enriched} terms already enriched")
        print(f"📍 Will process remaining {total_terms - already_enriched} terms\n")

    if TEST_MODE:
        total_terms = min(TEST_LIMIT, total_terms)
        print(f"⚠️  TEST MODE: Processing only first {total_terms} terms\n")

    # Setup Selenium WebDriver (reuse for all lookups)
    print("🌐 Starting Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in background
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ WebDriver ready\n")

    matched_count = 0
    unmatched_count = 0
    multi_source_count = 0
    processed_this_session = 0
    start_time = time.time()

    try:
        for i, (term_key, term_data) in enumerate(list(terms.items())[:total_terms if TEST_MODE else None]):
            # Check graceful shutdown
            if shutdown_requested:
                print("\n⚠️  Stopping after current term...")
                break

            english_term = term_key  # Normalized key is the search term

            # Skip if already has sonaveeb_variants (resume support)
            if term_data.get('senses') and term_data['senses'][0].get('sonaveeb_variants'):
                continue

            processed_this_session += 1
            print(f"\n  🔍 [{i+1}/{total_terms}] Looking up: {english_term}")

            # Lookup in Sonaveeb
            sonaveeb_variants = lookup_term_in_sonaveeb(english_term, driver)

            print(f"    → Found {len(sonaveeb_variants)} variants")

            # Add to first sense
            if term_data.get('senses'):
                add_sonaveeb_to_sense(term_data['senses'][0], sonaveeb_variants)

            # Update stats
            if sonaveeb_variants:
                matched_count += 1
                if len(sonaveeb_variants) > 1:
                    multi_source_count += 1
                print(f"    ✓ {english_term}: {len(sonaveeb_variants)} source(s)")
                # Show sources
                for variant in sonaveeb_variants:
                    print(f"       - {variant['source_name']}: {variant['estonian']}")
            else:
                unmatched_count += 1
                print(f"    ✗ {english_term}: Not found")

            # Checkpoint save
            if processed_this_session % CHECKPOINT_INTERVAL == 0:
                print(f"\n  💾 CHECKPOINT: Saving progress...")
                save_json_file(glossary_data, OUTPUT_FILE)
                elapsed = time.time() - start_time
                avg_time = elapsed / processed_this_session
                remaining = total_terms - (i + 1)
                eta_minutes = (remaining * avg_time) / 60
                print(f"  💾 Saved! Processed {processed_this_session} terms this session")
                print(f"  ⏱️  ETA: ~{eta_minutes:.1f} minutes remaining\n")

            # Progress indicator
            if (i + 1) % PROGRESS_INTERVAL == 0:
                total_enriched = already_enriched + matched_count + unmatched_count
                print(f"\n  📊 Progress: {total_enriched}/{total_terms} terms processed")
                print(f"  📊 This session: {matched_count} found, {unmatched_count} not found\n")

            # Rate limiting
            time.sleep(REQUEST_DELAY)

    finally:
        # Always close driver and save
        driver.quit()
        print("\n🔒 WebDriver closed")

        # Final save
        print("💾 Saving final progress...")
        save_json_file(glossary_data, OUTPUT_FILE)
        print("✅ Progress saved!\n")

    print(f"\n✅ Lookup session complete!")
    print(f"   📊 This session: {matched_count} found, {unmatched_count} not found")
    print(f"   📊 Multiple sources: {multi_source_count}")
    total_enriched = count_already_enriched(glossary_data)
    print(f"   📊 Total enriched: {total_enriched}/{len(terms)} terms\n")

    return glossary_data


def update_metadata(data: Dict, sonaveeb_stats: Dict):
    """Update metadata with Sonaveeb enrichment info."""
    if 'metadata' not in data:
        data['metadata'] = {}

    data['metadata']['sonaveeb_enriched'] = datetime.now().isoformat()
    data['metadata']['sonaveeb_matched'] = sonaveeb_stats['matched']
    data['metadata']['sonaveeb_multi_source'] = sonaveeb_stats['multi_source']


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function."""
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("\n" + "="*60)
    print("  Sonaveeb Lookup")
    print("  Issue #7: Enrich Glossary with Sonaveeb data")
    print("="*60 + "\n")
    print("💡 Press Ctrl+C to stop gracefully (progress will be saved)")
    print("💡 You can resume later - script will skip already enriched terms\n")

    # Load input data
    print(f"📖 Loading: {INPUT_FILE}")
    glossary_data = load_json_file(INPUT_FILE)
    term_count = len(glossary_data.get('terms', {}))
    print(f"✅ Loaded {term_count} terms\n")

    # Enrich with Sonaveeb
    enriched_data = enrich_with_sonaveeb(glossary_data)

    # Calculate final stats
    matched = 0
    multi_source = 0
    for term_data in enriched_data.get('terms', {}).values():
        for sense in term_data.get('senses', []):
            sv_variants = sense.get('sonaveeb_variants', [])
            if sv_variants:
                matched += 1
                if len(sv_variants) > 1:
                    multi_source += 1
                break  # Count term once

    stats = {
        'matched': matched,
        'multi_source': multi_source
    }

    update_metadata(enriched_data, stats)

    # Save results
    print(f"💾 Saving: {OUTPUT_FILE}")
    save_json_file(enriched_data, OUTPUT_FILE)
    print(f"✅ Saved successfully!\n")

    print("="*60)
    print(f"  ✨ Done! Enriched {matched}/{term_count} terms from Sonaveeb")
    if multi_source:
        print(f"  📚 {multi_source} terms found in multiple databases")
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
