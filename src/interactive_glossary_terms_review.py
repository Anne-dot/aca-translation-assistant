#!/usr/bin/env python3
"""
Interactive review script for multiple meanings.
Quality control for auto-split extraction logic.

Issue #21 - PHASE 1, STEP 1.1 Quality Control
"""

import sys
from pathlib import Path
from datetime import datetime
from utils import load_json_file, save_json_file, collect_normalization_issues


# ============================================================
# STATISTICS
# ============================================================

def count_actions_by_type(terms):
    """Count how many terms have each action type."""
    action_counts = {
        'accepted': 0,
        'merged': 0,
        'edited': 0,
        'flagged': 0
    }

    for term in terms:
        actions = term.get('actions', [])
        if actions:
            # Count based on last action
            last_action = actions[-1]['type']
            if last_action in action_counts:
                action_counts[last_action] += 1

    return action_counts


def calculate_percentage(count, total):
    """Calculate percentage with one decimal place."""
    if total == 0:
        return 0.0
    return round((count / total) * 100, 1)


def count_terms_by_review_status(terms):
    """Count terms by review status, meanings, and actions."""
    total = len(terms)
    flagged = sum(1 for t in terms if t.get('needsReview', False))
    reviewed = sum(1 for t in terms if t.get('reviewedAt') is not None)
    multiple_meanings = sum(1 for t in terms if len(t.get('meanings', [])) > 1)

    action_counts = count_actions_by_type(terms)

    return {
        'total': total,
        'flagged': flagged,
        'reviewed': reviewed,
        'not_reviewed': total - reviewed,
        'remaining_flagged': flagged - reviewed,
        'multiple_meanings': multiple_meanings,
        'actions': action_counts
    }


def display_statistics(stats):
    """Display term statistics with percentages."""
    total = stats['total']

    print(f"\n📊 Statistics:")
    print(f"   Total terms: {total}")

    mm_pct = calculate_percentage(stats['multiple_meanings'], total)
    print(f"   Multiple meanings: {stats['multiple_meanings']} ({mm_pct}%)")

    print(f"\n📝 Review Status:")
    print(f"   Flagged for review: {stats['flagged']} ({calculate_percentage(stats['flagged'], total)}%)")

    reviewed_pct = calculate_percentage(stats['reviewed'], total)
    print(f"   Reviewed: {stats['reviewed']} ({reviewed_pct}%)")

    not_reviewed_pct = calculate_percentage(stats['not_reviewed'], total)
    print(f"   Not reviewed: {stats['not_reviewed']} ({not_reviewed_pct}%)")

    print(f"\n📈 Actions (of {total} total):")
    actions = stats['actions']
    for action_type, count in actions.items():
        pct = calculate_percentage(count, total)
        print(f"   {action_type.capitalize()}: {count} ({pct}%)")

    print()


# ============================================================
# TERM DISPLAY
# ============================================================

def display_complete_term_info(term, title=None, index=None, total=None):
    """
    Display complete term information with all fields.
    Single source for term display - used everywhere (DRY principle).

    Args:
        term: Term dictionary
        title: Custom title (e.g., "FINAL REVIEW", "UPDATED TERM INFO")
        index: Term index (e.g., 1)
        total: Total terms (e.g., 88)
    """
    print(f"\n{'='*60}")

    # Header
    if title:
        if index and total:
            print(f"Term {index}/{total}: {title}")
        else:
            print(title)
    elif index and total:
        print(f"Term {index}/{total}")
    else:
        print("Term Info")

    print(f"{'='*60}\n")

    # Term-level fields
    print(f"Term: {term['term']}")
    print(f"Type: {term.get('grammaticalType', 'N/A')}")

    if term.get('termNote'):
        print(f"termNote: {term['termNote']}")

    if term.get('seeAlso'):
        print(f"seeAlso: {', '.join(term['seeAlso'])}")
    else:
        print(f"seeAlso: N/A")

    # Review notes (numbered)
    if term.get('reviewNotes'):
        print(f"\n📝 Review notes:")
        for i, note in enumerate(term['reviewNotes'], 1):
            if isinstance(note, dict):
                print(f"  {i}. {note['note']} ({note['date'][:10]})")
            else:
                print(f"  {i}. {note}")

    # Meanings
    meanings = term.get('meanings', [])
    if meanings:
        print()
        if len(meanings) == 1:
            # Single meaning
            meaning = meanings[0]
            print("Definition:")
            print(f"  {meaning.get('definition', 'N/A')}")

            if meaning.get('synonyms'):
                print(f"\nSynonyms:")
                print(f"  {', '.join(meaning['synonyms'])}")

            if meaning.get('usageExample'):
                print(f"\nExample:")
                print(f"  {meaning['usageExample']}")
        else:
            # Multiple meanings
            for i, meaning in enumerate(meanings, 1):
                print(f"Meaning {i}:")
                print(f"  Definition: {meaning.get('definition', 'N/A')}")

                if meaning.get('synonyms'):
                    print(f"  Synonyms: {', '.join(meaning['synonyms'])}")

                if meaning.get('usageExample'):
                    print(f"  Example: {meaning['usageExample']}")

                if i < len(meanings):
                    print()

    # Page references
    if term.get('pageReferences'):
        print(f"\nPage References:")
        # Format page references with indentation
        refs = term['pageReferences']
        for line in refs.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")

    print(f"{'='*60}\n")


