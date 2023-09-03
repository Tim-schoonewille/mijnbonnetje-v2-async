from uuid import UUID


from fastapi import APIRouter, HTTPException, UploadFile

from app import crud, models
from app.config import settings
from app.utilities.receipt import handle_receipt_file
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser

router = APIRouter(prefix=settings.URL_PREFIX + '/receipt-file', tags=['receipt-file'])


@router.post('/')
async def create_receipt_file(
    user: VerifiedUser,
    file: UploadFile,
    entry_id: int | UUID,
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
    return await handle_receipt_file(db, user, file, entry_id)
