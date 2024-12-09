import uuid
from typing import Any


from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from . import gpt_key, gpt_model
from api import logger
from api.schemas import Plan


async def create_plan_chain(
    id: uuid.UUID, budget: int, total_days: int
) -> dict[str, Any]:
    logger.info(f"Generating {id}...")
    model = ChatOpenAI(model=gpt_model, api_key=gpt_key).with_structured_output(Plan)

    system_template = "You are an AI travel agent who creates vacation plans."
    human_template = """
    My budget is {budget} dollars.
    I want to go on a vacation for {total_days} days.
    Write a travel itinerary for me.
    """
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("human", human_template)]
    )

    chain = prompt_template | model
    result: Plan = await chain.ainvoke({"budget": budget, "total_days": total_days})
    logger.info(f"Generated {id}")

    return result.model_dump()
