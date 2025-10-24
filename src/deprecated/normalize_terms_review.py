#!/usr/bin/env python3
"""
Interactive term normalization review script.
Detects normalization needs based on Issue #25 decisions.
Adds normalizationAction metadata for future TBX transformation.

Issue #25 - Term normalization policy decisions
"""

import sys
from pathlib import Path
from datetime import datetime
from utils import load_json_file, save_json_file


# ============================================================
# CONSTANTS
# ============================================================

# Category types from Issue #25
CATEGORY_PARENTHESES = "split_parentheses"
CATEGORY_ASTERISK = "remove_asterisk"
CATEGORY_MULTIPLE_COMMA = "split_multiple_comma"
CATEGORY_MULTIPLE_SLASH = "split_multiple_slash"
CATEGORY_SEEALSO_FORMAT = "clean_seealso"


# ============================================================
# DETECTION FUNCTIONS - PARENTHESES
# ============================================================

def detect_parentheses_notation(term):
    """
    Detect parentheses notation like (s), (ren), (es).

    Issue #25 Category 5: Singular/Plural
    Examples: caregiver(s), foster child(ren), honor(s) student
    Decision: Split into separate terms, remove notation
    """
    if '(' not in term or ')' not in term:
        return None

    # Pattern: word(s)
    if '(s)' in term:
        base = term.replace('(s)', '').strip()
        plural = base + 's'
        return {
            'category': CATEGORY_PARENTHESES,
            'pattern': '(s)',
            'suggestion': [base, plural]
        }

    # Pattern: word(ren)
    if '(ren)' in term:
        base = term.replace('(ren)', '').strip()
        plural = base + 'ren'
        return {
            'category': CATEGORY_PARENTHESES,
            'pattern': '(ren)',
            'suggestion': [base, plural]
        }

    # Pattern: word(es)
    if '(es)' in term:
        base = term.replace('(es)', '').strip()
        plural = base + 'es'
        return {
            'category': CATEGORY_PARENTHESES,
            'pattern': '(es)',
            'suggestion': [base, plural]
        }

    return None


# ============================================================
# DETECTION FUNCTIONS - ASTERISK
# ============================================================

def detect_asterisk(term):
    """
    Detect asterisk footnote markers.

    Issue #25 Category 7: Asterisks
    Examples: counseling*, para-alcoholic*, one's self *
    Decision: Remove asterisk, move explanation to note field
    """
    if '*' not in term:
        return None

    clean_term = term.replace('*', '').strip()
    return {
        'category': CATEGORY_ASTERISK,
        'suggestion': {'cleanTerm': clean_term}
    }


# ============================================================
# DETECTION FUNCTIONS - MULTIPLE TERMS
# ============================================================

def detect_multiple_terms_comma(term):
    """
    Detect multiple terms separated by comma.

    Issue #25 Category 4: Multiple terms in one field
    Examples: hero, hero child | distorted image, distorted self-image
    Decision: Split into separate terms, same concept
    """
    # Skip if has parentheses (that's different category)
    if '(' in term:
        return None

    if ', ' not in term:
        return None

    parts = [p.strip() for p in term.split(',')]
    if len(parts) > 1:
        return {
            'category': CATEGORY_MULTIPLE_COMMA,
            'suggestion': parts
        }

    return None


def detect_multiple_terms_slash(term):
    """
    Detect multiple terms separated by slash.

    Issue #25 Category 4: Multiple terms in one field
    Examples: Annual Business Conference/ABC | PTSD/Post Traumatic Stress Disorder
    Decision: Split into separate terms, same concept
    """
    if '/' not in term:
        return None

    parts = [p.strip() for p in term.split('/')]
    if len(parts) > 1:
        return {
            'category': CATEGORY_MULTIPLE_SLASH,
            'suggestion': parts
        }

    return None


# ============================================================
# DETECTION FUNCTIONS - SEEALSO FORMAT
# ============================================================