# ============================================================
# USER INTERACTION
# ============================================================

def display_review_menu(terms):
    """Display main menu options with term counts."""
    # Calculate counts for each filter
    flagged = sum(1 for t in terms if t.get('needsReview', False))
    not_reviewed = sum(1 for t in terms if t.get('reviewedAt') is None)
    reviewed_ok = sum(1 for t in terms
                      if t.get('reviewedAt') is not None
                      and not t.get('needsReview', False))
    reviewed_flagged = sum(1 for t in terms
                           if t.get('reviewedAt') is not None
                           and t.get('needsReview', False))
    total = len(terms)

    print("\n" + "="*60)
    print("  Foundation Glossary Review")
    print("="*60)
    print("\nOptions:")
    print(f"  [1] Flagged ({flagged} terms)")
    print(f"  [2] Not reviewed ({not_reviewed} terms)")
    print(f"  [3] Reviewed - OK ({reviewed_ok} terms)")
    print(f"  [4] Reviewed - Flagged ({reviewed_flagged} terms)")
    print(f"  [5] All terms ({total} terms)")
    print(f"  [6] Show statistics and exit")
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
    print("  [a] Accept - Entry is correct")
    print("  [e] Edit - Modify meanings")
    print("  [t] Edit term fields - grammaticalType, seeAlso")
    print("  [n] Edit review notes")
    print("  [m] Merge - Should be single meaning")
    print("  [f] Flag - Mark for review")
    print("  [s] Skip - Review later")
    print("  [q] Quit review\n")


def get_review_action():
    """Get user's review action for current term."""
    return get_user_choice("Your choice: ", ['a', 'e', 't', 'n', 'm', 'f', 's', 'q'])


# ============================================================
# NORMALIZATION HANDLING - Issue #25
# ============================================================

def display_normalization_issue(issue):
    """Display detected normalization issue with suggestion."""
    print(f"\n{'='*60}")
    print(f"⚠️  NORMALIZATION ISSUE DETECTED")
    print(f"{'='*60}")
    print(f"\nCategory: {issue['category']}")

    if issue['category'] == 'split_parentheses':
        print(f"Pattern: {issue['pattern']}")
        print(f"Suggestion: Split into {len(issue['suggestion'])} terms")
        for i, term in enumerate(issue['suggestion'], 1):
            print(f"   {i}. \"{term}\"")

    elif issue['category'] == 'remove_asterisk':
        print(f"Suggestion: Remove asterisk")
        print(f"   Clean term: \"{issue['suggestion']['cleanTerm']}\"")

    elif issue['category'] in ['split_multiple_comma', 'split_multiple_slash']:
        sep = "," if issue['category'] == 'split_multiple_comma' else "/"
        print(f"Separator: '{sep}'")
        print(f"Suggestion: Split into {len(issue['suggestion'])} terms")
        for i, term in enumerate(issue['suggestion'], 1):
            print(f"   {i}. \"{term}\"")

    elif issue['category'] == 'clean_seealso':
        print(f"seeAlso field has suspicious entries:")
        for item in issue['suggestion']:
            print(f"   \"{item['entry']}\" - {item['reason']}")

    print(f"{'='*60}\n")


