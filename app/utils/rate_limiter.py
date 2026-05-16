"""Simple in-memory fixed-window rate limiter."""

import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Limit requests per client IP within a fixed time window."""

    def __init__(self, app, requests_per_window: int, window_seconds: int) -> None:
        super().__init__(app)
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.monotonic()
        bucket = self.requests[client_ip]

        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.requests_per_window:
            retry_after = int(self.window_seconds - (now - bucket[0])) if bucket else self.window_seconds
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json",
                headers={"Retry-After": str(max(retry_after, 1))},
            )

        bucket.append(now)
        return await call_next(request)