def detect_seealso_issues(term_data):
    """
    Detect seeAlso with explanations instead of terms.

    Issue #25 Category 8: "See also" format
    Example: "trauma for further references in the literature"
    Decision: Flag suspicious entries for manual review, extract term only
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
            'category': CATEGORY_SEEALSO_FORMAT,
            'suggestion': issues
        }

    return None


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_term_header(term_data, current, total):
    """Display term header with basic information."""
    print("\n" + "="*60)
    print(f"Term {current}/{total}: {term_data['term']}")

    if term_data.get('grammaticalType'):
        print(f"Type: ({term_data['grammaticalType']})")

    if term_data.get('meanings'):
        definition = term_data['meanings'][0].get('definition', '')
        if definition:
            short_def = definition[:100] + "..." if len(definition) > 100 else definition
            print(f"Definition: {short_def}")

    print("="*60)


def display_issue_details(issue):
    """Display detected issue with suggestions."""
    print(f"\n⚠️  Issue detected: {issue['category']}")

    if issue['category'] == CATEGORY_PARENTHESES:
        print(f"   Pattern: {issue['pattern']}")
        print(f"   Suggestion: Split into {len(issue['suggestion'])} terms")
        for i, term in enumerate(issue['suggestion'], 1):
            print(f"      {i}. \"{term}\"")

    elif issue['category'] == CATEGORY_ASTERISK:
        print(f"   Suggestion: Remove asterisk")
        print(f"      Clean term: \"{issue['suggestion']['cleanTerm']}\"")

    elif issue['category'] in [CATEGORY_MULTIPLE_COMMA, CATEGORY_MULTIPLE_SLASH]:
        sep = "," if issue['category'] == CATEGORY_MULTIPLE_COMMA else "/"
        print(f"   Separator: '{sep}'")
        print(f"   Suggestion: Split into {len(issue['suggestion'])} terms")
        for i, term in enumerate(issue['suggestion'], 1):
            print(f"      {i}. \"{term}\"")

    elif issue['category'] == CATEGORY_SEEALSO_FORMAT:
        print(f"   seeAlso field has suspicious entries:")
        for item in issue['suggestion']:
            print(f"      \"{item['entry']}\" - {item['reason']}")


def display_action_menu():
    """Display available actions for current term."""
    print("\nWhat to do?")
    print("  [1] Accept suggestion")
    print("  [2] Edit manually")
    print("  [3] Skip (review later)")
    print("  [4] Mark as correct (no action)")


# ============================================================
# USER INTERACTION
# ============================================================

def get_user_choice(prompt, valid_choices):
    """Get validated user input."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")


def prompt_user_action():
    """Ask user what action to take."""
    display_action_menu()
    return get_user_choice("\nYour choice (1-4): ", ['1', '2', '3', '4'])


# ============================================================
# MANUAL EDIT HANDLERS
# ============================================================

def handle_manual_edit(issue):
    """Handle manual editing of suggestions."""
    print("\n📝 Enter your changes:")

    if issue['category'] in [CATEGORY_PARENTHESES, CATEGORY_MULTIPLE_COMMA, CATEGORY_MULTIPLE_SLASH]:
        print("Enter terms (comma separated):")
        user_input = input("> ").strip()
        terms = [t.strip() for t in user_input.split(',')]
        return {
            'type': issue['category'],
            'data': terms
        }

    elif issue['category'] == CATEGORY_ASTERISK:
        print("Enter clean term:")
        clean = input("> ").strip()
        print("Enter note (optional, press Enter to skip):")
        note = input("> ").strip()
        return {
            'type': issue['category'],
            'data': {
                'cleanTerm': clean,
                'note': note if note else None
            }
        }

    elif issue['category'] == CATEGORY_SEEALSO_FORMAT:
        print("Enter corrected seeAlso entries (comma separated):")
        user_input = input("> ").strip()
        terms = [t.strip() for t in user_input.split(',')]
        return {
            'type': issue['category'],
            'data': terms
        }

    return None


# ============================================================
# TERM PROCESSING
# ============================================================

