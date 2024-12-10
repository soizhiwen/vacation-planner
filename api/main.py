import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from pymongo import MongoClient
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from api import logger
from api.routers import plans


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.mongo = MongoClient(
        os.getenv("ME_CONFIG_MONGODB_SERVER"),
        int(os.getenv("ME_CONFIG_MONGODB_PORT")),
        username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
        password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
    )
    app.db = app.mongo[os.getenv("MONGO_INITDB_DATABASE")]
    yield
    app.mongo.close()


app = FastAPI(lifespan=lifespan)
app.include_router(plans.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error(exc)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(exc)
    exc = jsonable_encoder(exc.errors())
    return JSONResponse(exc, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
