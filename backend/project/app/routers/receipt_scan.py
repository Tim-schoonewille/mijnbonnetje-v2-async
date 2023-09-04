from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException


from app import crud
from app import models
from app.config import settings
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.receipt import handle_receipt_scan

router = APIRouter(prefix=f"{settings.URL_PREFIX}/receipt-scan", tags=["receipt-scan"])


@router.post("/", response_model=models.ReceiptScan, status_code=201)
async def create_receipt_scan(
    user: VerifiedUser,
    receipt_file_id: int | UUID,
    db: GetDB,
):
    """Creates a new scan of a receipt file.
    Gets the file, parses it through an OCR image processor.
    Saves the scan to database.

    Raises:\n
        404: {detail: "RECEIPT_FILE_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED"}
        404: {detail: "INVALID_FILE_PATH"}

    """
    receipt_file_in_db = await crud.receipt_file.get(db, receipt_file_id)
    if receipt_file_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_FILE_NOT_FOUND")
    if receipt_file_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    receipt_file_path = receipt_file_in_db.file_path
    return await handle_receipt_scan(
        db=db,
        user=user,
        receipt_file_id=receipt_file_id,
        receipt_file_path=receipt_file_path,
    )


@router.get("", response_model=list[models.ReceiptScan])
async def read_multiple_receipt_scans(
    params: ParametersDepends,
    user: VerifiedUser,
    db: GetDB,
):
    """Read multiple receipt scans.
    With filter parameters.
    Requires verified user token.
    """
    return await crud.receipt_scan.get_multi(db, user, **params)


@router.get("/{receipt_scan_id}", response_model=models.ReceiptScan)
async def read_specific_receipt_scan(
    receipt_scan_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """Read specific receipt scan from database
    Checks for ownership in the file.

    Raises:
        404: {detail="RECEIPT_SCAN_NOT_FOUND}
        403: {detail="ACCESS_DENIED"}

    """
    receipt_scan_in_db = await crud.receipt_scan.get(db, receipt_scan_id)
    if receipt_scan_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_SCAN_NOT_FOUND")
    receipt_file = await receipt_scan_in_db.awaitable_attrs.receipt_file
    if receipt_file.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return receipt_scan_in_db


@router.delete("/{receipt_scan_id}", response_model=dict[str, str])
async def delete_receipt_scan(
    receipt_scan_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """delete specific receipt scan from database
    Checks for ownership in the file.

    Raises:
        404: {detail="RECEIPT_SCAN_NOT_FOUND}
        403: {detail="ACCESS_DENIED"}

    """
    receipt_scan_in_db = await crud.receipt_scan.get(db, receipt_scan_id)
    if receipt_scan_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_SCAN_NOT_FOUND")
    receipt_file = await receipt_scan_in_db.awaitable_attrs.receipt_file
    if receipt_file.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    await crud.receipt_scan.remove(db, receipt_scan_in_db)
    return dict(message="RECEIPT_SCAN_REMOVED")
