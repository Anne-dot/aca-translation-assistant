import json
import csv
from pathlib import Path


def ensure_directory_exists(file_path: str) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def read_csv_file(file_path: str, delimiter: str = "\t") -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            yield row


def load_json_file(file_path: str) -> any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data: any, file_path: str, indent: int = 2) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
