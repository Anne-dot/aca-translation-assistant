#!/usr/bin/env python3
"""
Interactive review script for multiple meanings.
Quality control for auto-split extraction logic.

Issue #21 - PHASE 1, STEP 1.1 Quality Control
"""

from pathlib import Path
from datetime import datetime
from utils import load_json_file, save_json_file


# ============================================================
# STATISTICS
# ============================================================

def count_terms_by_review_status(terms):
    """Count terms by review status and meanings."""
    total = len(terms)
    flagged = sum(1 for t in terms if t.get('needsReview', False))
    reviewed = sum(1 for t in terms if t.get('reviewedAt') is not None)
    multiple_meanings = sum(1 for t in terms if len(t.get('meanings', [])) > 1)

    return {
        'total': total,
        'flagged': flagged,
        'reviewed': reviewed,
        'remaining': flagged - reviewed,
        'multiple_meanings': multiple_meanings
    }


def display_statistics(stats):
    """Display term statistics in readable format."""
    print(f"\n📊 Statistics:")
    print(f"   Total terms: {stats['total']}")
    print(f"   Multiple meanings: {stats['multiple_meanings']}")
    print(f"   Flagged for review: {stats['flagged']}")
    print(f"   Already reviewed: {stats['reviewed']}")
    print(f"   Remaining: {stats['remaining']}\n")


# ============================================================
# TERM DISPLAY
# ============================================================

def display_term_header(term, index, total):
    """Display term header with basic info."""
    print(f"\n{'='*60}")
    print(f"Term {index}/{total}: {term['term']}")
    if term.get('grammaticalType'):
        print(f"Type: ({term['grammaticalType']})")
    if term.get('seeAlso'):
        print(f"See also: {', '.join(term['seeAlso'])}")
    if term.get('reviewNotes'):
        print(f"📝 Review notes:")
        for note in term['reviewNotes']:
            print(f"   - {note['note']} ({note['date'][:10]})")
    print(f"{'='*60}\n")


def display_single_meaning(meaning, meaning_num=None):
    """Display one meaning with all fields."""
    if meaning_num is not None:
        print(f"Meaning {meaning_num}:")

    print(f"  Definition: {meaning.get('definition', 'N/A')}")

    synonyms = meaning.get('synonyms', [])
    if synonyms:
        print(f"  Synonyms: {', '.join(synonyms)}")

    example = meaning.get('usageExample', '')
    if example:
        print(f"  Example: {example}")

    print()


def display_all_meanings(meanings):
    """Display all meanings for a term."""
    if len(meanings) == 1:
        display_single_meaning(meanings[0])
    else:
        for i, meaning in enumerate(meanings, 1):
            display_single_meaning(meaning, i)


def display_page_references(page_refs):
    """Display page references if present."""
    if page_refs:
        print(f"Page References:\n{page_refs}\n")


# ============================================================
# USER INTERACTION
# ============================================================

def display_review_menu():
    """Display main menu options."""
    print("\n" + "="*60)
    print("  Foundation Glossary Review")
    print("="*60)
    print("\nOptions:")
    print("  [1] Review flagged terms only (needsReview: true)")
    print("  [2] Review all terms")
    print("  [3] Show statistics and exit")
    print("  [q] Quit\n")


def get_user_choice(prompt, valid_choices):
    """Get validated user input."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")


def display_term_action_menu():
    """Display actions available for current term."""
    print("Actions:")
    print("  [a] Accept - Auto-split is correct")
    print("  [e] Edit - Modify meanings")
    print("  [m] Merge - Should be single meaning")
    print("  [f] Flag - Mark for review")
    print("  [s] Skip - Review later")
    print("  [q] Quit review\n")


def get_review_action():
    """Get user's review action for current term."""
    return get_user_choice("Your choice: ", ['a', 'e', 'm', 'f', 's', 'q'])


# ============================================================
# REVIEW ACTIONS
# ============================================================

def mark_term_as_reviewed(term):
    """Mark term as reviewed with timestamp."""
    term['reviewedAt'] = datetime.now().isoformat()
    term['needsReview'] = False
    return term


def accept_term(term):
    """Accept auto-split as correct."""
    print("✅ Accepted!\n")
    return mark_term_as_reviewed(term)


def skip_term(term):
    """Skip term for later review."""
    print("⏭️  Skipped\n")
    return term


def flag_term_for_review(term):
    """Flag term for review with optional note."""
    note = input("Reason for flagging (optional): ").strip()

    term['needsReview'] = True
    if note:
        if 'reviewNotes' not in term:
            term['reviewNotes'] = []
        term['reviewNotes'].append({
            'date': datetime.now().isoformat(),
            'note': note
        })

    print("🚩 Flagged for review!\n")
    return term


# ============================================================
# EDIT FUNCTIONALITY - FIELD OPERATIONS
# ============================================================

def display_current_field_value(field_name, current_value, is_list=False):
    """Display current value of a field."""
    print(f"\nCurrent {field_name}:")
    if is_list:
        display_value = ', '.join(current_value) if current_value else 'N/A'
    else:
        display_value = current_value if current_value else 'N/A'
    print(f"  {display_value}")


def display_field_edit_options():
    """Display options for editing a field."""
    print(f"\nOptions:")
    print(f"  [k] Keep current value")
    print(f"  [e] Enter new value")
    print(f"  [d] Delete (set to empty)")


def get_new_field_value(is_list):
    """Get new value from user input."""
    if is_list:
        new_value = input("Enter comma-separated values: ").strip()
        if new_value:
            return [item.strip() for item in new_value.split(',')]
        return []
    else:
        return input("Enter new value: ").strip()


