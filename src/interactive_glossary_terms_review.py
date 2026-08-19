#!/usr/bin/env python3
import sys
import os
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from functools import reduce

from tools.filemanage import load_json_file, save_json_file
from tools.normalization_detection import collect_normalization_issues
from tools.ui import page_break



#==============================================================================#
# STATISTICS                                                                   #
#==============================================================================#
def count_terms_by_review_status(terms):
	total = len(terms)
	flagged = reviewed = multiple_meanings = 0
	
	for t in terms:
		flagged           += t.get("needsReview", False)
		reviewed          += t.get("reviewedAt") is not None
		multiple_meanings += len(t.get("meanings", [])) > 1
	
	return {
		"total":             total,
		"flagged":           flagged,
		"reviewed":          reviewed,
		"not_reviewed":      total - reviewed,
		"remaining_flagged": flagged - reviewed,
		"multiple_meanings": multiple_meanings,
		"actions":           count_actions_by_type(terms)
	}

def count_actions_by_type(terms):
	counts = { "accepted": 0, "merged": 0, "edited": 0, "flagged": 0 }
	
	for term in terms:
		actions = term.get("actions", [])
		if actions:
			last_action = actions[-1]["type"]
			counts[last_action] += (last_action in counts)
	
	return counts



def display_statistics(stats):
	def percent(count, total):
		return 0.0 if total == 0 else round(count / total * 100, 1)
	
	total        = stats["total"]
	multiple     = percent(stats["multiple_meanings"], total)
	flagged      = percent(stats["flagged"],           total)
	reviewed     = percent(stats["reviewed"],          total)
	not_reviewed = percent(stats["not_reviewed"],      total)
	
	print(f"""
| Statistics:
	Total terms: {total}
	Multiple meanings: {stats["multiple_meanings"]} ({multiple}%)
	
> Review Status:
	Flagged for review: {stats["flagged"]} ({flagged}%)
			  Reviewed: {stats["reviewed"]} ({reviewed}%)
		  Not reviewed: {stats["not_reviewed"]} ({not_reviewed}%)
	
> Actions (of {total} total):""")
	
	actions = stats["actions"]
	for action_type, count in actions.items():
		print(
			f"\t{action_type.capitalize()}: {count} ({percent(count, total)}%)"
		)
	
	print()



#==============================================================================#
# TERM DISPLAY                                                                 #
#==============================================================================#
def display_complete_term_info(term, title = None, index = None, total = None):
	term_name = ""
	if index and total: term_name  = f"{index}/{total}" + (bool(title) * ": ")
	if title:           term_name += title
	if not term_name:   term_name  = "info"
	
	print(f"""
================================================================================
Term {term_name}:
================================================================================
Term: {term["term"]}
Type: {term.get("grammaticalType", "N/A")}
Note: {term.get("termNote", "none")}

see also: {", ".join(term.get("seeAlso", ["N/A"]))}
""")
	
	issues = collect_normalization_issues(term)
	if issues:
		print()
		print(f"! Normalization issues detected:")
		for issue in issues: print(f"\t- {get_issue_description_short(issue)}")
	
	if term.get("normalizationAction"):
		action = term["normalizationAction"]
		print()
		print(f"<- normalizationAction: {action['type']}")
		match action["type"]:
			case "split_multiple_slash" | "split_multiple_comma":
				print(f"\t-> Split into: {', '.join(action['data'])}")
			case "clean_seealso":
				if action["data"] and isinstance(action["data"][0], dict):
					entries = [item["entry"] for item in action["data"]]
				else:
					entries = action["data"]
				print(f"\t-> Clean seeAlso entries: {', '.join(entries)}")
			case "remove_parentheses":
				print(f"\t-> Split: {', '.join(action['data'])}")
			case "remove_asterisk":
				print(f"\t-> Clean term: {action['data']['cleanTerm']}")
	
	if term.get("reviewNotes"):
		print()
		print(f"| Review notes:")
		for i, note in enumerate(term["reviewNotes"], 1):
			if type(note) is dict:
				print(f"\t{i}. {note['note']} ({note['date'][:10]})")
			else:
				print(f"\t{i}. {note}")
	
	meanings = term.get("meanings", [])
	if meanings:
		print()
		if len(meanings) == 1:
			meaning = meanings[0]
			print("Definition:")
			print(f"\t{meaning.get('definition', 'N/A')}")
			
			if meaning.get("synonyms"):
				print()
				print(f"Synonyms:")
				print(f"\t{', '.join(meaning['synonyms'])}")
			
			if meaning.get("usageExample"):
				print()
				print(f"Example:")
				print(f"\t{meaning['usageExample']}")
		else:
			for i, meaning in enumerate(meanings, 1):
				print(f"Meaning {i}:")
				print(f"\tDefinition: {meaning.get('definition', 'N/A')}")
				
				if meaning.get("synonyms"):
					print(f"\tSynonyms: {', '.join(meaning['synonyms'])}")
				
				if meaning.get("usageExample"):
					print(f"\tExample: {meaning['usageExample']}")
				
				if i < len(meanings): print()
	
	if term.get("pageReferences"):
		print()
		print(f"Page References:")
		# Format page references with indentation
		refs = term["pageReferences"]
		for line in refs.split("\n"):
			if line.strip(): print(f"\t{line.strip()}")
	
	print(page_break())



