from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDStore(
    CRUDBase[
        models.StoreDB,
        models.StoreCreate,
        models.StoreUpdate,
    ]
):
    async def search(self, db: AsyncSession, user: models.UserDB, q: str):
        """Find a store in DB"""
        if q is None:
            return []
        all_stores = await self.get_multi(db, user)
        result = [
            store
            for store in all_stores
            if (len(q) == 1 and store.name.lower().startswith(q.lower()))
            or (len(q) > 1 and q.lower() in store.name.lower())
        ]
        return result


store = CRUDStore(models.StoreDB)
