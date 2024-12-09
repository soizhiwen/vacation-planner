from typing import Any
from datetime import datetime

from bson import ObjectId
from pydantic_core import core_schema
from pydantic import BaseModel, ConfigDict, Field


class PyObjectId(str):
    """To create a pydantic Object that validates bson ObjectID"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)


class Activity(BaseModel):
    time: str = Field(description="The time of the activity")
    place: str = Field(description="The place of the activity")
    activity: str = Field(description="The activity to do")
    notes: str = Field(description="Additional notes for the activity")


class Day(BaseModel):
    day: int = Field(description="The day of the plan")
    activities: list[Activity] = Field(description="The activities for the day")


class Header(BaseModel):
    title: str = Field(description="The title of the plan")
    description: str = Field(description="The description of the plan")


class Plan(Header):
    days: list[Day] = Field(description="The days of the plan")


class CreatePlanInput(BaseModel):
    budget: int = Field(description="The budget for vacation")
    total_days: int = Field(description="The total days for vacation")


class CreatePlanOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: PyObjectId = Field(alias="_id", description="ID of the plan")


class ReadPlanOutput(Plan, CreatePlanInput, CreatePlanOutput):
    timestamp: datetime = Field(description="The timestamp of the plan creation")


class ReadPlansOutput(Header, CreatePlanOutput):
    pass
