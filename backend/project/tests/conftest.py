import random

import pytest
from app import crud
from app import models
from app.config import Settings
from app.config import get_settings
from app.db import TestAsyncSessionLocal
from app.db import create_test_tables
from app.db import get_db
from app.db import override_get_db
from app.db import test_sync_engine
from app.main import create_application
from app.mongodb import get_mongo_db
from app.mongodb import get_test_mongo_db
from app.utilities.core.auth import get_sudo
from app.utilities.core.auth import get_user
from app.utilities.core.auth import get_user_api_call_log
from app.utilities.core.auth import get_verified_user
from app.utilities.core.redis import cache
from app.utilities.core.user_api_call_log import api_calls_exceeded
from fastapi import Depends
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

# from pydantic_settings import BaseSettings


def get_settings_override():
    settings = get_settings()
    settings.TESTING = True
    settings.ID_UUID = False
    settings.DB_ASYNC_URL = settings.DB_TEST_ASYNC_URL
    settings.DB_SYNC_URL = settings.DB_TEST_SYNC_URL
    settings.REDIS_LOGIN_PREFIX = "test_login_attempts_user"
    settings.LOGIN_LOCKOUT_TIME = 5
    settings.MONGO_DB_DB = settings.MONGO_DB_TESTDB
    settings.STATIC_FOLDER = "/public-test"
    return settings


async def get_verified_user_override(db: AsyncSession = Depends(override_get_db)):
    user = await crud.user.get(db, 10)
    return user
    # return models.UserDB(
    #     id=10, email='testing@test.pytest', password='testing'
    # )


async def get_sudo_override():
    return models.UserDB(id=1, email="mock@gmail.com", sudo=True)


async def get_user_api_call_log_override(
    mongo: AsyncIOMotorClient = Depends(get_test_mongo_db),
    settings: Settings = Depends(get_settings_override),
):
    collection = mongo[settings.API_CALL_LOG_COLLECTION]
    no_authorization = await api_calls_exceeded(collection, 1, 10)
    if no_authorization:
        raise HTTPException(status_code=403, detail="request amount exceeded")
    return None


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def client():
    app = create_application(testing=True)
    app.mount("/public", StaticFiles(directory="public-test"), name="public-test")
    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_db] = db_session
    app.dependency_overrides[get_verified_user] = get_verified_user_override
    app.dependency_overrides[get_user] = get_verified_user_override
    app.dependency_overrides[get_sudo] = get_sudo_override
    app.dependency_overrides[get_user_api_call_log] = get_user_api_call_log_override
    app.dependency_overrides[get_mongo_db] = get_test_mongo_db
    create_test_tables(drop=True)
    cache().flushdb()
    with TestClient(app) as test_client:
        yield test_client


async def db_session():
    async with TestAsyncSessionLocal() as session:
        yield session
    await session.close()
