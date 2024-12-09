import uuid
from typing import Any, Union

import pymongo

from . import db
from api import logger


def create(data: dict[str, Any]) -> None:
    try:
        db["plans"].insert_one(data)
    except Exception as e:
        logger.error(f"Failed to create plan: {e}")


def read(id: uuid.UUID) -> Union[dict[str, Any], None]:
    try:
        return db["plans"].find_one({"id": id}, {"_id": 0})
    except Exception as e:
        logger.error(f"Failed to read plan: {e}")


def read_all() -> Union[list[dict[str, Any]], None]:
    try:
        return db["plans"].find(
            {},
            {"_id": 0, "title": 1, "description": 1},
            sort=[("timestamp", pymongo.DESCENDING)],
        )
    except Exception as e:
        logger.error(f"Failed to read plan: {e}")


def delete(id: uuid.UUID) -> None:
    try:
        db["plans"].delete_one({"id": id})
    except Exception as e:
        logger.error(f"Failed to delete plan: {e}")
