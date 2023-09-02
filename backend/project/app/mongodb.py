from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app.config import get_settings

settings = get_settings()


client = AsyncIOMotorClient(settings.MONGO_DB_URL)
database = client[settings.MONGO_DB_DB]


async def get_mongo_db():
    yield database


async def get_test_mongo_db():
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    database = client[settings.MONGO_DB_TESTDB]
    yield database