#==============================================================================#
# USER INTERACTION                                                             #
#==============================================================================#
def get_user_choice(prompt, valid_choices):
	while True:
		choice = input(prompt).strip().lower()
		if choice in valid_choices: return choice
		print(f"""Invalid choice.
Please choose from: {", ".join(valid_choices)}
""")



#==============================================================================#
# NORMALIZATION HANDLING - Issue #25                                           #
#==============================================================================#
def get_issue_description_short(issue):
	category = issue["category"]
	
	options = {
		"split_parentheses":   f"Term contains parentheses: {issue['pattern']}",
		"remove_asterisk":      "Term contains asterisk marker",
		"split_multiple_comma": "Term contains comma (multiple terms)",
		"split_multiple_slash": "Term contains slash (multiple terms)",
	}
	
	if category == "clean_seealso":
		entries = [item["entry"] for item in issue["suggestion"]]
		return f"seeAlso contains term variants: {', '.join(entries[:2])}"
	elif category in options:
		return options[category]
	else:
		return f"Unknown issue: {category}"



def display_normalization_issue(issue):
	print("""
================================================================================
! NORMALIZATION ISSUE DETECTED !
================================================================================
Category: {issue["category"]}
""")
	
	match issue["category"]:
		case "split_parentheses":
			print(f"Pattern: {issue['pattern']}")
			print(f"Suggestion: Split into {len(issue['suggestion'])} terms")
			for i, term in enumerate(issue["suggestion"], 1):
				print(f"   {i}. \"{term}\"")
			
		case "remove_asterisk":
			print(f"Suggestion: Remove asterisk")
			print(f"   Clean term: \"{issue['suggestion']['cleanTerm']}\"")
			
		case "split_multiple_comma" | "split_multiple_slash":
			sep = "," if issue["category"] == "split_multiple_comma" else "/"
			print(f"Separator: '{sep}'")
			print(f"Suggestion: Split into {len(issue['suggestion'])} terms")
			for i, term in enumerate(issue["suggestion"], 1):
				print(f"   {i}. \"{term}\"")
			
		case "clean_seealso":
			print(f"seeAlso field has suspicious entries:")
			for item in issue["suggestion"]:
				print(f"   \"{item['entry']}\" - {item['reason']}")
	
	print(page_break())



def handle_normalization_edit(issue):
	print()
	print("| Enter your changes:")
	
	match issue["category"]:
		case "split_parentheses" | "split_multiple_comma" \
		| "split_multiple_slash":
			print("Enter terms (comma separated):")
			user_input = input("> ").strip()
			terms = [t.strip() for t in user_input.split(",")]
			return {
				"type": issue["category"],
				"data": terms
			}
			
		case "remove_asterisk":
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
			
		case "clean_seealso":
			print("Enter corrected seeAlso entries (comma separated):")
			user_input = input("> ").strip()
			terms = [t.strip() for t in user_input.split(",")]
			return {
				"type": issue["category"],
				"data": terms
			}
	
	return None



