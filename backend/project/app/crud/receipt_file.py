from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDReceiptFile(CRUDBase[
    models.ReceiptFileDB,
    models.ReceiptFileCreate,
    models.ReceiptFileUpdate
]):
    pass


receipt_file = CRUDReceiptFile(models.ReceiptFileDB)
