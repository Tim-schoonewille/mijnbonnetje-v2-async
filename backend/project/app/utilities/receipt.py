import httpx
import io
import json
import os
from uuid import uuid4, UUID

import aiofiles  # type: ignore
import openai
import pytesseract as pt  # type: ignore
from fastapi import UploadFile, HTTPException
from PIL import Image  # type: ignore
from PIL import ImageFilter
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models
from app.config import settings
from app.utilities.get_proxy import get_working_proxy
from app.utilities.store import add_store_to_user
from app.utilities.store import create_or_get_store_id
from app.utilities.product_item import create_product_entries


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
    print('[...] opening file')
    async with aiofiles.open(file_path, "wb") as f:
        print('[..] Writing to disk')
        await f.write(await file.read())
    print('[..] Write succeeded')
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
    print('[..] Writing to file')
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
    # img = img.filter(ImageFilter.SHARPEN)
    # img = img.convert("L")
    config = "--psm 1"
    extraction = pt.image_to_string(img, config=config)
    return extraction


async def refresh_receipt_entry(
    db: AsyncSession, entry: models.ReceiptEntryDB
) -> models.ReceiptEntryDB:
    await db.refresh(
        entry, ["receipt_files", "receipt_scans", "store", "product_items"]
    )
    return entry


def parse_receipt_with_openai(
    prompt_query: str,
    gpt_model: str = "gpt-3.5-turbo",
    max_tokens: int = 1000,
    temp: int = 0,
) -> dict:
    prompt_question_old = """
    can you parse this receipt scan and return to me the items in json format? I only want you to respond with json. No need to format it for my view, if you do that, I get alot clutter that I don't need. Try to get me the best possible JSON response as possible.  I want the json to look like this array of objects: \n
    { "name": "<name:string>", "price": <price:float>, "quantity": <quantity:integer> } 
    """
    prompt_question = """
    can you parse this receipt scan and return to me the items in json format? I only want you to respond with json. No need to format it for my view, if you do that, I get alot clutter that I don't need. Try to get me the best possible JSON response as possible. Also,if you can find the: Total Price of receipt, the store of the receipt, and the location of said store, I also want you to send that back to me.\n If you can't define the store with name an city, or not the total price, just leave it at null, but if possible, calculate the total price from the individual items that you have found.\nI want the json to look like this object: \n
    {"store": {"name": <name_of_store:string>, "city": <city_of_store:string>},
    "totalPrice": <total_price_as_on_the_receipt:float(number)>, "productItems":
    [array of objects:{ "name": "<name:string>", "price": <price:float>, "quantity": <quantity:integer (default: 1)> }] 
    """

    prompt = prompt_question + prompt_query
    openai.api_key = settings.OPENAI_API_KEY
    result = openai.Completion.create(
        model=gpt_model,
        prompt=prompt,
        # messages=[{'role': 'user', 'content': prompt}],
        max_tokens=max_tokens,
        temperature=temp,
    )
    print("OPENAI CALL RESULT:\n", result)
    try:
        items = json.loads(result["choices"][0]["text"])
        # items = json.loads(result['choices'][0]['message']['content'])

        # print('ITEM:::\n\n', items)
    except json.decoder.JSONDecodeError:
        return {}
    return items


async def handle_receipt_ocr(
    db: AsyncSession,
    user: models.UserDB,
    entry: models.ReceiptEntryDB,
    scan: models.ReceiptScanDB,
    file_path: str,
    cache: AsyncRedis,
    external_ocr: bool = False,
    testing: bool = False,
) -> models.ReceiptEntryDB:
    """handles the receipt parsing ocr"""
    if external_ocr:
        data = await get_external_ocr_data(file_path=file_path, cache=cache)
    else:
        data = await get_mock_ocr_data()

    await crud.receipt_scan.update(db, models.ReceiptScanUpdate(scan_json=data), scan)
    ocr_receipt = data["receipts"][0]
    purchase_date = ocr_receipt["date"]
    store_name = ocr_receipt["merchant_name"]
    total_amount = ocr_receipt["total"]
    product_items = ocr_receipt["items"]

    store_id = await create_or_get_store_id(db, user, store_name)
    if not testing:
        await add_store_to_user(db, user, store_id)
    entry_update_schema = models.ReceiptEntryUpdate(
        store_id=store_id,
        total_amount=int(total_amount * 100),
        purchase_date=str(purchase_date),
    )
    await create_product_entries(
        db=db,
        user=user,
        entry_id=entry.id,
        purchase_date=purchase_date,
        store_id=store_id,
        items=product_items,
        total_amount=total_amount
    )
    await crud.receipt_entry.update(db, entry_update_schema, entry)
    return await refresh_receipt_entry(db, entry)


async def get_external_ocr_data(file_path: str, cache: AsyncRedis) -> dict:
    """OCR receipt scan with external API"""
    endpoint = "https://ocr.asprise.com/api/v1/receipt"
    ip = await get_working_proxy(cache=cache)
    # ip = '138.199.23.163:8443'
    proxy = {
        'http://': f'http://{ip}',
        'https://': f'http://{ip}'
        }
    async with httpx.AsyncClient(proxies=proxy, verify=True) as client:
        async with aiofiles.open(file_path, mode="rb") as file:
            file_content = await file.read()
        files = {"file": file_content}
        response = await client.post(
            endpoint,
            data={
                "api_key": "TEST",
                "recognizer": "auto",
                "ref_no": "ocr_pyton_123",
            },
            files=files,
            timeout=20
        )
        data = response.json()
        print(data)
    if data["success"] is False:
        raise HTTPException(status_code=400, detail="EXTERNAL_API_LIMIT_EXCEEDED")
    return data


async def get_mock_ocr_data() -> dict:
    """Gets data from JSON file that is a replica from external API"""
    mock_json_data = "./data/triade_bon.json"
    with open(mock_json_data, "r") as f:
        data = json.load(f)
    return data
