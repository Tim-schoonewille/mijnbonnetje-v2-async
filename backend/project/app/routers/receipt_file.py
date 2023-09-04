import os
from uuid import UUID


from fastapi import APIRouter, HTTPException, UploadFile

from app import crud, models
from app.config import settings
from app.utilities.receipt import handle_receipt_file
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.dependencies import GetSettings

router = APIRouter(prefix=settings.URL_PREFIX + '/receipt-file', tags=['receipt-file'])


@router.post('/', response_model=models.ReceiptFile, status_code=201)
async def create_receipt_file(
    user: VerifiedUser,
    file: UploadFile,
    entry_id: int | UUID,
    settings: GetSettings,
    db: GetDB,
):
    """
    Upload a receipt to server.

    Raises:\n
        400: {detail: "ERROR_IN_FILE"}\n
        400: {detail: "FILE_TOO_LARGE_MAX_X_MB"}\n
        400: {detail: "INVALID_FILE_TYPE}\n

    """
    receipt_entry_in_db = await crud.receipt_entry.get(db, entry_id)
    if receipt_entry_in_db is None:
        raise HTTPException(status_code=404, detail="ENTRY_NOT_FOUND")
    if receipt_entry_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="NOT_YOUR_ENTRY")
    return await handle_receipt_file(db, user, file, entry_id, settings.STATIC_FOLDER)


@router.get('/', response_model=list[models.ReceiptFile])
async def read_multiple_receipt_files(
    user: VerifiedUser,
    params: ParametersDepends,
    db: GetDB,
):
    """ Return multiple receipt files, depending on given parameters
    Requires verified user token
    """
    return await crud.receipt_file.get_multi(db, user, **params)


@router.get('/{receipt_file_id}', response_model=models.ReceiptFile)
async def read_specific_receipt_file(
    receipt_file_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """ Returns specific receipt file from database, requires verified user token

        Raises:\n
            403: {detail: "NOT_YOUR_RECEIPT_FILE"}\n
            404: {detail: "RECEIPT_FILE_NOT_FOUND"}\n
    """
    receipt_file_in_db = await crud.receipt_file.get(db, receipt_file_id)
    if receipt_file_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_FILE_NOT_FOUND")
    if receipt_file_in_db.user_id != user.id and not user.sudo:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_FILE")
    return receipt_file_in_db


@router.delete('/{receipt_file_id}', response_model=dict[str, str])
async def delete_receipt_file(
    receipt_file_id: int | UUID,
    user: VerifiedUser,
    settings: GetSettings,
    db: GetDB,
):
    """ deeletes a specific receipt file from database, requires verified user token

        Raises:\n
            403: {detail: "NOT_YOUR_RECEIPT_FILE"}\n
            404: {detail: "RECEIPT_FILE_NOT_FOUND"}\n
            404: {detail: "RECEIPT_IMAGE_NOT_FOUND"}\n
    """
    receipt_file_in_db = await crud.receipt_file.get(db, receipt_file_id)
    if receipt_file_in_db is None:
        raise HTTPException(status_code=404, detail="RECEIPT_FILE_NOT_FOUND")
    if receipt_file_in_db.user_id != user.id and not user.sudo:
        raise HTTPException(status_code=403, detail="NOT_YOUR_RECEIPT_FILE")
    if not os.path.exists(receipt_file_in_db.file_path):
        raise HTTPException(status_code=404, detail="RECEIPT_IMAGE_NOT_FOUND")
    os.remove(receipt_file_in_db.file_path)
    return dict(message="RECEIPT_FILE_DELETED")
