from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app import models
from app.config import get_settings
from app.models.base import Base

settings = get_settings()


async_engine = create_async_engine(
    settings.DB_ASYNC_URL,
    pool_pre_ping=True,
    echo=settings.DB_SQL_ECHO,
    # poolclass=NullPool
)


test_async_engine = create_async_engine(
    settings.DB_TEST_ASYNC_URL,
    pool_pre_ping=True,
    echo=settings.DB_SQL_ECHO,
    poolclass=NullPool,
)


sync_engine = create_engine(settings.DB_SYNC_URL, echo=settings.DB_SQL_ECHO)


test_sync_engine = create_engine(settings.DB_TEST_SYNC_URL, echo=settings.DB_SQL_ECHO)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, autoflush=True, future=True, expire_on_commit=False
)


TestAsyncSessionLocal = async_sessionmaker(
    bind=test_async_engine, autoflush=False, future=True, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        # await session.close()


async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        yield session


async def get_db_in_pytest():
    db = TestAsyncSessionLocal()
    return db


async def create_tables(drop: bool = False):
    from app.utilities.core.db import fill_db  # type: ignore

    async with async_engine.begin() as session:
        if drop:
            await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await fill_db(db)


def sync_create_tables(drop: bool = False):
    if drop:
        Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


def create_test_tables(drop: bool = False):
    if drop:
        Base.metadata.drop_all(bind=test_sync_engine)
    Base.metadata.create_all(bind=test_sync_engine)
    with Session(test_sync_engine) as session:
        new_user = models.UserDB(id=10, email='testing@test.pytest', password='testing')
        session.add(new_user)
        session.commit()
