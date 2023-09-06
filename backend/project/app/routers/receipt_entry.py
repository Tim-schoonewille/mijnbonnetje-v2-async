from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException

from app import crud
from app import models
from app.config import settings
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser

router = APIRouter(
    prefix=settings.URL_PREFIX + "/receipt-entry", tags=["receipt-entry"]
)


@router.post("/", response_model=models.ReceiptEntry, status_code=201)
async def create_receipt_entry(
    schema: models.ReceiptEntryCreate, user: VerifiedUser, db: GetDB
):
    """Create new receipt entry
    Optional parameter: store_id (int | UUID)

    Raises:\n
        404: {detail:"STORE_NOT_FOUND" }
    """
    if schema.store_id:
        store = await crud.store.get(db, schema.store_id)
        if store is None:
            raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
        await store.awaitable_attrs.users
        if store and user not in store.users:
            store.users.append(user)
            await db.commit()
    new_receipt_entry = await crud.receipt_entry.create(db, schema, user)
    return new_receipt_entry


@router.get("/", response_model=list[models.ReceiptEntry])
async def read_multiple_receipt_entries(
    params: ParametersDepends,
    user: VerifiedUser,
    db: GetDB,
):
    """
    Retreive multiple receipt entries
    (requires verifiied user token, or sudo token for all)
    """
    return await crud.receipt_entry.get_multi(db, user, **params)


@router.get("/{receipt_entry_id}", response_model=models.ReceiptEntry)
async def read_specific_receipt_entry(
    receipt_entry_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """
    Retreive a specific receipt entry (requires verifieduser token)

    Raises:\n
        404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
        403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
    """
    receipt_entry_in_db = await crud.receipt_entry.get(db, receipt_entry_id)
    if receipt_entry_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_ENTRY_NOT_FOUND")
    if receipt_entry_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_ENTRY")
    return receipt_entry_in_db


@router.patch("/{receipt_entry_id}", response_model=models.ReceiptEntry)
async def update_receipt_entry(
    receipt_entry_id: int | UUID,
    update_schema: models.ReceiptEntryUpdate,
    user: VerifiedUser,
    db: GetDB,
):
    """
    update a specific receipt entry (requires verifieduser token)

    Raises:\n
        404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
        403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
        404: {detail="STORE_NOT_FOUND"}
    """
    receipt_entry_in_db = await crud.receipt_entry.get(db, receipt_entry_id)
    if receipt_entry_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_ENTRY_NOT_FOUND")
    if receipt_entry_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_ENTRY")
    if update_schema.store_id:
        store = await crud.store.get(db, update_schema.store_id)
        if store is None:
            raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
        await store.awaitable_attrs.users
        if user not in store.users:
            store.users.append(user)
            await db.commit()
    if not update_schema.store_id:
        store = await crud.store.get(db, receipt_entry_in_db.store_id)
        if store is None:
            raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
        await store.awaitable_attrs.users
        if user in store.users:
            store.users.remove(user)
            await db.commit()
    updated_receipt_entry = await crud.receipt_entry.update(
        db, update_schema, receipt_entry_in_db
    )
    return updated_receipt_entry


@router.delete("/{receipt_entry_id}")
async def delete_receipt_entry(
    receipt_entry_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """
    delete a specific receipt entry (requires verifieduser token)

    Raises:\n
        404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
        403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
    """
    receipt_entry_in_db = await crud.receipt_entry.get(db, receipt_entry_id)
    if receipt_entry_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_ENTRY_NOT_FOUND")
    if receipt_entry_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_ENTRY")
    await crud.receipt_entry.remove(db, receipt_entry_in_db)
    return dict(message="RECEIPT_ENTRY_DELETED")
