#!/usr/bin/env python3
from pathlib import Path
from tools.filemanage import load_json_file, save_json_file

def migrate_reviewed_terms(terms):
	migrated_count = 0
	
	for term in terms:
		if "actions" in term or not term.get("reviewedAt"): continue
		
		action_type = "merged" if len(term.get("meanings", [])) == 1 \
			else "accepted"
		
		term["actions"] = [{"type": action_type, "date": term["reviewedAt"]}]
		
		migrated_count += 1
		print(f"+ {term['term']}: added '{action_type}' action")
	
	return migrated_count



def main():
	# TODO: error checking!!
	input_file = Path("data/1_extracted/foundation_raw.json")
	print(f"| Loading: {input_file}")
	
	terms = load_json_file(input_file)
	print(f"+ Loaded {len(terms)} terms\n")
	
	print("> Migrating reviewed terms...")
	migrated = migrate_reviewed_terms(terms)

	if migrated > 0:
		print()
		print(f"| Saving changes...")
		save_json_file(terms, input_file)
		print(f"+ Migration complete: {migrated} terms updated\n")
	else:
		print()
		print("- No terms to migrate")
		print()

if __name__ == "__main__": main()
