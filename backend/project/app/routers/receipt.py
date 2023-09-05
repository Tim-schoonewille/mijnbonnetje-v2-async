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
    await handle_receipt_scan(
        db=db,
        user=user,
        receipt_entry_id=receipt_file.receipt_entry_id,
        receipt_file_id=receipt_file.id,
        receipt_file_path=receipt_file.file_path,
    )
    receipt = await refresh_receipt_entry(db, receipt_entry)
    return receipt


@router.get('/', response_model=list[models.Receipt])
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