def display_normalization_menu():
    """Display normalization action menu."""
    print("Normalization actions:")
    print("  [1] Accept suggestion")
    print("  [2] Edit manually")
    print("  [3] Continue with normal review (ignore)")
    print("  [4] Skip term\n")


def get_normalization_action():
    """Get user's normalization action."""
    return get_user_choice("Your choice (1-4): ", ['1', '2', '3', '4'])


def handle_normalization_edit(issue):
    """Handle manual editing of normalization suggestion."""
    print("\n📝 Enter your changes:")

    if issue['category'] in ['split_parentheses', 'split_multiple_comma', 'split_multiple_slash']:
        print("Enter terms (comma separated):")
        user_input = input("> ").strip()
        terms = [t.strip() for t in user_input.split(',')]
        return {
            'type': issue['category'],
            'data': terms
        }

    elif issue['category'] == 'remove_asterisk':
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

    elif issue['category'] == 'clean_seealso':
        print("Enter corrected seeAlso entries (comma separated):")
        user_input = input("> ").strip()
        terms = [t.strip() for t in user_input.split(',')]
        return {
            'type': issue['category'],
            'data': terms
        }

    return None


def apply_normalization_action(term, action):
    """Apply normalization action to term."""
    term['normalizationAction'] = action
    print(f"\n✅ normalizationAction added: {action['type']}")


def display_updated_term_info(term):
    """Display updated term information after normalization."""
    # Show normalization action if present
    if 'normalizationAction' in term:
        action = term['normalizationAction']
        print(f"\n{'='*60}")
        print(f"normalizationAction: {action['type']}")
        if isinstance(action['data'], list):
            print(f"   → {len(action['data'])} terms: {', '.join(action['data'])}")
        elif isinstance(action['data'], dict):
            if 'cleanTerm' in action['data']:
                print(f"   → Clean term: {action['data']['cleanTerm']}")
        print(f"{'='*60}\n")

    # Show complete term info using DRY function
    display_complete_term_info(term, title="UPDATED TERM INFO")


def handle_normalization_issues(term):
    """
    Check for and handle normalization issues.
    Returns True if issues were handled, False otherwise.
    """
    # Skip if normalization action already applied
    if term.get('normalizationAction'):
        return False

    issues = collect_normalization_issues(term)

    if not issues:
        return False

    # Process each issue
    for issue in issues:
        display_normalization_issue(issue)
        display_normalization_menu()
        choice = get_normalization_action()

        if choice == '1':  # Accept suggestion
            action = {
                'type': issue['category'],
                'data': issue['suggestion']
            }
            apply_normalization_action(term, action)

        elif choice == '2':  # Edit manually
            action = handle_normalization_edit(issue)
            if action:
                apply_normalization_action(term, action)

        elif choice == '3':  # Continue with normal review
            print("⏭️  Skipping normalization, continuing to review...")
            return False

        elif choice == '4':  # Skip term
            print("⏭️  Term skipped")
            return True  # Signal to skip this term entirely

    # Show updated info if normalization was applied
    if 'normalizationAction' in term:
        display_updated_term_info(term)

    return False  # Continue to normal review


# ============================================================
# REVIEW ACTIONS
# ============================================================

def save_with_feedback(terms, file_path):
    """Save with transaction feedback."""
    try:
        print("💾 Saving...", end=" ", flush=True)
        save_json_file(terms, file_path)
        print("✅ Saved!")
        return True
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False


def mark_term_as_reviewed(term, action_type):
    """Mark term as reviewed with timestamp and action."""
    term['reviewedAt'] = datetime.now().isoformat()

    # Ask about review notes cleanup if notes exist
    if term.get('reviewNotes'):
        handle_review_notes_cleanup(term)

    # Clear flag only if no review notes remain
    if not term.get('reviewNotes'):
        term['needsReview'] = False

    if 'actions' not in term:
        term['actions'] = []
    term['actions'].append({
        'type': action_type,
        'date': datetime.now().isoformat()
    })

    return term


def accept_term(term):
    """Accept term as correct."""
    print("✅ Accepted!\n")
    return mark_term_as_reviewed(term, 'accepted')


