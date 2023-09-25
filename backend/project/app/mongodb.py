from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app.config import get_settings

settings = get_settings()


client = AsyncIOMotorClient(settings.MONGO_DB_URL)
database = client[settings.MONGO_DB_DB]


async def get_mongo_db():
    yield database


async def get_mongo_db_generator():
    async with AsyncIOMotorClient(settings.MONGO_DB_URL) as client:
        yield client[settings.MONGO_DB_DB]


async def get_test_mongo_db():
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    database = client[settings.MONGO_DB_TESTDB]
    yield database


async def generator_test_mongo():
    async with AsyncIOMotorClient(settings.MONGO_DB_URL) as client:
        yield client[settings.MONGO_DB_TESTDB]


async def drop_test_mongodb_database():
    client = AsyncIOMotorClient(settings.MONGO_DB_URL)
    database = client[settings.MONGO_DB_TESTDB]
    await database.client.drop_database(settings.MONGO_DB_TESTDB)
    