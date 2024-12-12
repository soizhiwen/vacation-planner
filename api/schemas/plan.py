from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from api.schemas.common import PyObjectId


class ActivitySchema(BaseModel):
    time: str = Field(description="The suggested time for the activity")
    place: str = Field(description="The name of the place")
    activity: str = Field(description="The activity to do")
    notes: str = Field(description="Additional notes for the activity")


class DaySchema(BaseModel):
    day: int = Field(description="The day of the plan")
    activities: list[ActivitySchema] = Field(description="The activities for the day")


class HeaderSchema(BaseModel):
    title: str = Field(description="The title of the plan")
    description: str = Field(description="The description of the plan")


class PlanSchema(HeaderSchema):
    days: list[DaySchema] = Field(description="The days of the plan")


class UserInputSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    budget: int = Field(description="The budget for vacation")
    total_days: int = Field(alias="totalDays", description="The total days for vacation")


class CreatePlanSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id", description="ID of the plan")


class ReadPlanSchema(CreatePlanSchema, UserInputSchema, PlanSchema):
    timestamp: datetime = Field(description="The timestamp of the plan creation")


class ReadPlansSchema(CreatePlanSchema, HeaderSchema):
    pass