def apply_normalization_action(term, action):
	term["normalizationAction"] = action
	print()
	print(f"+ normalizationAction added: {action['type']}")



def display_updated_term_info(term):
	if "normalizationAction" in term:
		action = term["normalizationAction"]
		print()
		print(page_break())
		print(f"normalizationAction: {action['type']}")
	
		if isinstance(action["data"], list):
			if action["data"] and isinstance(action["data"][0], dict):
				entries = [item["entry"] for item in action["data"]]
				print(f"\t-> {len(entries)} entries to clean: {', '.join(entries)}")
			else:
				print(f"\t-> {len(action['data'])} terms: {', '.join(action['data'])}")
		elif isinstance(action["data"], dict):
			if "cleanTerm" in action["data"]:
				print(f"\t-> Clean term: {action['data']['cleanTerm']}")
		
		print(page_break())
		print()
	
	display_complete_term_info(term, title = "UPDATED TERM INFO")



def check_and_handle_normalization_issues(term):
	issues = collect_normalization_issues(term)
	
	if not issues: return False
	
	existing_action = term.get("normalizationAction")
	if existing_action:
		issues = [
			issue for issue in issues
			if issue["category"] != existing_action["type"]
		]
	
	if not issues: return False
	
	for issue in issues:
		display_normalization_issue(issue)
		
		print("""Normalization actions:
	[1] Accept suggestion
	[2] Edit manually
	[3] Continue with normal review (ignore)
	[4] Skip term
""")
		
		match get_user_choice("> ", ["1", "2", "3", "4"]):
			case "1":
				action = {
					"type": issue["category"],
					"data": issue["suggestion"]
				}
				apply_normalization_action(term, action)
				
			case "2":
				action = handle_normalization_edit(issue)
				if action: apply_normalization_action(term, action)
				
			case "3":
				print("> Skipping normalization, continuing to review...")
				return False
				
			case "4":
				print("> Term skipped")
				return True
	
	if "normalizationAction" in term: display_updated_term_info(term)
	
	return False



#==============================================================================#
# REVIEW ACTIONS                                                               #
#==============================================================================#
def save_with_feedback(terms, file_path):
	try:
		print("> Saving...", flush = True)
		save_json_file(terms, file_path)
		print("+ Saved!")
		return True
	except Exception as e:
		print(f"- Save failed: {e}")
		return False



def mark_term_as_reviewed(term, action_type):
	term["reviewedAt"] = datetime.now().isoformat()
	
	if term.get("reviewNotes"): ask_for_review_notes_cleanup(term)
	
	# clear flag only if no notes remain
	if not term.get("reviewNotes"): term["needsReview"] = False
	
	if "actions" not in term: term["actions"] = []
	
	term["actions"].append({
		"type": action_type,
		"date": datetime.now().isoformat()
	})
	
	return term



def accept_term(term):
	print("+ Accepted!")
	print()
	return mark_term_as_reviewed(term, "accepted")



def flag_term_for_review(term):
	note = input("Reason for flagging (optional): ").strip()
	
	term["needsReview"] = True
	term["reviewedAt" ] = datetime.now().isoformat()
	
	if note:
		if "reviewNotes" not in term: term["reviewNotes"] = []
		
		term["reviewNotes"].append({
			"date": datetime.now().isoformat(),
			"note": note
		})
	
	if "actions" not in term: term["actions"] = []
	
	term["actions"].append({
		"type": "flagged",
		"date": datetime.now().isoformat()
	})
	
	print("!Flagged for review!")
	print()
	return term



def mark_waiting_for_update(term):
	term["waitingForUpdate"]   = True
	term["waitingForUpdateAt"] = datetime.now().isoformat()
	term["reviewedAt"]         = datetime.now().isoformat()
	term["needsReview"]        = False
	
	note = input("Reason for waiting (optional): ").strip()
	
	if note:
		if "reviewNotes" not in term: term["reviewNotes"] = []
		
		term["reviewNotes"].append({
			"date": datetime.now().isoformat(),
			"note": f"Waiting for update: {note}"
		})
	
	if "actions" not in term: term["actions"] = []
	
	term["actions"].append({
		"type": "waiting_for_update",
		"date": datetime.now().isoformat()
	})
	
	print("!Marked as waiting for script update!")
	print()
	return term



