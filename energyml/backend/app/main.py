import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import get_engine
from app.services.datasets import DatasetInUseError

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("energyml")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    settings.dataset_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Reproducible renewable forecasting and voltage state-estimation research.",
    lifespan=lifespan,
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.middleware("http")
async def request_context(request: Request, call_next: object) -> object:
    request_id = request.headers.get("x-request-id", str(uuid4()))[:100]
    content_length = int(request.headers.get("content-length", "0"))
    if content_length > settings.max_request_bytes:
        return JSONResponse(
            status_code=413, content={"detail": "request payload is too large"}
        )
    started = perf_counter()
    response = await call_next(request)  # type: ignore[operator]
    response.headers["x-request-id"] = request_id
    logger.info(
        "request completed in %.2fms",
        (perf_counter() - started) * 1000,
        extra={"request_id": request_id, "status": response.status_code},
    )
    return response


@app.exception_handler(LookupError)
async def not_found(_: Request, error: LookupError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(DatasetInUseError)
async def dataset_in_use(_: Request, error: DatasetInUseError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(error)})


@app.exception_handler(ValueError)
async def invalid_request(_: Request, error: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(error)})


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> str:
    return (Path(__file__).parent / "static" / "dashboard.html").read_text()
