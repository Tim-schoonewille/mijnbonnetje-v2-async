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
    column_filter_string: str | None = None,
    column_filter_string_value: str | UUID | None = None,
    column_filter_int: str | None = None,
    column_filter_int_value: int | None = None
) -> dict:
    return {
        "skip": skip,
        "limit": limit,
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "date_filter": date_filter,
        'column_filter_string': column_filter_string,
        'column_filter_string_value': column_filter_string_value,
        'column_filter_int': column_filter_int,
        'column_filter_int_value': column_filter_int_value,


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
