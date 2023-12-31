import pickle
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException

from app import crud
from app import models
from app.config import settings
from app.config import CachedItemPrefix
from app.utilities.core.redis import get_cached_item
from app.utilities.store import add_store_to_user
from app.utilities.store import remove_user_from_store
from app.utilities.store import entries_related_to_store
from app.utilities.core.dependencies import CountParameterDepends, GetAsyncCache, GetCache
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.dependencies import UserLimitedAPICalls

router = APIRouter(
    prefix=settings.URL_PREFIX + "/receipt-entry", tags=["receipt-entry"]
)


@router.post("/", response_model=models.ReceiptEntry, status_code=201)
async def create_receipt_entry(
    schema: models.ReceiptEntryCreate, user: UserLimitedAPICalls, db: GetDB
):
    """Create new receipt entry
    Optional parameter: store_id (int | UUID)

    Raises:\n
        404: {detail:"STORE_NOT_FOUND" }
    """
    if schema.store_id:
        await add_store_to_user(db, user, schema.store_id)
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


@router.get('/count')
async def count_receipt_entries(
    params: CountParameterDepends,
    user: VerifiedUser,
    db: GetDB,
):
    """
    Returns the amount of entries in DB.\n
    Can be filtered on a specific date in format: 'YYYY-MM-DD'.\n
    Custom filter can also be applied, but requires knowledge of the model.\n

    Raises:\n
        400: {detail: "DATE_FILTER_INVALID"}
    """
    result = await crud.receipt_entry.count(db=db, user_id=user.id, **params)
    return result


@router.get("/{receipt_entry_id}", response_model=models.ReceiptEntry)
async def read_specific_receipt_entry(
    receipt_entry_id: int | UUID,
    user: VerifiedUser,
    cache: GetAsyncCache,
    db: GetDB,
):
    """
    Retreive a specific receipt entry (requires verifieduser token)

    Raises:\n
        404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
        403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
    """
    cached_item = await get_cached_item(
        cache, CachedItemPrefix.RECEIPT, receipt_entry_id, user.id
    )
    if cached_item:
        return cached_item
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
    cache: GetAsyncCache,
    db: GetDB,
):
    """
    update a specific receipt entry (requires verifieduser token)

    Raises:\n
        400: {detail='ENTRY_NEEDS_STORE_ID'}
        404: {detail="RECEIPT_ENTRY_NOT_FOUND"}
        403: {detail="NOT_YOUR_RECEIPT_ENTRY"}
        404: {detail="STORE_NOT_FOUND"}
    """
    receipt_entry_in_db = await crud.receipt_entry.get(db, receipt_entry_id)
    if receipt_entry_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_ENTRY_NOT_FOUND")
    if receipt_entry_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_ENTRY")

    print('store id: ', update_schema.store_id)
    if update_schema.store_id and update_schema.store_id != 0:
        if receipt_entry_in_db.store_id:
            await add_store_to_user(db, cache, user, update_schema.store_id)
            entries_related = await entries_related_to_store(db, user, receipt_entry_in_db.store_id)
            if not entries_related:
                print('has no entries related')
                await remove_user_from_store(db, cache, user, receipt_entry_in_db.store_id)
    # if not update_schema.store_id and receipt_entry_in_db.store_id is not None:
    #     print('This action remvoved the store_id from entry...')
    #     raise HTTPException(status_code=400, detail='ENTRY_NEEDS_STORE_ID')

    updated_receipt_entry = await crud.receipt_entry.update(
        db, update_schema, receipt_entry_in_db
    )
    await cache.delete(f'{CachedItemPrefix.RECEIPT}{receipt_entry_id}')
    return updated_receipt_entry


@router.delete("/{receipt_entry_id}")
async def delete_receipt_entry(
    receipt_entry_id: int | UUID,
    user: VerifiedUser,
    cache: GetAsyncCache,
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
    if receipt_entry_in_db.store_id:
        print('has store id')
        has_entries_related_to_store = await entries_related_to_store(
            db, user, receipt_entry_in_db.store_id
        )
        if not has_entries_related_to_store:
            await remove_user_from_store(db, cache, user, receipt_entry_in_db.store_id)
    await cache.delete(f'{CachedItemPrefix.RECEIPT}{receipt_entry_id}')
    await crud.receipt_entry.remove(db, receipt_entry_in_db)
    return dict(message="RECEIPT_ENTRY_DELETED")
