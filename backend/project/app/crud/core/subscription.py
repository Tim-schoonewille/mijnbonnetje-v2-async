from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDSubscription(
    CRUDBase[
        models.SubscriptionDB, models.SubscriptionCreate, models.SubscriptionUpdate
    ]
):
    pass


subscription = CRUDSubscription(models.SubscriptionDB)
