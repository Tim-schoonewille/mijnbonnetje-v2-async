from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDReceiptEntry(
    CRUDBase[
        models.ReceiptEntryDB, models.ReceiptEntryCreate, models.ReceiptEntryUpdate
    ]
):
    pass


receipt_entry = CRUDReceiptEntry(models.ReceiptEntryDB)
