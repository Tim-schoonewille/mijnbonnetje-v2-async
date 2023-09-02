from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserCreate, UserDB, UserUpdateBase

from .crudbase import CRUDBase


class CRUDUser(CRUDBase[UserDB, UserCreate, UserUpdateBase]):
    async def get_by_email(self, db: AsyncSession, email: str):
        """Retrieve a user by email."""
        stmt = select(UserDB).where(UserDB.email == email)
        result = await db.scalars(stmt)
        return result.one_or_none()

    async def verify_email(self, db: AsyncSession, email: str):
        """Mark a user's email as verified."""
        user = await self.get_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        user.verified = True
        await db.commit()

    async def sudo(self, db: AsyncSession, id: int | UUID, action: str):
        """Modify user's sudo privileges."""
        user = await self.get(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        if action == "assign":
            user.sudo = True
        elif action == "revoke":
            user.sudo = False
        else:
            raise HTTPException(status_code=400, detail="INVALID_ACTION")
        await db.commit()

    async def disable(self, db: AsyncSession, id: int | UUID):
        """Disable user account."""
        user = await self.get(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        user.active = False
        await db.commit()

    async def enable(self, db: AsyncSession, id: int | UUID):
        """Enable user account."""
        user = await self.get(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        user.active = True
        await db.commit()

    async def update_password(
        self,
        db: AsyncSession,
        user: UserDB,
        password: str,
    ):
        """Update user's password."""
        await db.run_sync(lambda sess: user)
        user.password = password
        await db.commit()


user = CRUDUser(UserDB)
