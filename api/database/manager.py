import os

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from api import logger


class MongoManager:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

    async def connect(self) -> None:
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(
            os.getenv("ME_CONFIG_MONGODB_SERVER"),
            int(os.getenv("ME_CONFIG_MONGODB_PORT")),
            username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
            password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
        )
        self.database = self.client[os.getenv("MONGO_INITDB_DATABASE")]
        logger.info("Connected to MongoDB")

    async def close(self) -> None:
        logger.info("Closing MongoDB connection")
        self.client.close()
        logger.info("Closed MongoDB connection")


mongo_manager = MongoManager()


async def get_database() -> AsyncIOMotorDatabase:
    if mongo_manager.database is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database is not connected",
        )
    return mongo_manager.database
