import re

def normalize_query_text(query: str) -> str:
    """Trim query text, collapse repeated whitespace, and lowercase it."""

    return re.sub(r"\s+", " ", query.strip()).lower()
