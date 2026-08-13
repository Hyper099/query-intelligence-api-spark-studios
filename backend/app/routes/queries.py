from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.repositories.query_repository import QueryRepository
from app.schemas.query import QueryCreate, QueryResponse
from app.services.llm_service import LLMService
from app.services.query_service import QueryService

router = APIRouter(prefix="/queries", tags=["queries"])


def get_query_service(
    db: Session = Depends(get_db),  # noqa: B008
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> QueryService:
    """Build a query service for the current request."""

    return QueryService(
        repository=QueryRepository(db),
        llm_service=LLMService(settings),
        settings=settings,
    )


@router.post(
    "", 
    response_model=QueryResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_query(
    payload: QueryCreate,
    request: Request,
    service: QueryService = Depends(get_query_service),  # noqa: B008
) -> QueryResponse:
    """Process and store a natural language research query."""

    request_id = getattr(request.state, "request_id", "unknown")
    return service.create_query(payload.query, request_id=request_id)


@router.get(
    "/{query_id}", 
    response_model=QueryResponse
)
def get_query(
    query_id: int, 
    service: QueryService = Depends(get_query_service)  # noqa: B008
) -> QueryResponse:
    """Return a previously processed query."""

    result = service.get_query(query_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")
    return result