#==============================================================================#
# EDIT FUNCTIONALITY - FIELD OPERATIONS                                        #
#==============================================================================#
def edit_single_field(field_name, current_value):
	is_list = type(current_value) is list
	
	display_value = ", ".join(current_value) if is_list \
		else current_value if current_value \
		else "N/A"
	
	print(f"""
Current {field_name}:
	{display_value}

Options:
	[k] Keep current value
	[e] Enter new value
	[d] Delete (set to empty)
""")
	
	match get_user_choice("> ", ["k", "e", "d"]):
		case "k":
			return current_value
		case "e":
			if is_list:
				new_value = input("Enter comma-separated values: ").strip()
				if not new_value: return []
				
				return [
					item.strip() for item in new_value.split(",")
				]
			else:
				return input("Enter new value: ").strip()
		case "d":
			return [] if is_list else ""



#==============================================================================#
# EDIT FUNCTIONALITY - MEANING OPERATIONS                                      #
#==============================================================================#
def edit_single_meaning(meaning):
	print()
	print("| Editing meaning fields...")
	print()
	
	new_meaning = {}
	
	for field in ["definition", "synonyms", "usageExample"]:
		new_meaning[field] = edit_single_field(
			field, meaning.get(field, [] if field == "synonyms" else "")
		)
	
	return new_meaning



def select_meaning_to_edit(meanings):
	if len(meanings) == 1: return 0
	
	print()
	print("Which meaning to edit? (1 ... {i+1})")
	print("[0] to cancel")
	
	choice = int(get_user_choice(
		"> ", [str(i) for i in range(len(meanings) + 1)]
	))
	
	return none if choice == 0 else choice - 1



def edit_text_in_editor(current_text, field_name = "text"):
	with tempfile.NamedTemporaryFile(
		mode = "w", suffix = ".txt", delete = False, encoding = "utf-8"
	) as file:
		file.write(f"""
# Muuda {field_name} allpool.
# `#-ga` algavaid read eemaldatakse.
# Salvesta ja sulge redaktor kui valmis.
{current_text}""")
		temp_path = file.name
	
	# TODO: shouldn't this say something if the file / subprocess fails?
	# it's in a try block, after all.
	try: 
		editor = os.environ.get("EDITOR", "nano")
		subprocess.call([editor, temp_path])
		
		with open(temp_path, "r", encoding = "utf-8") as file:
			lines = file.readlines()
		
		edited_text = "".join([
			line for line in lines if not line.strip().startswith("#")
		]).strip()
		
		return edited_text
	
	finally:
		if os.path.exists(temp_path):
			os.unlink(temp_path)



def format_synonym_as_sentence(text):
	if text == "": return text
	if not text.endswith("."): text += "."
	return text.capitalize()



