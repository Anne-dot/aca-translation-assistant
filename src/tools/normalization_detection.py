"""
use collect_normalization_issues to get an array of normalization issues in a term
"""

def detect_comma_separated_terms(term_data):
	# ex: "hero, hero child"
	term = term_data["term"]
	if '(' in term or ',' not in term: return None
	
	parts = [p.strip() for p in term.split(',')]
	if len(parts) > 1:
		return {
			"category":   "split_multiple_comma",
			"suggestion": parts
		}
	
	return None

def detect_slash_separated_terms(term_data):
	# ex: "Annual Business Conference/ABC"
	term = term_data["term"]
	if '/' not in term: return None
	
	parts = [p.strip() for p in term.split('/')]
	if len(parts) > 1:
		return {
			"category":   "split_multiple_slash",
			"suggestion": parts
		}
	
	return None

def detect_plural_notation(term_data):
	# ex: caregiver(s), foster child(ren)
	term = term_data["term"]
	if '(' not in term or ')' not in term: return None
	
	for pattern in ["(s)", "(es)", "(ren)"]:
		if pattern in term:
			base = term.replace(pattern, '').strip()
			plural = base + pattern.strip("()")
			
			return {
				"category":   "split_parentheses",
				"pattern":    pattern,
				"suggestion": [base, plural]
			}
	
	return None

def detect_verbose_seealso(term_data):
	# ex: "trauma for further references in the literature"
	see_also = term_data.get("seeAlso", [])
	if not see_also: return None
	
	issues = []
	for entry in see_also:
		word_count = len(entry.split())
		if word_count > 4:
			issues.append({
				"entry":  entry,
				"reason": f"Too long ({word_count} words)"
			})
	
	if issues:
		return {
			"category":   "Clean_seealso",
			"suggestion": issues
		}
	
	return None

def detect_asterisk(term_data):
	# ex: "counseling*", "para-alcoholic*"
	term = term_data["term"]
	if '*' not in term: return None
	
	return {
		"category":   "remove_asterisk",
		"suggestion": {"cleanTerm": term.replace('*', '').strip()}
	}



def collect_normalization_issues(term_data):
	issues = []
	
	for check in [
		detect_comma_separated_terms,
		detect_slash_separated_terms,
		detect_plural_notation,
		detect_verbose_seealso,
		detect_asterisk,
	]:
		issue = check(term_data)
		if issue: issues.append(issue)
	
	return issues
