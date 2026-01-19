#!/usr/bin/env python3
"""
Migrate existing reviewed terms to add actions array.

One-time migration script to add actions to terms reviewed before
the actions tracking feature was implemented.
"""

from pathlib import Path
from tools.filemanage import load_json_file, save_json_file

def migrate_reviewed_terms(terms):
    """Add actions array to already reviewed terms."""
    migrated_count = 0

    for term in terms:
        # Skip if already has actions
        if 'actions' in term:
            continue

        # Only migrate reviewed terms
        if not term.get('reviewedAt'):
            continue

        # Determine action type
        if len(term.get('meanings', [])) == 1:
            # Single meaning likely means it was merged
            action_type = 'merged'
        else:
            # Multiple meanings means it was accepted
            action_type = 'accepted'

        # Add actions array
        term['actions'] = [{
            'type': action_type,
            'date': term['reviewedAt']
        }]

        migrated_count += 1
        print(f"  ✅ {term['term']}: added '{action_type}' action")

    return migrated_count


def main():
    """Run migration."""
    input_file = Path('data/1_extracted/foundation_raw.json')

    print(f"📖 Loading: {input_file}")
    terms = load_json_file(input_file)
    print(f"✅ Loaded {len(terms)} terms\n")

    print("🔄 Migrating reviewed terms...")
    migrated = migrate_reviewed_terms(terms)

    if migrated > 0:
        print(f"\n💾 Saving changes...")
        save_json_file(terms, input_file)
        print(f"✅ Migration complete: {migrated} terms updated\n")
    else:
        print(f"\nℹ️  No terms to migrate\n")


if __name__ == '__main__':
    main()