def handle_synonym_to_definition(term):
	has_synonym_note = False
	if term.get("reviewNotes"):
		for note in term["reviewNotes"]:
			note_text = note["note"] if isinstance(note, dict) else note
			if "synonym" in note_text.lower():
				has_synonym_note = True
				break
	
	if not has_synonym_note: return False
	
	meanings = term.get("meanings", [])
	if not meanings: return False
	
	meaning = meanings[0]
	synonyms = meaning.get("synonyms", [])
	if not synonyms: return False
	
	# Show current state
	print(page_break())
	print("* SYNONYM -> DEFINITION")
	print(page_break())
	print()
	
	print("Term has been flagged for synonyms issue.")
	print(f"\nCurrent definition:")
	print(f"\t{meaning.get('definition', 'N/A')}")
	print()
	
	print(f"Current synonyms:")
	for i, syn in enumerate(synonyms, 1): print(f"\t{i}. {syn}")
	print()
	
	print("""Options:
	[y] Yes - Move synonyms to definition
	[n] No - Skip for now
	[w] Waiting - Mark as waiting for script update
""")
	choice = get_user_choice("> ", ["y", "n", "w"])
	
	if choice == "n":
		print("> Skipped synonym move\n")
		return False
	elif choice == "w":
		print("X Marking term as waiting for script update...\n")
		mark_waiting_for_update(term)
		return False
	
	current_definition = meaning.get("definition", "")
	
	formatted_synonyms = [format_synonym_as_sentence(syn) for syn in synonyms]
	new_definition = current_definition + "\n\n" + "\n\n".join(formatted_synonyms)
	
	print()
	print("Preview (will open in editor):")
	print(f"\t{new_definition[:150]}...")
	print()
	
	final_definition = edit_text_in_editor(new_definition, "definitsioon")
	
	meaning["definition"] = final_definition
	meaning["synonyms"] = []
	meanings[0] = meaning
	term["meanings"] = meanings
	
	print("+ Synonyms moved to definition!")
	
	display_complete_term_info(term, title = "UPDATED TERM INFO")
	
	return True



def edit_definition(term):
	meanings = term.get("meanings", [])
	
	if not meanings:
		print("- No meanings found")
		print()
		return term
	
	if len(meanings) > 1:
		meaning_index = select_meaning_to_edit(meanings)
		if meaning_index is None:
			print("- Edit cancelled")
			print()
			return term
	else:
		meaning_index = 0
	
	meaning = meanings[meaning_index]
	current_definition = meaning.get("definition", "")
	
	print(f"""| Opening definition in text editor...

Current definition:
	{current_definition}
""")
	
	edited_definition = edit_text_in_editor(current_definition, "definitsioon")
	
	if edited_definition == current_definition:
		print("! No changes made!")
		print()
		return term
	
	meaning["definition"]   = edited_definition
	meanings[meaning_index] = meaning
	term["meanings"]        = meanings
	
	print("+ Definition updated!")
	
	display_complete_term_info(term, title = "UPDATED TERM INFO")
	
	if term.get("reviewNotes"): ask_for_review_notes_cleanup(term)
	
	return term



def edit_term_meanings(term):
	meanings = term.get("meanings", [])
	
	meaning_index = select_meaning_to_edit(meanings)
	
	if meaning_index is None:
		print("- Edit cancelled")
		print()
		return term
	
	edited_meaning = edit_single_meaning(meanings[meaning_index])
	meanings[meaning_index] = edited_meaning
	
	term["meanings"] = meanings
	print("+ Meaning edited!")
	print()
	
	return mark_term_as_reviewed(term, "edited")



def split_grammatical_type(grammatical_type):
	if not grammatical_type or "," not in grammatical_type:
		return (grammatical_type, None)
	
	parts = [p.strip() for p in grammatical_type.split(",", 1)]
	return (parts[0], parts[1] if len(parts) > 1 else None)



