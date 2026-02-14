from fastapi import FastAPI
from app.api.routes import router
from app.logger import configure_logging
from app.middleware.request_context import RequestContextMiddleware


configure_logging()

app = FastAPI(title="Weather Proxy")

app.add_middleware(RequestContextMiddleware)

app.include_router(router)
