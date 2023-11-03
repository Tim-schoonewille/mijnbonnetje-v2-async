import asyncio
import json
import pickle
import os
import time
from datetime import datetime, date
from pathlib import Path
from typing import Any
from app import models, crud

from app.config import settings
from app.tasks.celery import celery_app
from app.utilities.core.subscription import update_subscription_active_status
from app.db import AsyncSessionLocal
from app.utilities.export.utilities import get_and_export_receipts


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


@celery_app.task
def task_update_proxy_list_to_cache() -> None:
    async def update_proxy_list_to_cache() -> None:
        from app.tasks.utils.proxy_scanner import ProxyScanner
        from redis import asyncio as aioredis

        # endpoint = "https://ipv4.icanhazip.com"
        endpoint = "https://api.ipify.org?format=json"
        proxy_scanner = ProxyScanner("./utils/proxies.txt", endpoint)
        await proxy_scanner.test_all_proxies()
        redis = aioredis.from_url(f"redis://:{settings.REDIS_PASSWORD}@localhost:6379")
        async with redis.client() as client:
            await client.set("proxies", pickle.dumps(proxy_scanner.working_proxies))

    # asyncio.run(update_proxy_list_to_cache())
    print(os.getcwd())
    return


@celery_app.task
def export_receipts(
    params: dict[str, Any], user_id: int, export_types: list[str], folder_name: str
):
    asyncio.run(get_and_export_receipts(params, user_id, export_types, folder_name))

    return folder_name + ".zip"


@celery_app.task
def run_in_bg_test() -> None:
    time.sleep(10)
    print("Running in background or nay?")
    return None
