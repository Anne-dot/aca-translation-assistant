#!/usr/bin/env python3

import sys
from pathlib import Path
from datetime import datetime
from tools.filemanage import load_json_file, save_json_file
from tools.ui import page_break



def detect_parentheses_notation(term_data):
	term = term_data.get("term")
	if "(" not in term or ")" not in term: return None
	
	# Pattern: word(s)
	if "(s)" in term:
		base = term.replace("(s)", "").strip()
		plural = base + "s"
		return {
			"category": "split_parentheses",
			"pattern": "(s)",
			"suggestion": [base, plural]
		}
	
	# Pattern: word(ren)
	if "(ren)" in term:
		base = term.replace("(ren)", "").strip()
		plural = base + "ren"
		return {
			"category": "split_parentheses",
			"pattern": "(ren)",
			"suggestion": [base, plural]
		}
	
	# Pattern: word(es)
	if "(es)" in term:
		base = term.replace("(es)", "").strip()
		plural = base + "es"
		return {
			"category": "split_parentheses",
			"pattern": "(es)",
			"suggestion": [base, plural]
		}
	
	return None



def detect_asterisk(term_data):
	term = term_data.get("term")
	if "*" not in term: return None
	
	clean_term = term.replace("*", "").strip()
	return {
		"category": "remove_asterisk",
		"suggestion": {"cleanTerm": clean_term}
	}



def detect_multiple_terms_comma(term_data):
	term = term_data.get("term")
	
	if "(" in term: return None
	if ", " not in term: return None
	
	parts = [p.strip() for p in term.split(",")]
	if len(parts) > 1:
		return {
			"category": "split_multiple_comma",
			"suggestion": parts
		}
	
	return None



def detect_multiple_terms_slash(term_data):
	term = term_data.get("term")
	
	if "/" not in term: return None
	
	parts = [p.strip() for p in term.split("/")]
	if len(parts) > 1:
		return {
			"category": "split_multiple_slash",
			"suggestion": parts
		}
	
	return None



def detect_seealso_issues(term_data):
	# TODO: negative space!
	see_also = term_data.get("seeAlso", [])
	if not see_also: return None
	
	issues = []
	for entry in see_also:
		word_count = len(entry.split())
		if word_count > 4:
			issues.append({
				"entry": entry,
				"reason": f"Too long ({word_count} words)"
			})
	
	if issues:
		return {
			"category": "clean_seealso",
			"suggestion": issues
		}
	
	return None



#==============================================================================#
# DISPLAY FUNCTIONS                                                            #
#==============================================================================#

def display_term_header(term_data, current, total):
	page_break()
	print(f"Term {current}/{total}: {term_data['term']}")
	
	if term_data.get("grammaticalType"):
		print(f"Type: ({term_data['grammaticalType']})")
	
	if term_data.get("meanings"):
		definition = term_data["meanings"][0].get("definition", "")
		if definition:
			short_def = (
				definition[:100] + "..." if len(definition) > 100
				else definition
			)
			print(f"Definition: {short_def}")
	
	page_break()


def display_issue_details(issue):
	print()
	print(f"! Issue detected: {issue['category']}")
	
	if issue["category"] == "split_parentheses":
		print(f"""
	Pattern: {issue["pattern"]}
	Suggestion: Split into {len(issue["suggestion"])} terms
""")
		for i, term in enumerate(issue['suggestion'], 1):
			print(f"\t\t{i}. \"{term}\"")
	
	elif issue["category"] == "remove_asterisk":
		print(f"""
	Suggestion: Remove asterisk
		Clean term: "{issue["suggestion"]["cleanTerm"]}"
""")
	
	elif issue["category"] in ["split_multiple_comma", "split_multiple_slash"]:
		sep = "," if issue["category"] == "split_multiple_comma" else "/"
		print(f"""
	Separator: "{sep}"
	Suggestion: Split into {len(issue["suggestion"])} terms:""")
		for i, term in enumerate(issue["suggestion"], 1):
			print(f"\t\t{i}. \"{term}\"")
	
	elif issue["category"] == "clean_seealso":
		print(f"\tseeAlso field has suspicious entries:")
		for item in issue["suggestion"]:
			print(f"\t\t\"{item['entry']}\" - {item['reason']}")



#==============================================================================#
# USER INTERACTION                                                             #
#==============================================================================#

def prompt_user_action():
	print("""
What to do?
	[1] Accept suggestion
	[2] Edit manually
	[3] Skip (review later)
	[4] Mark as correct (no action)
	
""")
	
	valid_choices = ["1", "2", "3", "4"]
	while True:
		choice = input("> ").strip()
		if choice in valid_choices: return choice
		print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")



