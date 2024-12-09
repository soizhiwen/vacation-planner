import uuid
from typing import Any, Union

import pymongo
from pymongo.cursor import Cursor

from . import db


def create(data: dict[str, Any]) -> None:
    db["plans"].insert_one(data)


def read(id: uuid.UUID) -> Union[dict[str, Any], None]:
    return db["plans"].find_one({"id": id}, {"_id": 0})


def read_limit(limit: int = 10) -> Cursor:
    return (
        db["plans"]
        .find(
            {},
            {"_id": 0, "title": 1, "description": 1},
            sort=[("timestamp", pymongo.DESCENDING)],
        )
        .limit(limit)
    )


def delete(id: uuid.UUID) -> None:
    db["plans"].delete_one({"id": id})