def skip_term(term):
    """Skip term for later review."""
    print("⏭️  Skipped\n")
    return term


def flag_term_for_review(term):
    """Flag term for review with optional note."""
    note = input("Reason for flagging (optional): ").strip()

    term['needsReview'] = True
    term['reviewedAt'] = datetime.now().isoformat()  # Mark as reviewed

    if note:
        if 'reviewNotes' not in term:
            term['reviewNotes'] = []
        term['reviewNotes'].append({
            'date': datetime.now().isoformat(),
            'note': note
        })

    if 'actions' not in term:
        term['actions'] = []
    term['actions'].append({
        'type': 'flagged',
        'date': datetime.now().isoformat()
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

    return mark_term_as_reviewed(term, 'edited')


def split_grammatical_type(grammatical_type):
    """
    Split grammaticalType if it contains qualifier.

    Examples:
      "n, uncommon" → ("n", "uncommon")
      "adj, idiom" → ("adj", "idiom")
      "n" → ("n", None)

    Returns:
      tuple: (part_of_speech, qualifier)
    """
    if not grammatical_type or ',' not in grammatical_type:
        return (grammatical_type, None)

    parts = [p.strip() for p in grammatical_type.split(',', 1)]
    return (parts[0], parts[1] if len(parts) > 1 else None)


def edit_term_fields(term):
    """Edit term-level fields (grammaticalType, seeAlso). Returns without marking as reviewed."""
    print("\n📝 Editing term fields...\n")

    current_type = term.get('grammaticalType', '')

    # If grammaticalType is missing, ask for it immediately
    if not current_type:
        print("⚠️  grammaticalType is missing\n")

        new_type = edit_single_field(
            'grammaticalType',
            '',
            is_list=False
        )

        # Split grammaticalType if contains qualifier
        pos, qualifier = split_grammatical_type(new_type)
        term['grammaticalType'] = pos

        # Add qualifier to termNote if exists
        if qualifier:
            existing_note = term.get('termNote', '')
            if existing_note:
                term['termNote'] = f"{existing_note}; {qualifier}"
            else:
                term['termNote'] = qualifier
            print(f"\n✅ Split applied:")
            print(f"   grammaticalType: {pos}")
            print(f"   termNote: {qualifier}")

        # Ask if user wants to edit seeAlso too
        edit_seealso = input("\nEdit seeAlso too? [y/N]: ").strip().lower()
        if edit_seealso == 'y':
            current_seealso = term.get('seeAlso', [])
            new_seealso = edit_single_field(
                'seeAlso',
                current_seealso,
                is_list=True
            )
            term['seeAlso'] = new_seealso

    else:
        # grammaticalType exists - show submenu
        print("What to edit?")
        print("  [1] grammaticalType")
        print("  [2] seeAlso")
        print("  [3] Both")
        print("  [0] Cancel\n")

        choice = get_user_choice("Your choice: ", ['1', '2', '3', '0'])

        if choice == '0':
            print("❌ Edit cancelled\n")
            return term

        # Edit grammaticalType
        if choice in ['1', '3']:
            # Check if split suggestion available
            pos, qualifier = split_grammatical_type(current_type)

            if qualifier:
                # Show split preview and ask to apply
                print(f"\nℹ️  Current value will be split:")
                print(f"   Part of speech: {pos}")
                print(f"   Qualifier (→ termNote): {qualifier}\n")

                apply_split = input("Apply split? [Y/n]: ").strip().lower()

                if apply_split in ['', 'y', 'yes']:
                    # Apply split automatically
                    term['grammaticalType'] = pos
                    existing_note = term.get('termNote', '')
                    if existing_note:
                        term['termNote'] = f"{existing_note}; {qualifier}"
                    else:
                        term['termNote'] = qualifier
                    print(f"\n✅ Split applied:")
                    print(f"   grammaticalType: {pos}")
                    print(f"   termNote: {qualifier}")
                else:
                    # User declined - ask for new value
                    new_type = edit_single_field(
                        'grammaticalType',
                        current_type,
                        is_list=False
                    )
                    # Apply to new value entered
                    pos, qualifier = split_grammatical_type(new_type)
                    term['grammaticalType'] = pos
                    if qualifier:
                        existing_note = term.get('termNote', '')
                        if existing_note:
                            term['termNote'] = f"{existing_note}; {qualifier}"
                        else:
                            term['termNote'] = qualifier
                        print(f"\n✅ Split applied:")
                        print(f"   grammaticalType: {pos}")
                        print(f"   termNote: {qualifier}")
            else:
                # No split needed - normal edit
                new_type = edit_single_field(
                    'grammaticalType',
                    current_type,
                    is_list=False
                )
                term['grammaticalType'] = new_type

        # Edit seeAlso
        if choice in ['2', '3']:
            current_seealso = term.get('seeAlso', [])
            new_seealso = edit_single_field(
                'seeAlso',
                current_seealso,
                is_list=True
            )
            term['seeAlso'] = new_seealso

    print("✅ Term fields updated!")

    # Show complete updated info
    display_complete_term_info(term, title="UPDATED TERM INFO")

    # Handle review notes cleanup
    if term.get('reviewNotes'):
        handle_review_notes_cleanup(term)

    return term  # Return without marking as reviewed yet


def edit_review_notes(term):
    """
    Edit or delete review notes without changing term fields.
    Allows user to clean up notes before flagging with new reason.
    """
    if not term.get('reviewNotes'):
        print("⚠️  No review notes to edit\n")
        return term

    # Call cleanup handler
    handle_review_notes_cleanup(term)

    return term


def handle_review_notes_cleanup(term):
    """
    Ask user whether to clear review notes after editing term fields.
    Options: clear all, keep all, or interactive (choose per note).
    """
    # Show existing review notes first
    notes = term['reviewNotes']
    print("Review notes:")
    for i, note in enumerate(notes, 1):
        print(f"  {i}. {note}")
    print()

    print("Clear review notes?")
    print("  [y] Clear all notes")
    print("  [n] Keep all notes")
    print("  [i] Interactive (choose per note)\n")

    choice = get_user_choice("Your choice: ", ['y', 'n', 'i'])

    if choice == 'y':
        # Clear all notes
        del term['reviewNotes']
        print("✅ All review notes cleared\n")

    elif choice == 'i':
        # Interactive - ask about each note
        notes = term['reviewNotes']
        remaining_notes = []

        deleted_count = 0
        for i, note in enumerate(notes, 1):
            # Extract note text (handle both dict and string formats)
            if isinstance(note, dict):
                note_text = f"{note['note']} ({note['date'][:10]})"
            else:
                note_text = note

            # Show note in question
            print(f"\nDelete note #{i}: \"{note_text}\"? [y/N]: ", end="")
            delete = input().strip().lower()

            if delete == 'y':
                deleted_count += 1
                print("✅ Deleted")
            else:
                remaining_notes.append(note)
                print("⏭️  Kept")

        # Update term
        if remaining_notes:
            term['reviewNotes'] = remaining_notes
            print(f"\n✅ {deleted_count} note(s) deleted, {len(remaining_notes)} kept")
        else:
            del term['reviewNotes']
            print(f"\n✅ All {deleted_count} review note(s) deleted")

        # Show updated term info after cleanup
        print()
        display_complete_term_info(term, title="UPDATED TERM INFO")

    # If 'n' - do nothing, keep all notes


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


def display_merge_preview(merged_meaning):
    """Show how merged meaning will look."""
    print("\n" + "="*60)
    print("MERGE PREVIEW")
    print("="*60 + "\n")

    print("Merged Definition:")
    print(f"  {merged_meaning['definition']}\n")

    print("Merged Synonyms:")
    if merged_meaning['synonyms']:
        print(f"  {', '.join(merged_meaning['synonyms'])}\n")
    else:
        print("  (none)\n")

    print("Merged Usage Example:")
    print(f"  {merged_meaning['usageExample']}\n")

    print("="*60 + "\n")


def edit_merged_meaning(merged_meaning):
    """Allow editing of merged meaning before saving."""
    print("Would you like to edit the merged result?")
    print("  [y] Yes - Edit fields")
    print("  [n] No - Accept as is")

    choice = get_user_choice("Your choice: ", ['y', 'n'])

    if choice == 'n':
        return merged_meaning

    # Use existing edit functionality
    return edit_single_meaning(merged_meaning)


def merge_term_meanings(term):
    """Merge all meanings of a term into one with preview and edit."""
    meanings = term.get('meanings', [])

    if len(meanings) == 1:
        print("⚠️  Term already has single meaning!\n")
        return term

    print(f"\n⚠️  This will merge {len(meanings)} meanings into 1.")
    confirm = get_user_choice("Continue? [y/n]: ", ['y', 'n'])

    if confirm == 'n':
        print("❌ Merge cancelled\n")
        return term

    # Merge meanings
    merged_meanings = merge_all_meanings(meanings)
    merged_meaning = merged_meanings[0]

    # Show preview
    display_merge_preview(merged_meaning)

    # Allow editing
    final_meaning = edit_merged_meaning(merged_meaning)

    # Confirm final result
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    display_single_meaning(final_meaning)

    confirm_save = get_user_choice("Save this merged meaning? [y/n]: ", ['y', 'n'])

    if confirm_save == 'n':
        print("❌ Merge cancelled\n")
        return term

    term['meanings'] = [final_meaning]
    print("✅ Meanings merged!\n")

    return mark_term_as_reviewed(term, 'merged')


# ============================================================
# FILTERING
# ============================================================

def filter_terms_for_review(terms, review_mode):
    """Filter terms based on review mode."""
    if review_mode == '1':  # Flagged
        return [t for t in terms if t.get('needsReview', False)]
    elif review_mode == '2':  # Not reviewed
        return [t for t in terms if t.get('reviewedAt') is None]
    elif review_mode == '3':  # Reviewed - OK
        return [t for t in terms
                if t.get('reviewedAt') is not None
                and not t.get('needsReview', False)]
    elif review_mode == '4':  # Reviewed - Flagged
        return [t for t in terms
                if t.get('reviewedAt') is not None
                and t.get('needsReview', False)]
    elif review_mode == '5':  # All terms
        return terms
    return []


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Main review workflow."""
    input_file = Path("data/1_extracted/foundation_raw.json")

    # Configure UTF-8 for input
    sys.stdin.reconfigure(encoding='utf-8')

    # Load data
    print(f"\n📖 Loading: {input_file}")
    terms = load_json_file(input_file)
    print(f"✅ Loaded {len(terms)} terms\n")

    # Show menu with counts
    display_review_menu(terms)
    choice = get_user_choice("Select option: ", ['1', '2', '3', '4', '5', '6', 'q'])

    if choice == 'q':
        print("\n👋 Goodbye!\n")
        return

    if choice == '6':
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
        # Determine filter type for display
        if term.get('reviewedAt') and term.get('needsReview', False):
            filter_type = "REVIEWED - FLAGGED"
        elif term.get('reviewedAt'):
            filter_type = "REVIEWED - OK"
        elif term.get('needsReview', False):
            filter_type = "FLAGGED"
        else:
            filter_type = "NOT REVIEWED"

        display_complete_term_info(
            term,
            title=filter_type,
            index=i,
            total=len(terms_to_review)
        )

        # Check for normalization issues (Issue #25)
        skip_to_next = handle_normalization_issues(term)
        if skip_to_next:
            continue

        # Inner loop for term actions (allows returning after [t] edit)
        while True:
            display_term_action_menu()
            action = get_review_action()

            if action == 'q':
                print("\n⏸️  Review paused\n")
                break
            elif action == 'a':
                accept_term(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                break
            elif action == 's':
                skip_term(term)
                break
            elif action == 'f':
                flag_term_for_review(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                # Loop back to menu - don't break (consistent with [t] and [n])
            elif action == 'e':
                edit_term_meanings(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                break
            elif action == 't':
                edit_term_fields(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                # Loop back to menu - don't break
            elif action == 'n':
                edit_review_notes(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                # Loop back to menu - don't break
            elif action == 'm':
                merge_term_meanings(term)
                if save_with_feedback(terms, input_file):
                    modified = True
                break

        # Break outer loop if quit
        if action == 'q':
            break

    # Summary
    if modified:
        print(f"\n✅ All changes saved to: {input_file}\n")
    else:
        print("\n📝 No changes made\n")


if __name__ == "__main__":
    main()
