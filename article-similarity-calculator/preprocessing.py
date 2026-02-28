import re
from typing import Dict, List, Iterable

def clean_and_tokenize(text: str) -> List[str]:
    """
    Cleaning steps:
      - lowercase
      - remove digits
      - remove punctuation
      - tokenize into words
    """
    text = (text or "").lower()
    text = text.replace("_", " ")          # treat underscore as separator
    text = re.sub(r"\d+", "", text)        # remove digits
    text = re.sub(r"[^\w\s]+", " ", text)  # remove punctuation (replace with space)
    tokens = text.split()                  # tokenize by whitespace
    return tokens

def clean_and_tokenize_articles(articles: Iterable[Dict[str, str]]) -> Iterable[List[str]]:
    for a in articles:
        text = f"{a.get('title', '')} {a.get('content', '')}"
        yield clean_and_tokenize(text)