import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import MongoClient

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
