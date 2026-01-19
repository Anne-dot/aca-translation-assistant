#!/usr/bin/env python3
"""
Extract foundation_glossary.csv to structured JSON.
Part of PHASE 1, STEP 1.1 - Data Pipeline Implementation.
"""

from pathlib import Path
import tools.filemanage
from tools.text_processing import (
	clean_text, parse_list_from_text,
	detect_numbered_meanings, split_numbered_text
)


def extract_term_metadata(raw_term):
	"""
	Extract term name, grammatical type, and cross-references.
	
	Args:
		raw_term: Raw term string from CSV
	
	Returns:
		tuple: (term, grammatical_type, see_also_list)
	"""
	see_also = []
	term_part = raw_term
	
	# Extract "see also" references
	if "– see also" in raw_term or "- see also" in raw_term:
		parts = raw_term.replace("– see also", "|||").replace("- see also", "|||").split("|||")
		term_part = parts[0].strip()
		
		if len(parts) > 1:
			refs = parts[1].strip()
			for ref in refs.split(","):
				ref = ref.strip()
				if ":" in ref:
					ref = ref.split(":", 1)[1].strip()
				see_also.append(ref)
	
	# Extract grammatical type
	grammatical_type = ""
	term = term_part
	
	if "(" in term_part and ")" in term_part:
		start = term_part.rfind("(")
		end = term_part.rfind(")")
		if start < end:
			grammatical_type = term_part[start+1:end]
			term = term_part[:start].strip()
	
	return term, grammatical_type, see_also


def parse_term_row(row):
	"""
	Returns: dict with term data or None if should skip
	"""
	# Skip letter markers (single letter + empty columns)
	if len(row[0]) == 1 and all(not cell.strip() for cell in row[1:]):
		return None
	
	# Extract term metadata
	raw_term = row[0]
	term, grammatical_type, see_also = extract_term_metadata(raw_term)
	
	# Get non-empty columns after term
	non_empty = [row[i] for i in range(1, len(row)) if row[i].strip()]
	
	# Extract raw fields
	definition = non_empty[0] if len(non_empty) > 0 else ""
	synonyms = non_empty[1] if len(non_empty) > 1 else ""
	usageExample = non_empty[2] if len(non_empty) > 2 else ""
	pageReferences = non_empty[3] if len(non_empty) > 3 else ""
	
	# Check if has multiple numbered meanings
	has_multiple = detect_numbered_meanings(definition)
	
	if has_multiple:
		# Auto-split into meanings
		def_parts = split_numbered_text(definition)
		syn_parts = split_numbered_text(synonyms)
		ex_parts = split_numbered_text(usageExample)
		
		# Build meanings array
		meanings = []
		for i in range(len(def_parts)):
			meaning = {
				"definition": clean_text(def_parts[i]) if i < len(def_parts) else "",
				"synonyms": parse_list_from_text(syn_parts[i]) if i < len(syn_parts) else [],
				"usageExample": clean_text(ex_parts[i]) if i < len(ex_parts) else ""
			}
			meanings.append(meaning)
		
		term_data = {
			"term": term,
			"grammaticalType": grammatical_type,
			"seeAlso": see_also,
			"meanings": meanings,
			"pageReferences": clean_text(pageReferences),
			"needsReview": True,
			"reviewedAt": None
		}
	else:
		# Single meaning
		term_data = {
			"term": term,
			"grammaticalType": grammatical_type,
			"seeAlso": see_also,
			"meanings": [{
				"definition": clean_text(definition),
				"synonyms": parse_list_from_text(synonyms),
				"usageExample": clean_text(usageExample)
			}],
			"pageReferences": clean_text(pageReferences),
			"needsReview": False,
			"reviewedAt": None
		}
	
	return term_data


def extract_foundation_glossary():
	"""
	Extract foundation_glossary.csv to JSON format.
	
	Skips letter markers (A-W).
	Extracts 4 fields per term using non-empty column logic.
	Auto-splits terms with multiple numbered meanings.
	
	Returns:
		Number of extracted terms
	"""
	input_file = Path("data/ACA_WSO/foundation_glossary.csv")
	output_file = Path("data/1_extracted/foundation_raw.json")
	
	ensure_directory_exists(output_file)
	
	terms = []
	skipped_markers = 0
	
	for row in read_csv_file(input_file):
		term_data = parse_term_row(row)
		
		if term_data:
			terms.append(term_data)
		else:
			skipped_markers += 1
	
	# Save to JSON (DRY - uses utils)
	save_json_file(terms, output_file)
	
	# Print summary
	print(f"\n✅ Extraction complete!")
	print(f"📊 Extracted: {len(terms)} terms")
	print(f"⏭️  Skipped: {skipped_markers} letter markers")
	print(f"📁 Output: {output_file}\n")
	
	return len(terms)


if __name__ == "__main__":
	extract_foundation_glossary()
