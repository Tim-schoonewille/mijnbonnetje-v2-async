from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app import models
from app.mongodb import get_mongo_db
from app.crud.mongodb.mongo_crud import read_mongo_collection
from app.config import settings
from app.utilities.core.auth import get_user_api_call_log


router = APIRouter(prefix=f"{settings.URL_PREFIX}/test", tags=["test"])


@router.get("/api-call-log-limit")
async def mongo_request_limit_get(
    user: Annotated[models.UserDB, Depends(get_user_api_call_log)],
):
    """Test route te check wether the the amount of API requests is limited"""
    return {"hello": "world"}


@router.get("/get-collection")
async def read_collection(
    collection: str, mongodb: AsyncIOMotorClient = Depends(get_mongo_db)
):
    all_ = await read_mongo_collection(mongodb=mongodb, collection=collection)
    results = [models.ApiCallLog(**result) for result in all_]
    return results
