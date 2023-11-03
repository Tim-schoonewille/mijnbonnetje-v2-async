from datetime import datetime
import json
from typing import Any
from uuid import uuid4
from icecream import ic
from fastapi import APIRouter

from celery.result import AsyncResult
from pydantic import Field

from app import crud, models
from app.models.base import CamelBase
from app.tasks.tasks import export_receipts, run_in_bg_test
from app.tasks.celery import celery_app

from app.utilities.core.dependencies import GetDB, ParametersDepends, VerifiedUser
from app.utilities.receipt import refresh_receipt_entry


router = APIRouter(prefix="/export", tags=["export"])


class ExportBody(CamelBase):
    export_types: list[str] = Field(default_factory=list)


@router.post("/")
async def get_export(
    user: VerifiedUser,
    params: ParametersDepends,
    body: ExportBody,
) -> dict[str, Any]:
    folder_name = f"{datetime.utcnow().date()}-{uuid4()}-{user.id}"
    task = export_receipts.delay(params, user.id, body.export_types, folder_name)
    return {"export_id": task.id}


@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result
