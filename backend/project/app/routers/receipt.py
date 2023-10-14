import pickle
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile

from app import crud
from app import models
from app.config import settings
from app.config import CachedItemPrefix
from app.utilities.receipt import handle_receipt_file
from app.utilities.receipt import handle_receipt_scan
from app.utilities.receipt import refresh_receipt_entry
from app.utilities.receipt import handle_receipt_ocr
from app.utilities.core.dependencies import GetCache
from app.utilities.core.dependencies import GetAsyncCache
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import GetSettings
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.dependencies import UserLimitedAPICalls
from app.utilities.core.redis import get_cached_item
from app.utilities.store import entries_related_to_store, remove_user_from_store


router = APIRouter(prefix=settings.URL_PREFIX + "/receipt", tags=["receipt"])


@router.post("/", response_model=models.Receipt, status_code=201)
async def create_full_receipt(
    *,
    include_external_ocr: bool = False,
    user: VerifiedUser,
    file: UploadFile,
    settings: GetSettings,
    db: GetDB,
    cache: GetAsyncCache,
):
    """Creates a full receipt.
    Intended for frontend to create a receipt from file.
    Handles:\n
        Creating an entry\n
        Uploading a file\n
        ocr scan\n
        update the entry with store and product items\n

    Raises:\n
        400: {detail: "EXTERNAL_API_LIMIT_EXCEEDED}\n
        400: {detail: "ERROR_IN_FILE"}\n
        400: {detail: "FILE_TOO_LARGE_MAX_X_MB"}\n
        400: {detail: "INVALID_FILE_TYPE}\n
    """
    print('[+] DEBUG_RECEIPT:: Creating enry...')
    receipt_entry = await crud.receipt_entry.create(
        db=db, schema_in=models.ReceiptEntryCreate(), user=user
    )
    print('[+] DEBUG_RECEIPT :: CREATING RECEIPT FILE')
    receipt_file = await handle_receipt_file(
        db=db,
        user=user,
        receipt_file=file,
        entry_id=receipt_entry.id,
        folder=settings.STATIC_FOLDER,
    )
    print('[+] DEBUG_RECEIPT :: Scanning File')
    receipt_scan = await handle_receipt_scan(
        db=db,
        user=user,
        receipt_entry_id=receipt_file.receipt_entry_id,
        receipt_file_id=receipt_file.id,
        receipt_file_path=receipt_file.file_path,
    )
    print('[+] DEBUG_RECEIPT :: HANDLE EXTERNAL OCR')
    receipt = await handle_receipt_ocr(
        db=db,
        user=user,
        entry=receipt_entry,
        scan=receipt_scan,
        file_path=receipt_file.file_path,
        external_ocr=include_external_ocr,
        testing=settings.TESTING,
        cache=cache,
    )
    return receipt


@router.get("/", response_model=list[models.Receipt])
async def read_multiple_receipts(
    user: VerifiedUser,
    params: ParametersDepends,
    db: GetDB,
):
    """Read multiple receipts. Requires verified user token.
    Parameter filters available
    """
    receipts = await crud.receipt_entry.get_multi(db, user, **params)
    return [await refresh_receipt_entry(db, entry) for entry in receipts]


@router.get("/{receipt_id}", response_model=models.Receipt)
async def read_specific_full_receipt(
    receipt_id: int | UUID,
    user: VerifiedUser,
    cache: GetAsyncCache,
    db: GetDB,
):
    """Retreive a full receipt from database with:
    entry, file, scan, store?, product_items?

    Raises:\n
        404: {detail:"RECEIPT_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED"}
    """
    cached_item = await get_cached_item(
        cache, CachedItemPrefix.RECEIPT, receipt_id, user.id
    )
    if cached_item:
        print('Getting from cache')
        return cached_item

    receipt = await crud.receipt_entry.get(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="RECEIPT_NOT_FOUND")
    if receipt.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")

    full_receipt = await refresh_receipt_entry(db, receipt)
    await cache.set(
        name=f'{CachedItemPrefix.RECEIPT}{receipt_id}',
        value=pickle.dumps(full_receipt),
        ex=settings.CACHE_EXPIRATION_TIME,
    )
    return full_receipt


@router.delete("/{receipt_id}")
async def delete_specific_full_receipt(
    receipt_id: int | UUID,
    user: VerifiedUser,
    cache: GetAsyncCache,
    db: GetDB,
):
    """Delete a full receipt from database with:

    Raises:\n
        404: {detail:"RECEIPT_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED"}
    """
    receipt = await crud.receipt_entry.get(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="RECEIPT_NOT_FOUND")
    if receipt.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    await refresh_receipt_entry(db, receipt)

    entries_related = await entries_related_to_store(db, user, receipt.store_id)
    print('ENTRIES RELATED::: ', entries_related)
    if not entries_related:
        print('::: HAS NO ENTRIES RELATED')
        await remove_user_from_store(db, cache, user, receipt.store_id)

    await cache.delete(f'{CachedItemPrefix.RECEIPT}{receipt_id}')
    await cache.delete(f'{CachedItemPrefix.STORES}{user.id}')
    await crud.receipt_entry.remove(db, receipt)
    return dict(message="RECEIPT_DELETED")
