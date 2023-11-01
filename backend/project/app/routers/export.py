from datetime import datetime
import json
from typing import Any
from icecream import ic
from fastapi import APIRouter

from celery.result import AsyncResult

from app import crud, models
from app.tasks.tasks import export_receipts_to_json, run_in_bg_test
from app.tasks.celery import celery_app

from app.utilities.core.dependencies import GetDB, ParametersDepends, VerifiedUser
from app.utilities.receipt import refresh_receipt_entry


router = APIRouter(prefix="/export", tags=["export"])


@router.get("/")
async def get_export(
    user: VerifiedUser,
    params: ParametersDepends,
    db: GetDB,
):
    receipts = await crud.receipt_entry.get_multi(db, user, **params)
    full_receipts = [await refresh_receipt_entry(db, receipt) for receipt in receipts]
    validated_receipts = [
        models.Receipt(**receipt.__dict__).model_dump_json()
        for receipt in full_receipts
    ]
    bg_task = export_receipts_to_json.delay(validated_receipts, user.id)
    ic(bg_task)
    ic(bg_task.ready())
    ic(bg_task.id)
    return {'export_id': bg_task.id}


@router.get('/status/{task_id}')
def get_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result,
    }
    return result

