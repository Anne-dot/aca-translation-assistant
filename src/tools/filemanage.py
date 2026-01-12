"""
Functions for working with direcories and files.
"""

import json
import csv
from pathlib import Path

# TODO: was `ensure_output_dir`
def ensure_directory_exists(file_path):
	Path(file_path).parent.mkdir(parents=True, exist_ok=True)



# TODO: was `read_csv_file`
def read_csv_rows(file_path, delimiter = '\t'):
	with open(file_path, 'r', encoding = 'utf-8') as f:
		reader = csv.reader(f, delimiter=delimiter)
		for row in reader:
			yield row



def load_json_file(file_path):
	with open(file_path, 'r', encoding = 'utf-8') as f:
		return json.load(f)

def save_json_file(data, file_path, indent = 2):
	with open(file_path, 'w', encoding = 'utf-8') as f:
		json.dump(data, f, ensure_ascii = False, indent = indent)
