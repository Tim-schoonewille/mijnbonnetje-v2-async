from datetime import datetime
import os
from typing import Any
from uuid import uuid4
from app import crud, models
from app.db import AsyncSessionLocal
from app.utilities.export.receipt_exporter import ReceiptExporter


async def get_and_export_receipts(
    params: dict[str, Any],
    user_id: int,
    export_types: list[str],
    folder_name: str,
):
    async with AsyncSessionLocal() as session:
        if (user := await crud.user.get(session, user_id)) is None:
            return
        receipts = await crud.receipt_entry.get_multi(session, user, **params)
        for receipt in receipts:
            await session.refresh(receipt, ["store", "receipt_files"])
        receipts = [models.ReceiptForExport(**receipt.__dict__) for receipt in receipts]
        await session.close()

    exporter = ReceiptExporter(receipts=receipts, export_types=export_types)
    exporter.export()
    print(os.getcwd())
    print("dir: ", os.listdir("."))
    return None
