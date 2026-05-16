from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class QueryRecord(Base):
    """Persisted natural language query and extracted intelligence."""

    __tablename__ = "queries"

    id: Mapped[int]                         = mapped_column(Integer, primary_key=True, index=True)
    raw_query: Mapped[str]                  = mapped_column(Text, nullable=False)
    normalized_query: Mapped[str]           = mapped_column(Text, nullable=False)
    extracted_json: Mapped[str]             = mapped_column(Text, nullable=False)

    model_used: Mapped[str]                 = mapped_column(String(100), nullable=False)
    prompt_version: Mapped[str]             = mapped_column(String(20), nullable=False)
    processing_latency_ms: Mapped[int]      = mapped_column(Integer, nullable=False)
    extraction_source: Mapped[str]          = mapped_column(String(30), nullable=False, default="llm")

    created_at: Mapped[datetime]            = mapped_column(
                                                DateTime(timezone=True),
                                                default=lambda: datetime.now(timezone.utc),
                                                nullable=False,
                                            )
