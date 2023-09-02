from datetime import datetime
from datetime import timedelta
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app import models
from app.config import settings
from app.utilities.core import subscription as util_subscription


FUTURE = 0
today = str(datetime.utcnow().date() + timedelta(days=FUTURE))


async def get_user_api_call_log(
    collection: AsyncIOMotorClient, user_id: int | UUID
) -> dict:
    user_request_log = await collection.find_one({"user_id": user_id})
    return user_request_log


async def create_user_api_call_log(
    collection: AsyncIOMotorClient, user_id: int | UUID
) -> None:
    document = {
        "user_id": user_id,
        "created": datetime.utcnow(),
        "apicalls": [{"date": today, "amount": 0}],
    }
    await collection.insert_one(document)
    return None


async def create_api_call_log_for_today(
    collection: AsyncIOMotorClient, user_id: int | UUID, current_document: dict
) -> None:
    query = {"user_id": user_id}
    update = {"$addToSet": {"apicalls": {"date": today, "amount": 0}}}
    await collection.update_one(query, update, upsert=True)
    return None


async def update_amount_of_calls_today(
    collection: AsyncIOMotorClient, user_id: int | UUID, current_amount: int
) -> None:
    query = {"user_id": user_id, "apicalls.date": today}
    update = {"$set": {"apicalls.$.amount": current_amount + 1}}
    await collection.update_one(query, update)
    return None


def get_call_log_of_today(apicalls: list[dict]) -> dict | None:
    for apicall in apicalls:
        if apicall["date"] == today:
            return apicall
    return None


async def api_calls_exceeded(
    collection: AsyncIOMotorClient, user_id: int | UUID, limit: int
) -> bool:
    user_request_log = await get_user_api_call_log(
        collection=collection, user_id=user_id
    )
    if user_request_log is None:
        await create_user_api_call_log(collection, user_id)
        return False

    user_request_log_apicalls = user_request_log["apicalls"]
    request_today = get_call_log_of_today(apicalls=user_request_log_apicalls)

    if request_today is None:
        await create_api_call_log_for_today(collection, user_id, user_request_log)
        return False

    amount_of_requests_today = request_today["amount"]
    if amount_of_requests_today >= limit - 1:
        return True

    await update_amount_of_calls_today(
        collection=collection, user_id=user_id, current_amount=amount_of_requests_today
    )
    return False


async def get_api_call_limit(user: models.UserDB):
    user_subscription = await util_subscription.get_active_subscription(
        subscriptions=await util_subscription.get_subscriptions(user)
    )
    if user_subscription and user_subscription.active:
        tier = await user_subscription.awaitable_attrs.tier
        return tier.api_call_limit
    else:
        return settings.DEFAULT_API_CALL_LIMIT