def edit_term_fields(term):
	print()
	print("| Editing term fields...")
	print()
	
	current_type = term.get("grammaticalType", "")
	
	if not current_type:
		print("! grammaticalType is missing")
		print()
		
		new_type = edit_single_field("grammaticalType", "")
		
		pos, qualifier = split_grammatical_type(new_type)
		term["grammaticalType"] = pos
		
		if qualifier:
			existing_note = term.get("termNote", "")
			if existing_note:
				term["termNote"] = f"{existing_note}; {qualifier}"
			else:
				term["termNote"] = qualifier
			print()
			print(f"+ Split applied:")
			print(f"\tgrammaticalType: {pos}")
			print(f"\ttermNote: {qualifier}")
		
		print()
		if input("Edit seeAlso too? [y/N]: ").strip().lower() == "y":
			term["seeAlso"] = edit_single_field(
				"seeAlso", term.get("seeAlso", [])
			)
		
	else:
		print("""What to edit?
	[1] grammaticalType
	[2] seeAlso
	[3] Both
	[0] Cancel
""")
		
		choice = get_user_choice("> ", ["1", "2", "3", "0"])
		
		if choice == "0":
			print("- Edit cancelled")
			print()
			return term
		
		if choice in ["1", "3"]:
			pos, qualifier = split_grammatical_type(current_type)
			
			if qualifier:
				print()
				print(f"[i] Current value will be split:")
				print(f"\tPart of speech: {pos}")
				print(f"\tQualifier (→ termNote): {qualifier}\n")
				
				apply_split = input("Apply split? [Y/n]: ").strip().lower()
				
				if apply_split in ["", "y", "yes"]:
					term["grammaticalType"] = pos
					existing_note = term.get("termNote", "")
					if existing_note:
						term["termNote"] = f"{existing_note}; {qualifier}"
					else:
						term["termNote"] = qualifier
					print()
					print(f"+ Split applied:")
					print(f"\tgrammaticalType: {pos}")
					print(f"\ttermNote: {qualifier}")
				else:
					new_type = edit_single_field(
						"grammaticalType",
						current_type,
						is_list = False
					)
					pos, qualifier = split_grammatical_type(new_type)
					term["grammaticalType"] = pos
					if qualifier:
						existing_note = term.get("termNote", "")
						if existing_note:
							term["termNote"] = f"{existing_note}; {qualifier}"
						else:
							term["termNote"] = qualifier
						print()
						print(f"+ Split applied:")
						print(f"\tgrammaticalType: {pos}")
						print(f"\ttermNote: {qualifier}")
			else:
				new_type = edit_single_field(
					"grammaticalType",
					current_type,
					is_list = False
				)
				term["grammaticalType"] = new_type
		
		if choice in ["2", "3"]:
			term["seeAlso"] = edit_single_field(
				"seeAlso",
				term.get("seeAlso", []),
				is_list = True
			)
	
	print("+ Term fields updated!")
	
	display_complete_term_info(term, title = "UPDATED TERM INFO")
	
	if term.get("reviewNotes"): ask_for_review_notes_cleanup(term)
	
	return term



def edit_review_notes(term):
	if not term.get("reviewNotes"):
		print("! No review notes to edit!")
		print()
		return term
	
	ask_for_review_notes_cleanup(term)
	
	return term



def ask_for_review_notes_cleanup(term):
	display_complete_term_info(term, title = "CURRENT TERM STATE")
	
	notes = term["reviewNotes"]
	print("Review notes:")
	for i, note in enumerate(notes, 1): print(f"\t{i}. {note}")
	print()
	
	print("""Clear review notes?
	[y] Clear all notes
	[n] Keep all notes
	[i] Interactive (choose per note)
""")
	
	match get_user_choice("> ", ["y", "n", "i"]):
		case "y":
			del term["reviewNotes"]
			print("+ All review notes cleared")
			print()
			display_complete_term_info(term, title = "UPDATED TERM INFO")
			
		case "i":
			notes = term["reviewNotes"]
			remaining_notes = []
			
			deleted_count = 0
			for i, note in enumerate(notes, 1):
				if isinstance(note, dict):
					note_text = f"{note['note']} ({note['date'][:10]})"
				else:
					note_text = note
				
				print()
				delete = input(f"Delete note #{i}: \"{note_text}\"? [y/N]: ") \
					.strip().lower()
				
				if delete == "y":
					deleted_count += 1
					print("+ Deleted")
				else:
					remaining_notes.append(note)
					print("> Kept")
			
			# Update term
			print()
			if remaining_notes:
				term["reviewNotes"] = remaining_notes
				print(f"+ {deleted_count} note(s) deleted, {len(remaining_notes)} kept")
			else:
				del term["reviewNotes"]
				print(f"+ All {deleted_count} review note(s) deleted")
			
			print()
			display_complete_term_info(term, title = "UPDATED TERM INFO")
			
		case "n":
			print("+ All review notes kept\n")
			display_complete_term_info(term, title = "UPDATED TERM INFO")



#==============================================================================#
# MERGE FUNCTIONALITY                                                          #
#==============================================================================#
def combine_list_fields(list1, list2):
	combined = list1 + list2
	seen = set()
	result = []
	for item in combined:
		if item not in seen:
			seen.add(item)
			result.append(item)
	return result



