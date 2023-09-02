from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app.config import get_settings
from app.config import Settings
from app.config import settings


async def read_mongo_collection(
    collection: str,
    mongodb: AsyncIOMotorClient,
    filter_: dict | None = None,
):
    query = mongodb[collection].find(filter_)
    results = [result for result in await query.to_list(length=10000)]
    return results


async def delete_collection(
    settings: Settings = Depends(get_settings),
):
    async def inner_deletion(collection: str):
        client = AsyncIOMotorClient(settings.MONGO_DB_URL)
        db = client[settings.MONGO_DB_DB]
        coll = db[collection]
        await coll.delete_many({})
        return None

    return inner_deletion


def delete_api_call_logs() -> None:
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    db = client[settings.MONGO_DB_TESTDB]
    coll = db[settings.API_CALL_LOG_COLLECTION]
    coll.delete_many({})
    return None
