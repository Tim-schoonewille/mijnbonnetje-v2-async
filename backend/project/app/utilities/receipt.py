import io
import os
from uuid import uuid4, UUID

import aiofiles  # type: ignore
import pytesseract as pt  # type: ignore
from fastapi import UploadFile, HTTPException
from PIL import Image  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models
from app.config import settings


async def write_receipt_file_to_disk(
    file: UploadFile, entry_id: int | UUID, folder: str
) -> str:
    """Take a FastAPI UploadFile object and checks for:
    - if the file has a filename and is valid
    - if the filesize is within set boundries.
    - if the file type is allowed.

    It saves it to the folder set in settings
    Returns the file path in string format
    """
    if file is None or file.filename is None:
        HTTPException(status_code=400, detail="ERROR_IN_FILE")
    file_size = await calculate_file_size(file)
    if file_size > settings.MAX_FILE_SIZE * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail=f"FILE_TOO_LARGE_MAX_{settings.MAX_FILE_SIZE}MB"
        )

    if not await check_file_type(file):
        raise HTTPException(status_code=400, detail="INVALID_FILE_TYPE")

    FOLDER_TO_SAVE_PATH = os.path.join("." + folder, str(entry_id))
    os.makedirs(FOLDER_TO_SAVE_PATH, exist_ok=True)
    file_name_without_spaces = file.filename.replace(" ", "")  # type: ignore
    file_name_on_disk = str(uuid4()) + file_name_without_spaces
    file_path = os.path.join(FOLDER_TO_SAVE_PATH, file_name_on_disk)
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())
    return file_path


async def calculate_file_size(file: UploadFile) -> int:
    """Returns the file size"""
    file.file.seek(0, 2)
    file_size = file.file.tell()
    await file.seek(0)
    return file_size


async def check_file_type(file: UploadFile) -> bool:
    """Is file type allowed. Allowed types in settings.ALLOWED_FILE_TYPES"""
    return file.content_type in settings.ALLOWED_FILE_TYPES


async def handle_receipt_file(
    db: AsyncSession,
    user: models.UserDB,
    receipt_file: UploadFile,
    entry_id: int | UUID,
    folder: str,
) -> models.ReceiptFileDB:
    file_path_on_disk = await write_receipt_file_to_disk(receipt_file, entry_id, folder)
    input_schema = models.ReceiptFileCreate(
        receipt_entry_id=entry_id,
        file_name=str(receipt_file.filename),
        file_path=file_path_on_disk,
        file_type=str(receipt_file.content_type),
        file_size=await calculate_file_size(receipt_file),
    )
    return await crud.receipt_file.create(db, input_schema, user)


async def handle_receipt_scan(
    db: AsyncSession,
    user: models.UserDB,
    receipt_entry_id: int | UUID,
    receipt_file_id: int | UUID,
    receipt_file_path: str,
) -> models.ReceiptScanDB:
    if not os.path.exists(receipt_file_path):
        raise HTTPException(status_code=404, detail="INVALID_FILE_PATH")
    receipt_scan = await scan_receipt(receipt_file_path)
    receipt_scan_schema = models.ReceiptScanCreate(
        receipt_entry_id=receipt_entry_id,
        receipt_file_id=receipt_file_id,
        scan=receipt_scan,
    )
    return await crud.receipt_scan.create(db, receipt_scan_schema, user)


async def scan_receipt(path_to_img: str) -> str:
    async with aiofiles.open(path_to_img, "rb") as f:
        img_data = await f.read()

    img = Image.open(io.BytesIO(img_data))
    img = img.convert("L")
    extraction = pt.image_to_string(img)
    return extraction


async def refresh_receipt_entry(
    db: AsyncSession, entry: models.ReceiptEntryDB
) -> models.ReceiptEntryDB:
    await db.refresh(
        entry, ["receipt_files", "receipt_scans", "store", "product_items"]
    )
    return entry
