import json

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.query import QueryRecord
from app.schemas.query import StructuredData


class QueryRepository:
    """Repository for query records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        raw_query: str,
        normalized_query: str,
        structured_data: StructuredData,
        model_used: str,
        prompt_version: str,
        processing_latency_ms: int,
        extraction_source: str,
    ) -> QueryRecord:
        """Persist a processed query."""

        record = QueryRecord(
            raw_query=raw_query,
            normalized_query=normalized_query,
            extracted_json=structured_data.model_dump_json(),
            model_used=model_used,
            prompt_version=prompt_version,
            processing_latency_ms=processing_latency_ms,
            extraction_source=extraction_source,
        )
        try:
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get(self, query_id: int) -> QueryRecord | None:
        """Return a stored query by id."""

        return self.db.get(QueryRecord, query_id)

    @staticmethod
    def structured_data_from_record(record: QueryRecord) -> StructuredData:
        """Convert persisted JSON to the public structured-data schema."""

        return StructuredData.model_validate(json.loads(record.extracted_json))
