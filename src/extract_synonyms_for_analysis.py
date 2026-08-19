#!/usr/bin/env python3

import json

def main():
	input_file  = "data/1_extracted/foundation_raw.json"
	output_file = "data/1_extracted/synonyms_analysis.json"
	
	with open(input_file, 'r', encoding = 'utf-8') as file:
		terms = json.load(file)
	
	candidates = []
	
	for term in terms:
		if term.get('reviewedAt') or term.get('needsReview'): continue
		
		has_synonyms  = False
		synonyms_text = []
		
		for meaning in term.get('meanings', []):
			if meaning.get('synonyms'):
				has_synonyms = True
				synonyms_text.extend(meaning.get('synonyms', []))
		
		if has_synonyms: candidates.append({
			'term': term['term'], 'synonyms': synonyms_text
		})
	
	with open(output_file, 'w', encoding='utf-8') as file:
		json.dump(candidates, file, ensure_ascii = False, indent = 2)
	

	print(f"""
) Extracted {len(candidates)} terms with synonyms
* Saved to: {output_file}

Preview (first 5):
""")
	for i, c in enumerate(candidates[:5], 1):
		print(f"""
{i}. {c['term']}
	Synonyms: {c['synonyms']}
""")

if __name__ == '__main__': main()
