# from datetime import date
from datetime import datetime

# from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from app import crud
from app import models
from app.config import settings

from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import SudoUser
from app.utilities.core.dependencies import VerifiedUser

from app.utilities.core.log import log_traffic
from app.utilities.core.subscription import generate_payment_api

# from app.utilities.core.subscription import get_subscriptions
from app.utilities.core.subscription import get_payment_pending_subscription


router = APIRouter(prefix=f"{settings.URL_PREFIX}/sub/payment", tags=["payment"])


@router.get("/", response_model=list[models.Payment])
@log_traffic()
async def read_all_payments(
    params: ParametersDepends,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """Return all payment history."""
    results = await crud.payment.get_multi(db, user, **params)
    return results


@router.post("/update")
@log_traffic()
async def update_payment(
    external_id: UUID,
    update: models.UpdatePayment,
    request: Request,
    db: GetDB,
):
    """
    Route to update a payment status.

    Raises:\n
        400: {detail: 'PAYMENT_COMPLETED_OR_EXPIRED}\n
        404: {detail: 'INVALID_PAYMENT_ID}
    """
    payment = await crud.payment.get_by_external_id(db, external_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="INVALID_PAYMENT_ID")

    if (
        payment.status == models.PaymentStatus.COMPLETED
        or payment.status == models.PaymentStatus.FAILED
    ):
        raise HTTPException(status_code=400, detail="PAYMENT_COMPLETED_OR_EXPIRED")

    update_schema = models.PaymentUpdate(
        payment_date=datetime.utcnow(), method=update.method, status=update.status
    )
    updated_payment = await crud.payment.update(db, update_schema, payment)
    subscription = await payment.awaitable_attrs.subscription
    subscription_update_schema = models.SubscriptionUpdate(active=True)
    if update.status == models.PaymentStatus.COMPLETED:
        # today = date.today()
        # if today > subscription.start_date:
        #     tier = await subscription.awaitable_attrs.tier
        #     subscription_update_schema.start_date = today
        #     subscription_update_schema.end_date = today + timedelta(days=tier.duration)

        await crud.subscription.update(
            db=db, update_schema=subscription_update_schema, object=subscription
        )
    return updated_payment


@router.get("/pending")
@log_traffic()
async def read_pending_payment(
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """Returns pending payment(s)"""
    subscriptions = await crud.subscription.get_multi(db, user)
    payment_pending = await get_payment_pending_subscription(list(subscriptions))
    return payment_pending


@router.get("/{payment_id}")
@log_traffic()
async def read_specific_payment(
    payment_id: int | UUID,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """
    Returns data from specific payment.

    Raises:\n
        404: {detail: 'PAYMENT_NOT_FOUND'}
    """
    payment = await crud.payment.get(db, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="PAYMENT_NOT_FOUND")
    return payment


@router.post("/", response_model=models.Payment, status_code=201)
@log_traffic()
async def create_payment(
    input_schema: models.PaymentCreateSchema,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """
    Create a new payment for a requested subscription.

    Raises:\n
        400: {detail: 'PAYMENT_ALREADY_FULFILLED}\n
        402: {detail: 'PAYMENT_PENDING}\n
        403: {detail: 'NO_SUB_OR_NOT_YOUR_SUB'}
    """
    subscription = await crud.subscription.get(db, input_schema.subscription_id)
    if subscription is None or subscription.user_id != user.id:
        raise HTTPException(status_code=403, detail="NO_SUB_OR_NOT_YOUR_SUB")

    subscription_payments = await subscription.awaitable_attrs.payments
    for payment in subscription_payments:
        if payment.status == models.PaymentStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="PAYMENT_ALREADY_FULFILLED")
        if payment.status == models.PaymentStatus.PENDING:
            raise HTTPException(status_code=402, detail="PAYMENT_PENDING")

    tier = await subscription.awaitable_attrs.tier
    external_id = await generate_payment_api()
    new_payment = models.PaymentCreate(  # type: ignore
        subscription_id=subscription.id,
        external_id=external_id,
        amount=tier.price,
    )
    new_payment_in_db = await crud.payment.create(db, new_payment, user)
    return new_payment_in_db


@router.delete("/{payment_id}")
@log_traffic()
async def delete_payment(
    payment_id: int,
    user: SudoUser,
    request: Request,
    db: GetDB,
):
    """
    Delete a payment (requires sudo)

    Raises:\n
        404: {detail: 'PAYMENT_NOT_FOUND'}
    """
    payment = await crud.payment.get(db, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="PAYMENT_NOT_FOUND")
    await crud.payment.remove(db, payment)
    return {"success": "Payment removed"}
