from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.base import CamelBase


class ApiCall(CamelBase):
    date: str
    amount: int


class ApiCallLog(CamelBase):
    # id: ObjectId = Field(alias='_id')
    user_id: int | UUID
    created: datetime
    apicalls: list[ApiCall]
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ApiCallLogCreate(BaseModel):
    user_id: int | UUID
    created: datetime
    ApiCalls: list[ApiCall]
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