def collect_all_issues(term_data):
    """Collect all detected issues for a term."""
    issues = []

    # Category 5: Parentheses
    parentheses = detect_parentheses_notation(term_data['term'])
    if parentheses:
        issues.append(parentheses)

    # Category 7: Asterisk
    asterisk = detect_asterisk(term_data['term'])
    if asterisk:
        issues.append(asterisk)

    # Category 4: Multiple terms (comma)
    comma = detect_multiple_terms_comma(term_data['term'])
    if comma:
        issues.append(comma)

    # Category 4: Multiple terms (slash)
    slash = detect_multiple_terms_slash(term_data['term'])
    if slash:
        issues.append(slash)

    # Category 8: seeAlso format
    seealso = detect_seealso_issues(term_data)
    if seealso:
        issues.append(seealso)

    return issues


def save_normalization_action(term_data, action_type, action_data):
    """Save normalization action to term data."""
    term_data['normalizationAction'] = {
        'type': action_type,
        'data': action_data
    }
    term_data['reviewedAt'] = datetime.now().isoformat()
    term_data['needsReview'] = False


def process_single_issue(term_data, issue, stats):
    """Process one detected issue with user interaction."""
    display_issue_details(issue)
    choice = prompt_user_action()

    if choice == '1':  # Accept suggestion
        save_normalization_action(term_data, issue['category'], issue['suggestion'])
        stats['accepted'] += 1
        print("✅ Suggestion accepted")
        return True

    elif choice == '2':  # Edit manually
        action = handle_manual_edit(issue)
        if action:
            save_normalization_action(term_data, action['type'], action['data'])
            stats['edited'] += 1
            print("✅ Manual edit saved")
            return True

    elif choice == '3':  # Skip
        stats['skipped'] += 1
        print("⏭️  Skipped")
        return False

    elif choice == '4':  # Mark as correct
        term_data['reviewedAt'] = datetime.now().isoformat()
        term_data['needsReview'] = False
        stats['no_action'] += 1
        print("✅ Marked as correct")
        return True

    return False


def process_term(term_data, stats):
    """Process one term - detect and handle all issues."""
    issues = collect_all_issues(term_data)

    if not issues:
        return False

    # Process each detected issue
    modified = False
    for issue in issues:
        if process_single_issue(term_data, issue, stats):
            modified = True

    return modified


# ============================================================
# STATISTICS
# ============================================================

def display_final_statistics(stats):
    """Display review session statistics."""
    print("\n" + "="*60)
    print("✅ Review complete!")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"   Total reviewed: {stats['total_reviewed']}")
    print(f"   - Accepted: {stats['accepted']}")
    print(f"   - Edited: {stats['edited']}")
    print(f"   - Skipped: {stats['skipped']}")
    print(f"   - No action: {stats['no_action']}")
    print()


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Main review workflow."""
    input_file = Path("data/1_extracted/foundation_raw.json")

    # Configure UTF-8 for input
    sys.stdin.reconfigure(encoding='utf-8')

    # Load data
    print("\n🔍 Term Normalization Review")
    print("="*60)
    print(f"\n📂 Loading: {input_file}")

    terms = load_json_file(input_file)
    print(f"✅ Loaded {len(terms)} terms\n")

    # Initialize statistics
    stats = {
        'accepted': 0,
        'edited': 0,
        'skipped': 0,
        'no_action': 0,
        'total_reviewed': 0
    }

    # Process each term
    for i, term_data in enumerate(terms, 1):
        print(f"\n📍 Progress: {i}/{len(terms)}")

        display_term_header(term_data, i, len(terms))

        had_issues = process_term(term_data, stats)

        if had_issues:
            stats['total_reviewed'] += 1

            # Save after each term
            print("💾 Saving...", end=" ", flush=True)
            save_json_file(terms, input_file)
            print("✅ Saved!")

    # Display final statistics
    display_final_statistics(stats)

    print(f"💾 All changes saved to: {input_file}\n")


if __name__ == '__main__':
    main()
