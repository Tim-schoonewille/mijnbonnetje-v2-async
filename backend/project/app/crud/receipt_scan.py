from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDReceiptScan(
    CRUDBase[models.ReceiptScanDB, models.ReceiptScanCreate, models.ReceiptScanUpdate]
):
    pass


receipt_scan = CRUDReceiptScan(models.ReceiptScanDB)
