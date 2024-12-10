import pymongo
from pymongo.results import InsertOneResult
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, Response, status

from api.schemas.common import PyObjectId
from api.schemas.plan import UserInputSchema, ReadPlanSchema, ReadPlansSchema


async def create_plan(
    plan: UserInputSchema, db: AsyncIOMotorDatabase
) -> InsertOneResult:
    created_plan = await db["plans"].insert_one(plan)
    return created_plan


async def read_plans(limit: int, db: AsyncIOMotorDatabase) -> list[ReadPlansSchema]:
    plans = (
        await db["plans"]
        .find(
            {},
            {"_id": 1, "title": 1, "description": 1},
            sort=[("timestamp", pymongo.DESCENDING)],
            limit=limit,
        )
        .to_list()
    )
    return plans


async def read_plan(id: PyObjectId, db: AsyncIOMotorDatabase) -> ReadPlanSchema:
    plan = await db["plans"].find_one({"_id": id})
    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found."
        )
    return plan


async def delete_plan(id: PyObjectId, db: AsyncIOMotorDatabase) -> Response:
    deleted_plan = await db["plans"].delete_one({"_id": id})
    if deleted_plan.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found.")
