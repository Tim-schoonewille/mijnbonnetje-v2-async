from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile

from app import crud
from app import models
from app.config import settings
from app.utilities.receipt import handle_receipt_file
from app.utilities.receipt import handle_receipt_scan
from app.utilities.receipt import refresh_receipt_entry
from app.utilities.receipt import parse_receipt_with_openai
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import GetSettings
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser


router = APIRouter(prefix=settings.URL_PREFIX + "/receipt", tags=["receipt"])


@router.post("/", response_model=models.Receipt, status_code=201)
async def create_full_receipt(
    *,
    exclude_ai_scan: bool = True,
    user: VerifiedUser,
    file: UploadFile,
    settings: GetSettings,
    db: GetDB,
):
    receipt_entry = await crud.receipt_entry.create(
        db=db, schema_in=models.ReceiptEntryCreate(), user=user
    )
    receipt_file = await handle_receipt_file(
        db=db,
        user=user,
        receipt_file=file,
        entry_id=receipt_entry.id,
        folder=settings.STATIC_FOLDER,
    )
    receipt_scan = await handle_receipt_scan(
        db=db,
        user=user,
        receipt_entry_id=receipt_file.receipt_entry_id,
        receipt_file_id=receipt_file.id,
        receipt_file_path=receipt_file.file_path,
    )
    receipt = await refresh_receipt_entry(db, receipt_entry)
    if exclude_ai_scan is False:
        items = parse_receipt_with_openai(receipt_scan.scan)
        print('[+] FROM THE ROUTER::::::')
        print(items)
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


@router.get('/{receipt_id}', response_model=models.Receipt)
async def read_specific_full_receipt(
    receipt_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """Retreive a full receipt from database with:
    entry, file, scan, store?, product_items?

    Raises:\n
        404: {detail:"RECEIPT_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED"}
    """
    receipt = await crud.receipt_entry.get(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="RECEIPT_NOT_FOUND")
    if receipt.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return await refresh_receipt_entry(db, receipt)


@router.delete('/{receipt_id}')
async def delete_specific_full_receipt(
    receipt_id: int | UUID,
    user: VerifiedUser,
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

    await crud.receipt_entry.remove(db, receipt)
    return dict(message="RECEIPT_DELETED")
