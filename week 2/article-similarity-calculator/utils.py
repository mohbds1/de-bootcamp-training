import csv
import pickle
from typing import Dict, Iterable, List

def read_articles_csv(path: str) -> Iterable[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"id", "title", "content"}
        fields = set(reader.fieldnames or [])
        if not required.issubset(fields):
            raise ValueError(f"CSV must contain columns {required}. Found: {reader.fieldnames}")
        for row in reader:
            yield {
                "id": (row.get("id") or "").strip(),
                "title": (row.get("title") or "").strip(),
                "content": (row.get("content") or "").strip(),
            }

def save_pickle(obj, path: str) -> None:
    with open(path, "wb") as f:
        pickle.dump(obj, f)