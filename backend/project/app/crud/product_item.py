from app.crud.core.crudbase import CRUDBase
from app import models


class CRUDProductItem(CRUDBase[
    models.ProductItemDB,
    models.ProductItemCreate,
    models.ProductItemUpdate
]):
    pass


product_item = CRUDProductItem(models.ProductItemDB)
