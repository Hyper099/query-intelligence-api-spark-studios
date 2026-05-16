"""Fallback structured extraction when LLM output is unavailable or invalid."""

import re

from app.schemas.query import StructuredData

REGION_ALIASES: dict[str, str] = {
    "southeast asia": "Southeast Asia",
    "south east asia": "Southeast Asia",
    "europe": "Europe",
    "north america": "North America",
    "latin america": "Latin America",
    "south america": "South America",
    "middle east": "Middle East",
    "africa": "Africa",
    "asia": "Asia",
    "united states": "United States",
    "usa": "United States",
    "us": "United States",
    "india": "India",
    "china": "China",
}

COMPANY_TYPES: dict[str, str] = {
    "startups": "startup",
    "startup": "startup",
    "scaleups": "scaleup",
    "scaleup": "scaleup",
    "enterprises": "enterprise",
    "enterprise": "enterprise",
    "companies": "company",
    "company": "company",
    "vendors": "vendor",
    "vendor": "vendor",
}

STOPWORDS = {
    "find",
    "show",
    "list",
    "identify",
    "research",
    "the",
    "a",
    "an",
    "in",
    "for",
    "of",
    "and",
    "or",
    "with",
    "near",
    "by",
}


def heuristic_extract(query: str) -> StructuredData:
    """Extract a best-effort structured response from query text."""

    lower_query = query.lower()
    region = _detect_region(lower_query)
    company_type = _detect_company_type(lower_query)
    keywords = _extract_keywords(lower_query)
    industry = _detect_industry(lower_query, region, company_type)

    confidence = 0.45
    if industry:
        confidence += 0.15
    if region:
        confidence += 0.1
    if company_type:
        confidence += 0.1

    return StructuredData(
        industry=industry,
        region=region,
        company_type=company_type,
        keywords=keywords,
        confidence_score=min(confidence, 0.75),
    )


def _detect_region(lower_query: str) -> str | None:
    for alias, canonical in REGION_ALIASES.items():
        if re.search(rf"\b{re.escape(alias)}\b", lower_query):
            return canonical
    return None


def _detect_company_type(lower_query: str) -> str | None:
    for alias, canonical in COMPANY_TYPES.items():
        if re.search(rf"\b{re.escape(alias)}\b", lower_query):
            return canonical
    return None


def _extract_keywords(lower_query: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", lower_query)
    keywords: list[str] = []
    for word in words:
        if word in STOPWORDS or len(word) < 2:
            continue
        if word not in keywords:
            keywords.append(word)
    return keywords[:10]


def _detect_industry(lower_query: str, region: str | None, company_type: str | None) -> str | None:
    text = lower_query
    for phrase in REGION_ALIASES:
        text = re.sub(rf"\b{re.escape(phrase)}\b", " ", text)
    for phrase in COMPANY_TYPES:
        text = re.sub(rf"\b{re.escape(phrase)}\b", " ", text)
    words = [
        word
        for word in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text)
        if word not in STOPWORDS and len(word) > 1
    ]
    if not words:
        return None
    return " ".join(words[:3])
