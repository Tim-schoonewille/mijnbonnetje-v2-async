from uuid import UUID
from datetime import datetime

from pydantic import ConfigDict
from pydantic import Field

from app.models.base import CamelBase


class TrafficLogBase(CamelBase):
    path: str
    client: tuple
    server: tuple
    method: str
    path_params: dict | None = None
    type_: str
    http_version: str
    user_id: int | UUID | str | None = None
    query_parameters: dict | None = None


class TrafficLogCreate(TrafficLogBase):
    request_date: datetime = Field(default_factory=datetime.utcnow)


class TrafficLog(TrafficLogBase):
    request_date: datetime
    model_config = ConfigDict(from_attributes=True)


class TrafficLogwithMetaData(CamelBase):
    total: int
    traffic_log: list[TrafficLog]
