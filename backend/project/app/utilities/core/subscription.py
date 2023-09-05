from datetime import date
from datetime import timedelta
from uuid import UUID
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models


# from app.models.core import payment
# from app.models.core.subscription import (
#     SubscriptionCreateSchema,
#     SubscriptionDB,
#     SubscriptionCreate,
# )
# from app.models.core.tier import TierDB
# from app.models.core.user import UserDB


def calculate_end_date(start_date: date, tier_duration: int) -> date:
    """
    Calculate the end date of a subscription based on the provided start date
    and the duration of the subscription tier.
    """
    return start_date + timedelta(days=tier_duration)


async def read_multi_subs_with_tier_and_payments(
    db: AsyncSession,
    user: models.UserDB,
    params: dict,
):
    """
    Retrieve multiple subscriptions for a user from the database, along with
    their associated tier and payment information, based on specified paramd.
    """
    results = await crud.subscription.get_multi(db, user, **params)
    for result in results:
        await result.awaitable_attrs.tier
        await result.awaitable_attrs.payments
    return results


async def read_single_sub_with_tier_and_payments(
    db: AsyncSession,
    id: int | UUID,
):
    """
    Retrieve a single subscription from the database by ID, along with its
    associated tier and payment information.
    """
    subscription = await crud.subscription.get(db, id)
    if subscription is None:
        return None
    await subscription.awaitable_attrs.tier
    await subscription.awaitable_attrs.payments
    return subscription


async def create_new_sub(
    db: AsyncSession,
    sub_input_schema: models.SubscriptionCreateSchema,
    tier: models.TierDB,
    user: models.UserDB,
):
    """
    Create a new subscription in the database with the provided input schema,
    associated tier, and user details. Also creates a new payment entry.
    """
    end_date = calculate_end_date(sub_input_schema.start_date, tier.duration)
    new_subscription_schema = models.SubscriptionCreate(  # type: ignore
        start_date=sub_input_schema.start_date,
        end_date=end_date,
        tier_id=tier.id,
    )
    new_subscription = await crud.subscription.create(
        db=db, schema_in=new_subscription_schema, user=user
    )
    external_id = await generate_payment_api()
    new_payment = models.PaymentCreate(  # type: ignore
        subscription_id=new_subscription.id,
        external_id=external_id,
        amount=tier.price,
    )
    await crud.payment.create(db, new_payment, user)
    await new_subscription.awaitable_attrs.tier
    await new_subscription.awaitable_attrs.payments
    return new_subscription


async def get_subscriptions(user: models.UserDB) -> list[models.SubscriptionDB]:
    subscriptions = await user.awaitable_attrs.subscriptions
    return subscriptions


# async def get_active_subscription(
#     subscriptions: list[models.SubscriptionDB],
# ) -> models.SubscriptionDB | None:
#     for sub in subscriptions:
#         if sub.active:
#             return sub
#     return None


async def get_active_subscription(
    subscriptions: list[models.SubscriptionDB],
) -> models.SubscriptionDB | None:
    active_subscriptions = (sub for sub in subscriptions if sub.active)
    return next(active_subscriptions, None)


# async def get_payment_pending_subscription(
#     subscriptions: list[models.SubscriptionDB],
# ) -> models.SubscriptionDB | None:
#     today = date.today()
#     for sub in subscriptions:
#         if not sub.active and sub.end_date and sub.end_date > today:
#             return sub
#     return None


async def get_payment_pending_subscription(
    subscriptions: list[models.SubscriptionDB],
) -> models.SubscriptionDB | None:
    today = date.today()
    pending_subscriptions = (
        sub
        for sub in subscriptions
        if not sub.active and sub.end_date and sub.end_date > today
    )
    return next(pending_subscriptions, None)


async def update_subscription_active_status():
    from app.db import async_sessionmaker, async_engine

    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        stmt = select(models.SubscriptionDB)
        results = await session.execute(stmt)
        subscriptions = results.scalars().all()
        active_subscriptions = [sub for sub in subscriptions if sub.active]
        today = date.today()
        for active_sub in active_subscriptions:
            if today > active_sub.end_date:
                active_sub.active = False
                await session.commit()
        await async_engine.dispose()


async def generate_payment_api() -> UUID:
    return uuid4()