def merge_two_meanings(meaning1, meaning2):
	merged = {
		"definition": (
			meaning1.get("definition", "") + " " +
			meaning2.get("definition", "")
		).strip(),
		
		"synonyms": combine_list_fields(
			meaning1.get("synonyms", []),
			meaning2.get("synonyms", [])
		),
		
		"usageExample": (
			meaning1.get("usageExample", "") + " " +
			meaning2.get("usageExample", "")
		).strip()
	}
	return merged



def merge_term_meanings(term):
	meanings = term.get("meanings", [])
	
	if len(meanings) == 1:
		print("!! Term already has single meaning!")
		print()
		return term
	
	print()
	print(f"!! This will merge {len(meanings)} meanings into 1.")
	confirm = get_user_choice("Continue? [y/n]: ", ["y", "n"])
	
	if confirm == "n":
		print("- Merge cancelled")
		print()
		return term
	
	merged = reduce(merge_two_meanings, meanings)
	
	print("""
================================================================================
MERGE PREVIEW
================================================================================

Merged Definition:
	{merged["definition"]}

Merged Synonyms:
	{', '.join(merged['synonyms']) if merged["synonyms"] else "(none)"}

Merged Usage Example:
	{merged["usageExample"]}
	
================================================================================
""")
	
	
	print("""Would you like to edit the merged result?
	[y] Yes - Edit fields
	[n] No  - Accept as is
""")
	
	final_meaning = merged
	if get_user_choice("> ", ["y", "n"]) == "y":
		final_meaning = edit_single_meaning(merged)
	
	print("""
================================================================================
FINAL RESULT
================================================================================
""")
	# TODO: ...uh oh. god damn you, ai hallucinations.
	# i feared i had accidentally "optimised" this function out,
	# ...but it seems like this function never existed, as far as referencing
	# git blame has to say. ...what now?
	# display_single_meaning(final_meaning)
	
	if get_user_choice("Save this merged meaning? [y/n]: ", ["y", "n"]) == "n":
		print("- Merge cancelled")
		print()
		return term
	
	term["meanings"] = [final_meaning]
	print("+ Meanings merged!")
	print()
	
	return mark_term_as_reviewed(term, "merged")



#==============================================================================#
# FILTERING                                                                    #
#==============================================================================#
def filter_terms_for_review(terms, review_mode):
	if review_mode == "5":
		return terms
	
	# TODO: optimise this to select and store the used function once
	
	def not_waiting(t): return not t["waitingForUpdate"]
	
	check = {
		"1": lambda t : t["needsReview"]                         and not_waiting(t),
		"2": lambda t : t["reviewedAt"] is None                  and not_waiting(t),
		"3": lambda t : t["reviewedAt"] and not t["needsReview"] and not_waiting(t),
		"4": lambda t : t["reviewedAt"] and t["needsReview"]     and not_waiting(t),
		"7": lambda t : t["waitingForUpdate"],
		"8": lambda t :
			t["reviewedAt"] is None and not t["needsReview"]     and not_waiting(t),
	}
	
	if review_mode in check:
		return [t for t in terms if check[review_mode](t)]
	
	return []



#==============================================================================#
# MAIN FUNCTION                                                                #
#==============================================================================#
def display_review_menu(terms):
	total        = len(terms)
	waiting      = sum(1 for t in terms if     t.get("waitingForUpdate", False))
	active_terms =    [t for t in terms if not t.get("waitingForUpdate", False)]
	
	flagged = not_reviewed = reviewed_ok = reviewed_flagged = unflagged = 0
	for t in active_terms:
		needs_review = t.get("needsReview", False)
		is_reviewed  = t.get("reviewedAt") is not None
		
		flagged          += needs_review
		not_reviewed     += not is_reviewed
		reviewed_ok      += is_reviewed and not needs_review
		reviewed_flagged += is_reviewed and needs_review
		unflagged        += not is_reviewed and not needs_review
	
	print(page_break())
	print("Foundation Glossary Review")
	print(page_break())
	print(f"""Options:
	[1] Flagged ({flagged} terms)
	[2] Not reviewed ({not_reviewed} terms)
	[3] Reviewed - OK ({reviewed_ok} terms)
	[4] Reviewed - Flagged ({reviewed_flagged} terms)
	[5] All terms ({total} terms)
	[6] Show statistics and exit
	[7] Waiting for update ({waiting} terms)
	[8] Unflagged - not reviewed yet ({unflagged} terms)
	[q] Quit
""")

