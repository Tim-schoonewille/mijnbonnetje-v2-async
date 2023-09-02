from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud.core.crudbase import CRUDBase


class CRUDPayment(
    CRUDBase[models.PaymentDB, models.PaymentCreate, models.PaymentUpdate]
):
    async def get_by_external_id(self, db: AsyncSession, id: UUID):
        """Retrieve object by external ID."""
        stmt = select(models.PaymentDB).where(models.PaymentDB.external_id == id)
        result = await db.scalars(stmt)
        return result.one_or_none()


payment = CRUDPayment(models.PaymentDB)
