import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from api.chains.plans import create_plan_chain
from api.schemas import CreatePlanInput, CreatePlanOutput, ReadPlanOutput

router = APIRouter(prefix="/plans")


@router.post("/", tags=["plans"])
async def create_plan(
    plan: CreatePlanInput, background_tasks: BackgroundTasks
) -> CreatePlanOutput:
    id = uuid.uuid4()
    background_tasks.add_task(
        create_plan_chain,
        id,
        plan.season,
        plan.hobbies,
        plan.budget,
    )
    return CreatePlanOutput(id=id)


@router.get("/{id}", tags=["plans"])
async def read_plan(id: uuid.UUID) -> ReadPlanOutput:
    #     raise HTTPException(status_code=404, detail="ID not found")

    # return ReadPlanOutput(id=plan.id, plan=plan.plan)
    pass
