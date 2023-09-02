from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models

from .crudbase import CRUDBase


class CRUDRefreshToken(
    CRUDBase[
        models.RefreshTokenDB, models.RefreshTokenCreate, models.RefreshTokenUpdate
    ]
):
    async def get_by_token(self, db: AsyncSession, jti: str):
        """Retrieve refresh token by its JTI (JSON Token ID)."""
        stmt = select(models.RefreshTokenDB).where(models.RefreshTokenDB.jti == jti)
        result = await db.scalars(stmt)
        return result.one_or_none()

    async def get_by_user_id(self, db: AsyncSession, id: int | UUID):
        """Retrieve all refresh tokens by user ID."""
        stmt = select(models.RefreshTokenDB).where(models.RefreshTokenDB.user_id == id)
        result = await db.scalars(stmt)
        return result.all()

    async def revoke(self, db: AsyncSession, id: int | UUID):
        """Revoke refresh tokens by user ID."""
        tokens = await self.get_by_user_id(db, id)
        for token in tokens:
            token.consumed = True
        await db.commit()


refresh_token = CRUDRefreshToken(models.RefreshTokenDB)
