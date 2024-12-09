import uuid
from datetime import datetime

from pydantic import BaseModel, Field


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
    id: uuid.UUID = Field(description="ID of the plan")


class ReadPlanOutput(Plan, CreatePlanInput, CreatePlanOutput):
    timestamp: datetime = Field(description="The timestamp of the plan creation")


class ReadPlansOutput(Header):
    pass
