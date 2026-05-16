"""Small helpers for parsing model-produced JSON."""

import json
import re
from typing import Any


class JSONParseError(ValueError):
    """Raised when text cannot be parsed into a JSON object."""


def parse_json_object(text: str) -> tuple[dict[str, Any], str]:
    """Parse a JSON object from raw LLM text."""

    cleaned = cleanup_json_text(text)

    try:
        return _load_object(cleaned), "llm" if cleaned == text.strip() else "llm_cleaned"
    except (json.JSONDecodeError, TypeError):
        pass

    json_block = extract_json_block(cleaned)
    if json_block:
        try:
            repaired = repair_common_json_issues(json_block)
            return _load_object(repaired), "llm_cleaned"
        except (json.JSONDecodeError, TypeError):
            pass

    raise JSONParseError("Unable to parse a JSON object from LLM response")


def cleanup_json_text(text: str) -> str:
    return text.strip().replace("```json", "").replace("```JSON", "").replace("```", "").strip()


def extract_json_block(text: str) -> str | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]


def repair_common_json_issues(text: str) -> str:
    repaired = text.strip()
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    repaired = repaired.replace("None", "null").replace("True", "true").replace("False", "false")
    return repaired


def _load_object(text: str) -> dict[str, Any]:
    value = json.loads(text)
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object")
    return value
