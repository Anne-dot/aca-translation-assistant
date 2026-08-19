#!/usr/bin/env python3

from pathlib import Path
from tools.filemanage import (
    ensure_directory_exists,
    read_csv_file, save_json_file
)
from tools.text_processing import (
	clean_text, parse_list_from_text,
	has_numbered_meanings, split_numbered_text
)
import re


def extract_term_metadata(raw_term):
	see_also = []
	term_part = raw_term
	
	if re.search("[–-] see also", raw_term):
		parts = re.split("[–-] see also", raw_term)
		term_part = parts[0].strip()
		
		if len(parts) > 1:
			refs = parts[1].strip()
			for ref in refs.split(","):
				ref = ref.strip()
				if ":" in ref: ref = ref.split(":", 1)[1].strip()
				see_also.append(ref)
	
	grammatical_type = ""
	term = term_part
	
	if "(" in term_part and ")" in term_part:
		start = term_part.rfind("(")
		end   = term_part.rfind(")")
		if start < end:
			grammatical_type = term_part[start+1:end]
			term = term_part[:start].strip()
	
	return term, grammatical_type, see_also


def parse_term_row(row):
	if (len(row[0]) == 1 and all(not cell.strip() for cell in row[1:])):
		return None
	
	raw_term = row[0]
	term, grammatical_type, see_also = extract_term_metadata(raw_term)
	
	non_empty = [row[i] for i in range(1, len(row)) if row[i].strip()]
	
	definition     = non_empty[0] if len(non_empty) > 0 else ""
	synonyms       = non_empty[1] if len(non_empty) > 1 else ""
	usageExample   = non_empty[2] if len(non_empty) > 2 else ""
	pageReferences = non_empty[3] if len(non_empty) > 3 else ""
	
	if has_numbered_meanings(definition):
		def_parts = split_numbered_text(definition)
		syn_parts = split_numbered_text(synonyms)
		ex_parts  = split_numbered_text(usageExample)
		
		meanings = []
		for i in range(len(def_parts)):
			meaning = {"definition": "", "synonyms": [], "usageExample": ""}
			if i < len(def_parts): meaning["definition"  ] = clean_text(def_parts[i])
			if i < len(syn_parts): meaning["synonyms"    ] = parse_list_from_text(syn_parts[i])
			if i < len(ex_parts):  meaning["usageExample"] = clean_text(ex_parts[i])
			
			meanings.append(meaning)
		
		term_data = {
			"term":            term,
			"grammaticalType": grammatical_type,
			"seeAlso":         see_also,
			"pageReferences":  clean_text(pageReferences),
			"needsReview":     True,
			"reviewedAt":      None,
			"meanings":        meanings,
		}
	else:
		term_data = {
			"term":            term,
			"grammaticalType": grammatical_type,
			"seeAlso":         see_also,
			"pageReferences":  clean_text(pageReferences),
			"needsReview":     False,
			"reviewedAt":      None,
			"meanings": [{
				"definition":   clean_text(definition),
				"synonyms":     parse_list_from_text(synonyms),
				"usageExample": clean_text(usageExample)
			}],
		}
	
	return term_data


def main():
	input_file  = Path("data/ACA_WSO/foundation_glossary.csv")
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
	
	save_json_file(terms, output_file)
	
	print(f"""
Extraction complete!
	+ Extracted: {len(terms)} terms
	-   Skipped: {skipped_markers} letter markers
	*    Output: {output_file}
""")

if __name__ == "__main__": main()
