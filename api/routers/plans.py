import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException

from api import logger
from api.chains.plans import create_plan_chain
from api.schemas import CreatePlanInput, CreatePlanOutput, ReadPlanOutput
from api.database import plans

router = APIRouter(prefix="/plans")


@router.post("/", tags=["plans"])
async def create_plan(plan: CreatePlanInput) -> CreatePlanOutput:
    try:
        id = uuid.uuid4()
        data = await create_plan_chain(id, **plan.model_dump())
        data["id"] = id
        data["budget"] = plan.budget
        data["total_days"] = plan.total_days
        data["timestamp"] = datetime.now()
        plans.create(data)
        return CreatePlanOutput(id=id)
    except Exception as e:
        logger.error(f"Failed to create plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to create plan.")


@router.get("/{id}", tags=["plans"])
async def read_plan(id: uuid.UUID) -> ReadPlanOutput:
    try:
        data = plans.read(id)
        return ReadPlanOutput.model_validate(data)
    except Exception as e:
        logger.error(f"Failed to read plan: {e}")
        raise HTTPException(status_code=404, detail="Plan not found.")
