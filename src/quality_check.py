#!/usr/bin/env python3
"""
Automated quality check for extracted terms.
Identifies structural issues and flags terms requiring special attention.

Issue #23 - Automated quality check script
"""

from pathlib import Path
from datetime import datetime
from tools.filemanage import load_json_file, save_json_file

#==============================================================================#
# QUALITY CHECK FUNCTIONS                                                      #
#==============================================================================#
def has_missing_type(term):
	return not term.get('grammaticalType', '').strip()

def has_multiple_types(term):
	return ',' in term.get('grammaticalType', '')

def has_idiom(term):
	return 'idiom' in term.get('grammaticalType', '').lower()

def has_missing_definition(term):
	if not meanings := term.get('meanings', []): return True
	return any(
		not meaning.get('definition', '').strip() for meaning in meanings
	)

def has_missing_term(term):
	return not term.get('term', '').strip()



#==============================================================================#
# FLAGGING FUNCTIONS                                                           #
#==============================================================================#
def add_review_note_if_new(term, note_text):
	if 'reviewNotes' not in term: term['reviewNotes'] = []
	
	existing_notes = [note['note'] for note in term['reviewNotes']]
	if note_text not in existing_notes:
		term['reviewNotes'].append({
			'date': datetime.now().isoformat(),
			'note': note_text
		})

def add_flagged_action_if_new(term):
	if 'actions' not in term: term['actions'] = []
	
	action_types = [action['type'] for action in term['actions']]
	if 'flagged' not in action_types:
		term['actions'].append({
			'type': 'flagged',
			'date': datetime.now().isoformat()
		})

def flag_term_for_issue(term, issue_description):
	term['needsReview'] = True
	add_review_note_if_new(term, issue_description)
	add_flagged_action_if_new(term)
	return term



#==============================================================================#
# INFO CHECK FUNCTIONS                                                         #
#==============================================================================#
def has_missing_synonyms(term):
	return not any(
		meaning.get('synonyms') for meaning in term.get('meanings', [])
	)

def has_missing_examples(term):
	return not any(
		meaning.get('usageExample', '').strip() for meaning in term.get('meanings', [])
	)

def has_missing_references(term):
	return not term.get('pageReferences', '').strip()

def has_missing_see_also(term):
	return not term.get('seeAlso')



#==============================================================================#
# STATISTICS FUNCTIONS                                                         #
#==============================================================================#
def get_issue_description(term, check_type):
	if check_type == 'multiple_types':
		gram_type = term.get('grammaticalType', '')
		return f"Multiple grammatical types: {gram_type}"
	
	descriptions = {
		'missing_term': "Missing term field",
		'missing_type': "Missing grammaticalType",
		'missing_definition': "Missing definition in meanings"
	}
	return descriptions.get(check_type, "Unknown issue")


def check_and_flag_critical_issues(terms):
	checks = [
		('missing_term', has_missing_term),
		('missing_type', has_missing_type),
		('multiple_types', has_multiple_types),
		('missing_definition', has_missing_definition)
	]
	
	results = {check_name: [] for check_name, _ in checks}
	flagged_count = 0
	
	for term in terms:
		term_name = term.get('term', '<unnamed>')
		was_flagged = False
		
		for check_name, check_func in checks:
			if check_func(term):
				results[check_name].append(term_name)
				issue_desc = get_issue_description(term, check_name)
				flag_term_for_issue(term, issue_desc)
				was_flagged = True
			
		if was_flagged: flagged_count += 1
	
	return results, flagged_count

def count_info_issues(terms):
	return {
		'missing_synonyms': sum(1 for t in terms if has_missing_synonyms(t)),
		'missing_examples': sum(1 for t in terms if has_missing_examples(t)),
		'missing_references': sum(1 for t in terms if has_missing_references(t)),
		'missing_see_also': sum(1 for t in terms if has_missing_see_also(t))
	}



#==============================================================================#
# DISPLAY FUNCTIONS                                                            #
#==============================================================================#
def display_critical_results(critical_results):
	"""Display critical issues found."""
	print("CRITICAL Issues (auto-flagged):")
	
	issue_labels = {
		'missing_term': "Missing term field",
		'missing_type': "Missing grammaticalType",
		'multiple_types': "Multiple type markers",
		'missing_definition': "Missing definition"
	}
	
	has_any = False
	for issue_type, terms_list in critical_results.items():
		if terms_list:
			label = issue_labels.get(issue_type, issue_type)
			print(f"    {label}: {len(terms_list)} terms")
			has_any = True
	
	if not has_any:
		print("   No critical issues found!")


def display_info_results(info_counts):
	"""Display informational issues."""
	print("\nINFO (not flagged):")
	print(f"    Missing synonyms: {info_counts['missing_synonyms']} terms")
	print(f"    Missing examples: {info_counts['missing_examples']} terms")
	print(f"    Missing references: {info_counts['missing_references']} terms")
	print(f"    Missing seeAlso: {info_counts['missing_see_also']} terms")


def display_results(critical_results, info_counts, flagged_count):
	"""Display all quality check results."""
	print("\n" + "="*60)
	print("Quality Check Results")
	print("="*60 + "\n")
	
	display_critical_results(critical_results)
	display_info_results(info_counts)
	
	print(f"\nTerms auto-flagged: {flagged_count}")
	print()



#==============================================================================#
# MAIN FUNCTION                                                                #
#==============================================================================#
def main():
	"""Run quality check on extracted terms."""
	input_file = Path("data/1_extracted/foundation_raw.json")
	
	print(f"\n📖 Loading: {input_file}")
	terms = load_json_file(input_file)
	print(f"✅ Loaded {len(terms)} terms\n")
	
	print("🔍 Running quality checks...")
	critical_results, flagged_count = check_and_flag_critical_issues(terms)
	info_counts = count_info_issues(terms)
	
	display_results(critical_results, info_counts, flagged_count)
	
	if flagged_count > 0:
		print(f"💾 Saving changes to: {input_file}")
		save_json_file(terms, input_file)
		print("✅ Saved!\n")
	else:
		print("ℹ️  No changes needed\n")

if __name__ == '__main__':
	main()
