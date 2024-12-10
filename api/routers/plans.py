from datetime import datetime

import pymongo
from fastapi import APIRouter, HTTPException, Response, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from api import logger
from api.chains.plan import create_plan_chain
from api.database.manager import get_database
from api.schemas import (
    PyObjectId,
    CreatePlanInput,
    CreatePlanOutput,
    ReadPlanOutput,
    ReadPlansOutput,
)

router = APIRouter(prefix="/plans")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePlanOutput)
async def create_plan(
    data: CreatePlanInput, db: AsyncIOMotorDatabase = Depends(get_database)
) -> CreatePlanOutput:
    logger.info(f"Creating plan: {data}")
    data = data.model_dump()
    plan = await create_plan_chain(**data)
    plan = plan.model_dump()
    plan["timestamp"] = datetime.now()
    plan = data | plan
    new_plan = await db["plans"].insert_one(plan)
    logger.info(f"Plan created: {new_plan.inserted_id}")
    return {"id": new_plan.inserted_id}


@router.get("/", response_model=list[ReadPlansOutput])
async def read_plans(
    limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_database)
) -> list[ReadPlansOutput]:
    logger.info(f"Reading plans: {limit}")
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
    logger.info(f"Plans read: {plans}")
    return plans


@router.get("/{id}", response_model=ReadPlanOutput)
async def read_plan(
    id: PyObjectId, db: AsyncIOMotorDatabase = Depends(get_database)
) -> ReadPlanOutput:
    logger.info(f"Reading plan: {id}")
    plan = await db["plans"].find_one({"_id": id})
    if plan is not None:
        logger.info(f"Plan read: {plan}")
        return plan
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found.")


@router.delete("/{id}")
async def delete_plan(
    id: PyObjectId, db: AsyncIOMotorDatabase = Depends(get_database)
) -> Response:
    logger.info(f"Deleting plan: {id}")
    deleted_plan = await db["plans"].delete_one({"_id": id})
    if deleted_plan.deleted_count == 1:
        logger.info(f"Plan deleted: {id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found.")
