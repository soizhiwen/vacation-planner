from datetime import datetime

from fastapi import APIRouter, Response, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from api import logger
from api.crud import plans as crud_plans
from api.chains.plans import create_plan_chain
from api.database.manager import get_database
from api.schemas.common import PyObjectId
from api.schemas.plan import (
    UserInputSchema,
    CreatePlanSchema,
    ReadPlanSchema,
    ReadPlansSchema,
)

router = APIRouter(prefix="/plans")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreatePlanSchema)
async def create_plan(
    data: UserInputSchema, db: AsyncIOMotorDatabase = Depends(get_database)
) -> CreatePlanSchema:
    logger.info(f"Creating plan: {data}")
    data = data.model_dump()
    plan = await create_plan_chain(**data)
    plan = plan.model_dump()
    plan["timestamp"] = datetime.now()
    plan = data | plan
    created_plan = await crud_plans.create_plan(plan, db)
    logger.info(f"Plan created: {created_plan.inserted_id}")
    return {"id": created_plan.inserted_id}


@router.get("/", response_model=list[ReadPlansSchema])
async def read_plans(
    limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_database)
) -> list[ReadPlansSchema]:
    logger.info(f"Reading plans: {limit}")
    plans = await crud_plans.read_plans(limit, db)
    logger.info(f"Plans read: {plans}")
    return plans


@router.get("/{id}", response_model=ReadPlanSchema)
async def read_plan(
    id: PyObjectId, db: AsyncIOMotorDatabase = Depends(get_database)
) -> ReadPlanSchema:
    logger.info(f"Reading plan: {id}")
    plan = await crud_plans.read_plan(id, db)
    logger.info(f"Plan read: {plan}")
    return plan


@router.delete("/{id}")
async def delete_plan(
    id: PyObjectId, db: AsyncIOMotorDatabase = Depends(get_database)
) -> Response:
    logger.info(f"Deleting plan: {id}")
    response = await crud_plans.delete_plan(id, db)
    logger.info(f"Plan deleted: {id}")
    return response
