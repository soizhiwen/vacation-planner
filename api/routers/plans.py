from datetime import datetime

import pymongo
from fastapi import APIRouter, HTTPException, Request, Response, status

from api import logger
from api.chains.plans import create_plan_chain
from api.schemas import (
    PyObjectId,
    CreatePlanInput,
    CreatePlanOutput,
    ReadPlanOutput,
    ReadPlansOutput,
)

router = APIRouter(prefix="/plans")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePlanOutput)
async def create_plan(data: CreatePlanInput, req: Request) -> CreatePlanOutput:
    logger.info(f"Creating plan: {data}")
    data = data.model_dump()
    plan = await create_plan_chain(**data)
    plan = plan.model_dump()
    plan["timestamp"] = datetime.now()
    plan = data | plan
    new_plan = req.app.db["plans"].insert_one(plan)
    logger.info(f"Plan created: {new_plan.inserted_id}")
    return {"id": new_plan.inserted_id}


@router.get("/", response_model=list[ReadPlansOutput])
async def read_plans(req: Request, limit: int = 10) -> list[ReadPlansOutput]:
    logger.info(f"Reading plans: {limit}")
    plans = req.app.db["plans"].find(
        {},
        {"_id": 1, "title": 1, "description": 1},
        sort=[("timestamp", pymongo.DESCENDING)],
        limit=limit,
    )
    logger.info(f"Plans read: {plans}")
    return list(plans)


@router.get("/{id}", response_model=ReadPlanOutput)
async def read_plan(id: PyObjectId, req: Request) -> ReadPlanOutput:
    logger.info(f"Reading plan: {id}")
    plan = req.app.db["plans"].find_one({"_id": id})
    if plan is not None:
        logger.info(f"Plan read: {plan}")
        return plan
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found.")


@router.delete("/{id}")
async def delete_plan(id: PyObjectId, req: Request, res: Response) -> Response:
    logger.info(f"Deleting plan: {id}")
    deleted_plan = req.app.db["plans"].delete_one({"_id": id})
    if deleted_plan.deleted_count == 1:
        res.status_code = status.HTTP_204_NO_CONTENT
        logger.info(f"Plan deleted: {id}")
        return res
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found.")
