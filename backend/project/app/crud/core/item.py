from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDItem(CRUDBase[models.ItemDB, models.ItemCreate, models.ItemUpdate]):
    pass


item = CRUDItem(models.ItemDB)
