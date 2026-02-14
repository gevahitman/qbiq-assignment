import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.logger import logger


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Very important class.
    This class makes sure that every http request will be wrapped with its duration and uuid.
    simplify the requests, so we won't write it in any http handler function.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        request.state.request_id = request_id

        response = await call_next(request)

        duration = (time.time() - start_time) * 1000

        logger.info(
            "request_completed",
            request_id=request_id,
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=round(duration, 2),
        )

        response.headers["X-Request-ID"] = request_id
        return response
