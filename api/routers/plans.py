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
    try:
        data = data.model_dump()
        plan = await create_plan_chain(**data)
        plan = plan.model_dump()
        plan["timestamp"] = datetime.now()
        plan = data | plan
        new_plan = req.app.db["plans"].insert_one(plan)
        return CreatePlanOutput(id=new_plan.inserted_id)
    except Exception as e:
        logger.error(f"Failed to create plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create plan.",
        )


@router.get("/", response_model=list[ReadPlansOutput])
async def read_plans(req: Request, limit: int = 10) -> list[ReadPlansOutput]:
    try:
        plans = req.app.db["plans"].find(
            {},
            {"_id": 1, "title": 1, "description": 1},
            sort=[("timestamp", pymongo.DESCENDING)],
            limit=limit,
        )
        return list(plans)
    except Exception as e:
        logger.error(f"Failed to read plans: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plans not found."
        )


@router.get("/{id}", response_model=ReadPlanOutput)
async def read_plan(id: PyObjectId, req: Request) -> ReadPlanOutput:
    try:
        plan = req.app.db["plans"].find_one({"_id": id})
        if plan is not None:
            return plan
        raise Exception("Plan not found.")
    except Exception as e:
        logger.error(f"Failed to read plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found."
        )


@router.delete("/{id}")
async def delete_plan(id: PyObjectId, req: Request, res: Response) -> Response:
    try:
        deleted_plan = req.app.db["plans"].delete_one({"_id": id})
        if deleted_plan.deleted_count == 1:
            res.status_code = status.HTTP_204_NO_CONTENT
            return res
        raise Exception("Plan not found.")
    except Exception as e:
        logger.error(f"Failed to delete plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found."
        )
