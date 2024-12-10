from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


from api import logger
from api.routers import plans
from api.database.manager import mongo_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await mongo_manager.connect()
    yield
    await mongo_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(plans.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(req: Request, exc: HTTPException) -> JSONResponse:
    logger.error(exc)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    req: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error(exc)
    exc = jsonable_encoder(exc.errors())
    return JSONResponse(exc, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
