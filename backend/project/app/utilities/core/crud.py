from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import Query


def convert_to_datetime(str_date: str) -> datetime:
    return datetime.strptime(str_date, "%Y-%m-%d")


async def parameters(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 1000,
    user_id: int | UUID | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    date_filter: str = "created_at",
) -> dict:
    return {
        "skip": skip,
        "limit": limit,
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "date_filter": date_filter,
    }


async def count_parameters(
    start_date: str | None = None,
    end_date: str | None = None,
    date_filter: str = "created_at",
) -> dict:
    return {
        "start_date": start_date,
        "end_date": end_date,
        "date_filter": date_filter,
    }

