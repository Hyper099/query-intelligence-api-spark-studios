import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import init_db
from app.routes.queries import router as queries_router
from app.utils.logging import configure_logging
from app.utils.rate_limiter import RateLimitMiddleware

configure_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    RateLimitMiddleware,
    requests_per_window=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
app.include_router(queries_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id
    started = time.perf_counter()

    try:
        response = await call_next(request)
    except SQLAlchemyError:
        logger.exception("database_failure request_id=%s", request_id)
        return JSONResponse(status_code=503, content={"detail": "Database unavailable"})
    except Exception:
        logger.exception("unhandled_request_failure request_id=%s", request_id)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    latency_ms = int((time.perf_counter() - started) * 1000)
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request_completed method=%s path=%s status=%s latency_ms=%s request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
        request_id,
    )
    return response


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