def main():
	input_file = Path("~/data/1_extracted/foundation_raw.json")
	
	sys.stdin.reconfigure(encoding = "utf-8")
	print()
	print(f"> Loading: {input_file}")
	terms = load_json_file(input_file)
	print(f") Loaded {len(terms)} terms")
	print()
	
	flagged_count = 0
	for term in terms:
		if not term.get("needsReview", False):
			issues = collect_normalization_issues(term)
			if issues:
				term["needsReview"] = True
				flagged_count += 1
	
	if flagged_count > 0:
		save_json_file(terms, input_file)
		print(f"> Auto-flagged {flagged_count} terms with normalization issues")
		print()
	
	display_review_menu(terms)
	choice = get_user_choice(
		"> ", ["1", "2", "3", "4", "5", "6", "7", "8", "q"]
	)
	
	if choice == "q":
		print()
		print("Goodbye!")
		print()
		return
	
	if choice == "6":
		stats = count_terms_by_review_status(terms)
		display_statistics(stats)
		return
	
	terms_to_review = filter_terms_for_review(terms, choice)
	
	if not terms_to_review:
		print("!! No terms to review!")
		print()
		return
	
	print()
	print(f"> Reviewing {len(terms_to_review)} terms...")
	print()
	
	# Review loop
	modified = False
	previous_term_name = None
	
	for i, term in enumerate(terms_to_review, 1):
		if previous_term_name:
			print(f"""
================================================================================
< EXITING TERM: {previous_term_name}

> NEXT TERM: {i}/{len(terms_to_review)}
================================================================================
""")
		
		filter_type = [
			"NOT REVIEWED",  "FLAGGED",
			"REVIEWED - OK", "REVIEWED - FLAGGED"
		][("needsReview" in term)*1 + ("reviewedAt" in term)*2]
		
		display_complete_term_info(
			term,      title = filter_type,
			index = i, total = len(terms_to_review)
		)
		
		previous_term_name = term["term"]
		
		if check_and_handle_normalization_issues(term): continue
		
		if (
			handle_synonym_to_definition(term)
			and save_with_feedback(terms, input_file)
		): modified = True
		
		
		
		ACTION_FUNCTIONS = {
			"a": accept_term,          "w": mark_waiting_for_update,
			"f": flag_term_for_review, "m": merge_term_meanings,
			"e": edit_term_meanings,   "d": edit_definition,
			"t": edit_term_fields,     "n": edit_review_notes,
		}
		
		while True:
			print("""Actions:
	[a] Accept - Entry is correct
	[d] Edit definition - Quick definition edit
	[e] Edit - Modify meanings
	[t] Edit term fields - grammaticalType, seeAlso
	[n] Edit review notes
	[m] Merge - Should be single meaning
	[f] Flag - Mark for review
	[w] Waiting for update - Needs script enhancement
	[s] Skip - Review later
	[q] Quit review
""")
			
			action = get_user_choice(
				"> ", ["a", "d", "e", "t", "n", "m", "f", "w", "s", "q"]
			)
			
			function = ACTION_FUNCTIONS.get(action)
			if function:
				function(term)
				if save_with_feedback(terms, input_file): modified = True
				if action not in {"d", "e", "f", "t", "n"}: break
			elif action == "s": # skip
				print("> Skipped")
				print()
				break
			elif action == "q": # quit
				print()
				print("|| Review paused")
				print()
				break
		
		# exit outer loop aswell on [q]uit
		if action == "q": break
	
	print()
	print(
		f"+ All changes saved to `{input_file}`." if modified \
		else "- No changes made."
	)
	print()


if __name__ == "__main__": main()
