import re

def normalize_term(term):
	return term.lower().strip()

def clean_text_for_csv(text):
	# replace newlines with pipes, remove extra whitespace
	return ' '.join(text.replace('\n', ' | ').split())

def shorten_text(text, max_length = 100):
	if not text: text = ""
	cleaned = clean_text_for_csv(text)
	return cleaned if len(cleaned) <= max_length
		else (cleaned[:max_length] + "...")

def clean_text(text):
	if not text: text = ''
	return text.replace('\u00a0', ' ').strip()



def parse_list_from_text(text, delimiter=','):
	if not text or not text.strip():
		return []
	
	return [item.strip() for item in text.split(delimiter) if item.strip()]



def detect_numbered_meanings(text):
	if not text:
		return False
	# starts with "1." or has "\n1." followed by space
	return bool(re.search(r'(^|\n)\d+\.\s+', text))

def split_numbered_text(text):
	if not text: return []
	
	# Split by pattern: number followed by period and space
	parts = re.split(r'\n?(\d+)\.\s+', text)
	
	# parts format: ['prefix', '1', 'text1', '2', 'text2', ...]
	result = []
	for i in range(1, len(parts), 2):
		if i + 1 < len(parts):
			result.append(parts[i + 1].strip())
	
	return result if result else [text]