def edit_single_field(field_name, current_value, is_list=False):
    """Edit a single field with user interaction."""
    display_current_field_value(field_name, current_value, is_list)
    display_field_edit_options()

    choice = get_user_choice("Your choice: ", ['k', 'e', 'd'])

    if choice == 'k':
        return current_value
    elif choice == 'd':
        return [] if is_list else ''
    elif choice == 'e':
        return get_new_field_value(is_list)


# ============================================================
# EDIT FUNCTIONALITY - MEANING OPERATIONS
# ============================================================

def edit_single_meaning(meaning):
    """Edit all fields of one meaning."""
    print("\n📝 Editing meaning fields...\n")

    new_meaning = {}

    # Edit definition
    new_meaning['definition'] = edit_single_field(
        'definition',
        meaning.get('definition', ''),
        is_list=False
    )

    # Edit synonyms
    new_meaning['synonyms'] = edit_single_field(
        'synonyms',
        meaning.get('synonyms', []),
        is_list=True
    )

    # Edit usage example
    new_meaning['usageExample'] = edit_single_field(
        'usageExample',
        meaning.get('usageExample', ''),
        is_list=False
    )

    return new_meaning


def select_meaning_to_edit(meanings):
    """Let user select which meaning to edit."""
    if len(meanings) == 1:
        return 0

    print(f"\nWhich meaning to edit?")
    for i in range(len(meanings)):
        print(f"  [{i+1}] Meaning {i+1}")
    print(f"  [0] Cancel")

    valid_choices = [str(i) for i in range(len(meanings) + 1)]
    choice = get_user_choice("Select meaning: ", valid_choices)

    choice_num = int(choice)
    if choice_num == 0:
        return None
    return choice_num - 1


def edit_term_meanings(term):
    """Edit meanings of a term."""
    meanings = term.get('meanings', [])

    meaning_index = select_meaning_to_edit(meanings)

    if meaning_index is None:
        print("❌ Edit cancelled\n")
        return term

    edited_meaning = edit_single_meaning(meanings[meaning_index])
    meanings[meaning_index] = edited_meaning

    term['meanings'] = meanings
    print("✅ Meaning edited!\n")

    return mark_term_as_reviewed(term)


# ============================================================
# MERGE FUNCTIONALITY
# ============================================================

def combine_list_fields(list1, list2):
    """Combine two lists, removing duplicates."""
    combined = list1 + list2
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for item in combined:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def merge_two_meanings(meaning1, meaning2):
    """Merge two meanings into one."""
    merged = {
        'definition': f"{meaning1.get('definition', '')} {meaning2.get('definition', '')}".strip(),
        'synonyms': combine_list_fields(
            meaning1.get('synonyms', []),
            meaning2.get('synonyms', [])
        ),
        'usageExample': f"{meaning1.get('usageExample', '')} {meaning2.get('usageExample', '')}".strip()
    }
    return merged


def merge_all_meanings(meanings):
    """Merge multiple meanings into single meaning."""
    if len(meanings) == 1:
        return meanings

    merged = meanings[0]
    for meaning in meanings[1:]:
        merged = merge_two_meanings(merged, meaning)

    return [merged]


def merge_term_meanings(term):
    """Merge all meanings of a term into one."""
    meanings = term.get('meanings', [])

    if len(meanings) == 1:
        print("⚠️  Term already has single meaning!\n")
        return term

    print(f"\n⚠️  This will merge {len(meanings)} meanings into 1.")
    confirm = get_user_choice("Continue? [y/n]: ", ['y', 'n'])

    if confirm == 'n':
        print("❌ Merge cancelled\n")
        return term

    term['meanings'] = merge_all_meanings(meanings)
    print("✅ Meanings merged!\n")

    return mark_term_as_reviewed(term)


# ============================================================
# FILTERING
# ============================================================

def filter_terms_for_review(terms, review_mode):
    """Filter terms based on review mode."""
    if review_mode == '1':  # Flagged only
        return [t for t in terms if t.get('needsReview', False)]
    elif review_mode == '2':  # All terms
        return terms
    return []


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Main review workflow."""
    input_file = Path("data/1_extracted/foundation_raw.json")

    # Load data
    print(f"\n📖 Loading: {input_file}")
    terms = load_json_file(input_file)
    print(f"✅ Loaded {len(terms)} terms\n")

    # Show menu
    display_review_menu()
    choice = get_user_choice("Select option: ", ['1', '2', '3', 'q'])

    if choice == 'q':
        print("\n👋 Goodbye!\n")
        return

    if choice == '3':
        # Show stats and exit
        stats = count_terms_by_review_status(terms)
        display_statistics(stats)
        return

    # Filter terms for review
    terms_to_review = filter_terms_for_review(terms, choice)

    if not terms_to_review:
        print("⚠️  No terms to review!\n")
        return

    print(f"\n🔍 Reviewing {len(terms_to_review)} terms...\n")

    # Review loop
    modified = False
    for i, term in enumerate(terms_to_review, 1):
        display_term_header(term, i, len(terms_to_review))
        display_all_meanings(term.get('meanings', []))
        display_page_references(term.get('pageReferences', ''))

        display_term_action_menu()
        action = get_review_action()

        if action == 'q':
            print("\n⏸️  Review paused\n")
            break
        elif action == 'a':
            accept_term(term)
            modified = True
        elif action == 's':
            skip_term(term)
        elif action == 'f':
            flag_term_for_review(term)
            modified = True
        elif action == 'e':
            edit_term_meanings(term)
            modified = True
        elif action == 'm':
            merge_term_meanings(term)
            modified = True

    # Save if modified
    if modified:
        print(f"\n💾 Saving changes to: {input_file}")
        save_json_file(terms, input_file)
        print("✅ Saved!\n")
    else:
        print("\n📝 No changes made\n")


if __name__ == "__main__":
    main()
