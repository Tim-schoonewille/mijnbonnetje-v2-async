from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from app import crud
from app import models
from app.config import settings
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import SudoUser
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.subscription import create_new_sub
from app.utilities.core.subscription import get_active_subscription
from app.utilities.core.subscription import get_payment_pending_subscription
from app.utilities.core.subscription import get_subscriptions
from app.utilities.core.subscription import read_multi_subs_with_tier_and_payments
from app.utilities.core.subscription import read_single_sub_with_tier_and_payments

# from app.utilities.core.subscription import update_subscription_active_status
from app.utilities.core.log import log_traffic


router = APIRouter(
    prefix=f"{settings.URL_PREFIX}/sub/subscription", tags=["subscription"]
)


# @router.get("/update-subs")
# @log_traffic()
# async def update_subs(request: Request):
#     await update_subscription_active_status()
#     return {"lalala": "lalsadlfadsf"}


@router.get("/")
@log_traffic()
async def read_all_active_subscriptions(
    params: ParametersDepends,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """Return all subscriptions"""
    results = await read_multi_subs_with_tier_and_payments(
        db=db, user=user, params=params
    )
    return models.SubscriptionsWithTierAndMetaData(
        subscriptions=results, amount=len(results)
    )


@router.get("/{subscription_id}", response_model=models.SubscriptionWithTier)
@log_traffic()
async def read_specific_subscription(
    subscription_id: int | UUID,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """
    Returns a specific subscription based on ID

    Raises:\n
        403: {detail: 'NOT_YOUR_SUBSCRIPTION'}\n
        404: {detail: 'SUBSCRIPTION_NOT_FOUND'}
    """
    sub = await read_single_sub_with_tier_and_payments(db=db, id=subscription_id)
    if sub is None:
        raise HTTPException(status_code=404, detail="SUBSCRIPTION_NOT_FOUND")
    if sub.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_SUBSCRIPTION")

    return sub


@router.post("/", response_model=models.SubscriptionWithTier, status_code=201)
@log_traffic()
async def create_new_subscription(
    input_schema: models.SubscriptionCreateSchema,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """
    Create a new subscription.

    Raises:\n
        402: {detail: "PAYMENT_PENDING_FOR_SUB"}\n
        404: {detail: "TIER_NOT_FOUND"}\n
        409: {detail: "ALREADY_SUBBED"}
    """
    tier = await crud.tier.get(db, id=input_schema.tier_id)
    if tier is None:
        raise HTTPException(status_code=404, detail="TIER_NOT_FOUND")

    user_subscriptions = await get_subscriptions(user)
    active_subscription = await get_active_subscription(user_subscriptions)
    if active_subscription:
        raise HTTPException(status_code=409, detail="ALREADY_SUBBED")

    pending_subs = await get_payment_pending_subscription(user_subscriptions)
    if pending_subs:
        raise HTTPException(status_code=402, detail="PAYMENT_PENDING_FOR_SUB")

    return await create_new_sub(
        db=db, sub_input_schema=input_schema, tier=tier, user=user
    )


@router.patch("/{subscription_id}", response_model=models.Subscription)
@log_traffic()
async def update_subscription(
    subscription_id: int | UUID,
    update_schema: models.SubscriptionUpdate,
    user: SudoUser,
    request: Request,
    db: GetDB,
):
    """
    Update subscription (requires sudo)

    Raises:\n
        403: {detail: "NOT_YOUR_SUBSCRIPTION"}\n
        404: {detail: "SUBSCRIPTION_NOT_FOUND"}\n
    """
    subscription_in_db = await crud.subscription.get(db, subscription_id)
    if subscription_in_db is None:
        raise HTTPException(status_code=404, detail="SUBSCRIPTION_NOT_FOUND")
    updated_subscription = await crud.subscription.update(
        db=db, update_schema=update_schema, object=subscription_in_db
    )
    return updated_subscription


@router.delete("/{subscription_id}")
@log_traffic()
async def delete_subscription(
    subscription_id: int | UUID,
    user: SudoUser,
    request: Request,
    db: GetDB,
):
    """
    Delete subscription (requires sudo)

    Raises:\n
        404: {detail: "SUBSCRIPTION_NOT_FOUND"}\n
    """
    subscription = await crud.subscription.get(db, subscription_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="SUBSCRIPTION_NOT_FOUND")
    await crud.subscription.remove(db, subscription)
    return {"message": "Subscription deleted"}
