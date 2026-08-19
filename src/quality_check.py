#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
from tools.filemanage import load_json_file, save_json_file
from tools.ui import page_break

# TODO: UNUSED
# def has_idiom(term): return 'idiom' in term.get('grammaticalType', '').lower()

def flag_term_for_issue(term, issue_description):
	term["needsReview"] = True
	if "reviewNotes" not in term: term["reviewNotes"] = []
	if "actions"     not in term: term["actions"]     = []
	
	if issue_description not in [note["note"] for note in term["reviewNotes"]]:
		term["reviewNotes"].append({
			"date": datetime.now().isoformat(),
			"note": issue_description
		})
	
	if "flagged" not in [action["type"] for action in term["actions"]]:
		term["actions"].append({
			"type": "flagged",
			"date": datetime.now().isoformat()
		})
	
	return term



def get_issue_description(term, check_type):
	# this string just feels off; is there a situation where grammaticalType
	# would be None here, and should just a blank `: ` really be the solution?
	if check_type == "multiple_types":
		return "Multiple grammatical types: " + term.get("grammaticalType", "")
	
	descriptions = {
		"missing_term":       "Missing term field",
		"missing_type":       "Missing grammaticalType",
		"missing_definition": "Missing definition in meanings"
	}
	
	return descriptions.get(check_type, "Unknown issue")



def check_and_flag_critical_issues(terms):
	checks = {
		"missing_term":       lambda t:    not t.get("term", "").strip(),
		"missing_type":       lambda t:    not t.get("grammaticalType", "").strip(),
		"multiple_types":     lambda t: "," in t.get("grammaticalType", ""),
		"missing_definition": lambda t: (
			not t.get("meanings", [])
			or any(not m.get("definition", "").strip() for m in t["meanings"])
		)
	}
	
	results = {check: [] for check in checks}
	flagged_count = 0
	
	for term in terms:
		was_flagged = False
		
		for check, func in checks.items():
			if func(term):
				results[check].append(term.get("term", "<unnamed>"))
				flag_term_for_issue(term, get_issue_description(term, check))
				was_flagged = True
		
		flagged_count += was_flagged
	
	return results, flagged_count



def count_info_issues(terms):
	issues = {
		"missing_synonyms":   0, "missing_examples": 0,
		"missing_references": 0, "missing_see_also": 0,
	}
	
	for term in terms:
		issues["missing_synonyms"  ] += not any(
			meaning.get("synonyms")
			for meaning in term.get("meanings", [])
		)
		
		issues["missing_examples"  ] += any(
			meaning.get("usageExample", "").strip()
			for meaning in term.get("meanings", [])
		)
		
		issues["missing_references"] += not term.get("pageReferences", "").strip()
		issues["missing_see_also"  ] += not term.get("seeAlso")
	
	return issues



def display_results(info_counts, critical_results, flagged_count):
	print("""
================================================================================
Quality Check Results
================================================================================
""")
	
	issue_labels = {
		"missing_term":       "Missing term field",
		"missing_type":       "Missing grammaticalType",
		"multiple_types":     "Multiple type markers",
		"missing_definition": "Missing definition"
	}
	
	has_any = False
	for issue_type, terms_list in critical_results.items():
		if terms_list:
			if not has_any:
				print("CRITICAL Issues (auto-flagged):")
				has_any = True
			
			print(f"\t{issue_labels.get(issue_type, issue_type)}: {len(terms_list)} terms")
	
	print(f"""
INFO (not flagged):
	Missing synonyms:   {info_counts["missing_synonyms"]} terms
	Missing examples:   {info_counts["missing_examples"]} terms
	Missing references: {info_counts["missing_references"]} terms
	Missing seeAlso:    {info_counts["missing_see_also"]} terms

Terms auto-flagged: {flagged_count}
""")



def main():
	input_file = Path("data/1_extracted/foundation_raw.json")
	
	# TODO: this feels like it should have more explicit error handling
	print(f"> Loading: {input_file}")
	terms = load_json_file(input_file)
	print(f"+ Loaded {len(terms)} terms")
	print()
	print("> Running quality checks...")
	
	critical_results, flagged_count = check_and_flag_critical_issues(terms)
	
	display_results(count_info_issues(terms), critical_results, flagged_count)
	
	if flagged_count > 0:
		print(f"> Saving changes to: {input_file}")
		save_json_file(terms, input_file)
		print("+ Saved!\n")
	else:
		print("- No changes needed\n")

if __name__ == "__main__": main()
