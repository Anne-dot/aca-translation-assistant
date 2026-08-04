#!/usr/bin/env python3
import json
from datetime import datetime

# AI analysis results
# TODO: [[
# 	what is this here for? it should be in some external file,
# 	either as a csv or, more likely, a human-readable note -
# 	that is, if it's even needed anymore.
# ]] - Henri
TERMS_TO_FLAG = {
	'blindsided':            'Synonym "shocked by something you didn\'t expect" is a definition/explanation, not an alternative term',
	'challenge zone':        'Synonym "mindset of embracing change..." is a definition explaining the concept',
	'chemically addicted':   'Synonym "physically dependent on a substance" is a definition, not an alternative term',
	'comfort zone':          'Need to check - likely definition',
	'conscious contact':     'Need to check - likely definition',
	'critical inner parent': 'Need to check - likely definition',
	'cross-addiction':       'Need to check - likely definition',
	'cycle of dysfunction':  'Need to check - likely definition',
	'denial':                'Need to check - likely definition',
	'differentiate':         'Need to check - likely definition',
	'discount feelings':     'Need to check - likely definition',
	'dissociate':            'Need to check - likely definition',
	'distorted image':       'Need to check - likely definition',
	'dysfunctional family':  'Need to check - likely definition',
	'emotional sobriety':    'Need to check - likely definition',
}

def find_definitions_in_synonyms():
	with open(
		'data/1_extracted/synonyms_analysis.json',
		'r', encoding = 'utf-8'
	) as f: candidates = json.load(f)
	
	to_flag = {}
	
	for item in candidates:
		term         = item['term']
		synonyms     = item['synonyms']
		synonym_text = ', '.join(synonyms)
		
		
		
		reason = None
		if len(synonym_text) > 40 and any(
			word in synonym_text.lower() for word in
			['of', 'the', 'a person', 'someone', 'something']
		):
			reason = f'Long explanatory phrase: "{synonym_text}"'
		elif any(pattern in synonym_text.lower() for pattern in [
			'a person who',
			'someone who',
			'the act of',
			'the process of',
			'feeling of',
			'state of',
			'condition of'
		]):
			reason = f'Definition pattern detected: "{synonym_text}"'
		elif any(
			synonym.strip().split()[0].endswith('ing') and
			len(synonym) > 30 for synonym in synonyms
		):
			reason = f'Gerund with explanation: "{synonym_text}"'
		
		if reason: to_flag[term] = reason
	
	return to_flag

def main():
	input_file = "data/1_extracted/foundation_raw.json"
	
	print("> Analyzing all terms...")
	to_flag = find_definitions_in_synonyms()
	print(f") Analysis complete: {len(to_flag)} terms to flag\n")
	
	with open(input_file, 'r', encoding = 'utf-8') as file:
		terms = json.load(file)
	flagged_count = 0
	
	for term in terms:
		if term['term'] in to_flag:
			if term.get("reviewedAt") or term.get("needsReview"): continue
			
			term["needsReview"] = True
			if "reviewNotes" not in term: term["reviewNotes"] = []
			
			term["reviewNotes"].append({
				"date": datetime.now().isoformat(),
				"note": f"synonyms (AI): {to_flag[term['term']]}"
			})
			
			flagged_count += 1
			print(f") Flagged: {term['term']}")
	
	with open(input_file, "w", encoding = "utf-8") as file:
		json.dump(terms, file, ensure_ascii = False, indent=2)
	
	print(f"\n)) Done! Flagged {flagged_count} terms in foundation_raw.json")

if __name__ == '__main__': main()
