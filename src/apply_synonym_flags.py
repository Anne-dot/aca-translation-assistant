#!/usr/bin/env python3
import json
from datetime import datetime
from ai_synonym_analysis_results import ANALYSIS_RESULTS

def main():
	print("Applying AI synonym analysis results...")
	print()
	
	input_file = "data/1_extracted/foundation_raw.json"
	
	with open(input_file, 'r', encoding='utf-8') as f:
		terms = json.load(f)
	
	flagged_count = 0
	skipped_count = 0
	
	for term in terms:
		if term_name := term['term'] not in ANALYSIS_RESULTS: continue
		
		should_flag, reason = ANALYSIS_RESULTS[term_name]
		if not should_flag: continue
		
		if term.get('reviewedAt') or term.get('needsReview'):
			skipped_count += 1
			print(f"Skipped (already flagged/reviewed): {term_name}")
			continue
		
		term['needsReview'] = True
		
		if 'reviewNotes' not in term: term['reviewNotes'] = []
		
		term['reviewNotes'].append({
			'date': datetime.now().isoformat(),
			'note': f'synonyms (AI): {reason}'
		})
		
		flagged_count += 1
		print(f"Flagged: {term_name}")
	
	
	
	with open(input_file, 'w', encoding='utf-8') as f:
		json.dump(terms, f, ensure_ascii=False, indent=2)
	
	print(f"""

================================================================================
Done!
	Flagged {flagged_count} terms.
	Skipped {skipped_count} terms (already flagged / reviewed).
================================================================================""")

if __name__ == '__main__': main()
