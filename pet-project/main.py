import logging
from contextlib import asynccontextmanager
import time
from core.models import db_helper
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from logging_config import configure_logging
from api import router as api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting application : lifespan")
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.include_router(
    api_router,
)


@main_app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Response: {process_time:2.2f}s | {response.status_code}")
    response.headers["X-Process-Time"] = str(process_time)
    return response
