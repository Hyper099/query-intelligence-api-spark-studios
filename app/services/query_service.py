import logging
import time

from pydantic import ValidationError

from app.config import Settings
from app.repositories.query_repository import QueryRepository
from app.schemas.query import QueryMetadata, QueryResponse, QueryValidation, StructuredData
from app.services.llm_service import LLMService, LLMServiceError
from app.utils.heuristics import heuristic_extract
from app.utils.json_parser import JSONParseError, parse_json_object
from app.utils.query_text import normalize_query_text

logger = logging.getLogger(__name__)


class QueryService:
    """Coordinates LLM extraction, fallback parsing, and persistence."""

    def __init__(self, repository: QueryRepository, llm_service: LLMService, settings: Settings) -> None:
        self.repository = repository
        self.llm_service = llm_service
        self.settings = settings

    def create_query(self, raw_query: str, request_id: str) -> QueryResponse:
        """Process a query and persist the result."""

        started = time.perf_counter()
        normalized_query = normalize_query_text(raw_query)
        structured_data, extraction_source, schema_valid = self._extract_structured_data(
            normalized_query,
            request_id,
        )
        latency_ms = int((time.perf_counter() - started) * 1000)

        record = self.repository.create(
            raw_query=raw_query,
            normalized_query=normalized_query,
            structured_data=structured_data,
            model_used=self.settings.anthropic_model,
            prompt_version=self.settings.prompt_version,
            processing_latency_ms=latency_ms,
            extraction_source=extraction_source,
        )

        logger.info(
            "query_processed query_id=%s latency_ms=%s extraction_status=%s request_id=%s",
            record.id,
            latency_ms,
            "success" if schema_valid else "fallback",
            request_id,
        )
        return self._record_to_response(record)

    def get_query(self, query_id: int) -> QueryResponse | None:
        """Retrieve a stored query by id."""

        record = self.repository.get(query_id)
        if record is None:
            return None
        return self._record_to_response(record)

    def _extract_structured_data(self, query: str, request_id: str) -> tuple[StructuredData, str, bool]:
        try:
            raw_response = self.llm_service.extract_query(query)
            parsed_json, source = parse_json_object(raw_response)
            return StructuredData.model_validate(parsed_json), source, True
        except (LLMServiceError, JSONParseError, ValidationError) as exc:
            logger.warning(
                "structured_extraction_fallback reason=%s request_id=%s",
                type(exc).__name__,
                request_id,
            )
            return heuristic_extract(query), "heuristic", False

    def _record_to_response(self, record) -> QueryResponse:
        structured_data = self.repository.structured_data_from_record(record)
        schema_valid = record.extraction_source != "heuristic"
        return QueryResponse(
            id=record.id,
            normalized_query=record.normalized_query,
            structured_data=structured_data,
            metadata=QueryMetadata(
                model=record.model_used,
                prompt_version=record.prompt_version,
                processing_latency_ms=record.processing_latency_ms,
                extraction_source=record.extraction_source,
            ),
            validation=QueryValidation(schema_valid=schema_valid),
            created_at=record.created_at,
        )
