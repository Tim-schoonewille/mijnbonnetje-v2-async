from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDTier(CRUDBase[models.TierDB, models.TierCreate, models.TierUpdate]):
    pass


tier = CRUDTier(models.TierDB)
