from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class QueryCreate(BaseModel):
    """Request body for creating a processed query."""

    query: str = Field(..., min_length=3, max_length=1000)

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        """Reject blank or whitespace-only queries."""

        if not value.strip():
            raise ValueError("query must not be blank")
        return value


class StructuredData(BaseModel):
    """Structured intelligence extracted from a research query."""

    industry: str | None = None
    region: str | None = None
    company_type: str | None = None
    keywords: list[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)

    @field_validator("keywords")
    @classmethod
    def normalize_keywords(cls, value: list[str]) -> list[str]:
        """Normalize, deduplicate, and trim extracted keywords."""

        seen: set[str] = set()
        normalized: list[str] = []
        for item in value:
            keyword = item.strip().lower()
            if keyword and keyword not in seen:
                seen.add(keyword)
                normalized.append(keyword)
        return normalized


class QueryMetadata(BaseModel):
    """Operational metadata returned with a processed query."""

    model: str
    prompt_version: str
    processing_latency_ms: int
    extraction_source: str = Field(..., examples=["llm", "llm_cleaned", "heuristic"])


class QueryValidation(BaseModel):
    """Validation metadata for the extracted structured payload."""

    schema_valid: bool


class QueryResponse(BaseModel):
    """API response for a stored query."""

    status: str = "success"
    id: int
    normalized_query: str
    structured_data: StructuredData
    metadata: QueryMetadata
    validation: QueryValidation
    created_at: datetime
