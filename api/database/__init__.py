import os

from pymongo import MongoClient

mongo = MongoClient(
    os.getenv("ME_CONFIG_MONGODB_SERVER"),
    int(os.getenv("ME_CONFIG_MONGODB_PORT")),
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
    uuidRepresentation="standard",
)
db = mongo[os.getenv("MONGO_INITDB_DATABASE")]
