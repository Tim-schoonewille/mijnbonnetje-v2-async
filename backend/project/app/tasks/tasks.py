import asyncio
from datetime import datetime, date, time
from pathlib import Path

from app.config import settings
from app.tasks.celery import celery_app
from app.utilities.core.subscription import update_subscription_active_status


@celery_app.task
def task_update_subscription_active_status() -> None:
    asyncio.run(update_subscription_active_status())
    return None


@celery_app.task
def task_mock_user_activities() -> None:
    async def mock_user_activities():
        from app.utilities.core.db import (
            read_all_mock_users,
            create_mock_login_records,
            create_mock_refresh_token_records,
        )
        from app.db import AsyncSessionLocal, async_engine

        async with AsyncSessionLocal() as db:
            all_mock_users = await read_all_mock_users(db)
            await create_mock_login_records(db, all_mock_users[1:])
            await create_mock_refresh_token_records(db, all_mock_users[1:])
        await async_engine.dispose()

    asyncio.run(mock_user_activities())
    return


@celery_app.task
def task_log_traffic() -> None:
    from app.crud import mongo_crud
    from app.mongodb import database as mongodb

    today = date.today()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)
    filter_ = {
        "request_date": {
            "$gte": start_of_day,
            "$lte": end_of_day,
        }
    }
    api_traffic = asyncio.run(
        mongo_crud.read_mongo_collection(
            mongodb=mongodb, collection=settings.API_TRAFFIC_COLLECTION, filter_=filter_
        )
    )
    traffic_log_path = Path("./reports/traffic_logs/")
    with open(f"{traffic_log_path}/{today}.txt", "w") as f:
        f.write(str(api_traffic))