#==============================================================================#
# MANUAL EDIT HANDLERS                                                         #
#==============================================================================#

def handle_manual_edit(issue):
	print()
	print("= Enter your changes:")
	
	if issue["category"] in [
		"split_parentheses", "split_multiple_comma", "split_multiple_slash"
	]:
		print("Enter terms (comma separated):")
		user_input = input("> ").strip()
		terms = [t.strip() for t in user_input.split(",")]
		return {
			"type": issue["category"],
			"data": terms
		}
		
	elif issue["category"] == "remove_asterisk":
		print("Enter clean term:")
		clean = input("> ").strip()
		print("Enter note (optional, press Enter to skip):")
		note = input("> ").strip()
		return {
			"type": issue["category"],
			"data": {
				"cleanTerm": clean,
				"note": note if note else None
			}
		}
		
	elif issue["category"] == "clean_seealso":
		print("Enter corrected seeAlso entries (comma separated):")
		user_input = input("> ").strip()
		terms = [t.strip() for t in user_input.split(",")]
		return {
			"type": issue["category"],
			"data": terms
		}
	
	return None


#==============================================================================#
# TERM PROCESSING                                                              #
#==============================================================================#

def collect_all_issues(term_data):
	issues = []
	
	for check in [
		detect_parentheses_notation, detect_asterisk, detect_seealso_issues,
		detect_multiple_terms_comma, detect_multiple_terms_slash,
	]:
		result = check(term_data)
		if result: issues.append(result)
	
	return issues



def save_normalization_action(term_data, action_type, action_data):
	term_data["normalizationAction"] = {
		"type": action_type,
		"data": action_data
	}
	term_data["reviewedAt"] = datetime.now().isoformat()
	term_data["needsReview"] = False


def process_single_issue(term_data, issue, stats):
	display_issue_details(issue)
	choice = prompt_user_action()
	
	if choice == "1":  # Accept suggestion
		save_normalization_action(
			term_data, issue["category"], issue["suggestion"]
		)
		stats["accepted"] += 1
		print("+ Suggestion accepted")
		return True
	
	elif choice == "2":  # Edit manually
		action = handle_manual_edit(issue)
		if action:
			save_normalization_action(
				term_data, action["type"], action["data"]
			)
			stats["edited"] += 1
			print("+ Manual edit saved")
			return True
	
	elif choice == "3":  # Skip
		stats["skipped"] += 1
		print("> Skipped")
		return False
	
	elif choice == "4":  # Mark as correct
		term_data["reviewedAt"] = datetime.now().isoformat()
		term_data["needsReview"] = False
		stats["no_action"] += 1
		print("+ Marked as correct")
		return True
	
	return False


def process_term(term_data, stats):
	issues = collect_all_issues(term_data)
	
	if not issues: return False
	
	modified = False
	for issue in issues:
		if process_single_issue(term_data, issue, stats):
			modified = True
	
	return modified


#==============================================================================#
# STATISTICS                                                                   #
#==============================================================================#

def display_final_statistics(stats):
	print()
	page_break()
	print("+ Review complete!")
	page_break()
	print(f"""
Statistics:
	Total reviewed: {stats["total_reviewed"]}
	+ Accepted:  {stats["accepted"]}
	/ Edited:    {stats["edited"]}
	- Skipped:   {stats["skipped"]}
	. No action: {stats["no_action"]}

""")



#==============================================================================#
# MAIN FUNCTION                                                                #
#==============================================================================#

def main():
	# TODO: negative space!
	input_file = Path("data/1_extracted/foundation_raw.json")
	
	sys.stdin.reconfigure(encoding = "utf-8")
	
	print()
	print("> Term Normalization Review")
	page_break()
	print()
	print(f"> Loading: {input_file}")
	
	terms = load_json_file(input_file)
	print(f"+ Loaded {len(terms)} terms\n")
	
	stats = {
		"accepted": 0, "edited": 0, "skipped": 0, "no_action": 0,
		"total_reviewed": 0
	}
	
	for i, term_data in enumerate(terms, 1):
		print()
		print(f"- Progress: {i}/{len(terms)}")
		
		display_term_header(term_data, i, len(terms))
		
		had_issues = process_term(term_data, stats)
		
		if had_issues:
			stats["total_reviewed"] += 1
			
			print("> Saving...", end=" ", flush=True)
			save_json_file(terms, input_file)
			print("+ Saved!")
	
	display_final_statistics(stats)
	
	print(f"> All changes saved to: {input_file}\n")



if __name__ == "__main__": main()
