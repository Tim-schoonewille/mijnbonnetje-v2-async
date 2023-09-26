from datetime import timedelta
from typing import Any
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.models.base import Base
from app.utilities.core.crud import convert_to_datetime


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """Initialize CRUDBase with a model."""
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Retrieve an object by ID."""
        try:
            object = await db.get(self.model, id)
        except DBAPIError:
            raise HTTPException(status_code=404, detail="NOT_FOUND")
        return object

    async def get_multi(
        self,
        db: AsyncSession,
        user: models.UserDB,
        skip: int = 0,
        limit: int = 1000,
        user_id: int | UUID | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        date_filter: str = "created_at",
        column_filter: str | None = None,
        column_filter_value: str | int | UUID | None = None,
    ) -> Sequence[ModelType]:
        """
        Retrieve objects with filters and pagination.

        Constructs a query using self.model and applies filtering conditions:
        - Date range if provided and date column exists.
        - User ID if user has elevated privileges.
        - User association if user has no elevated privileges.
        Applies pagination and returns retrieved objects.
        """
        stmt = select(self.model)
        try:
            date_filter_column = getattr(self.model, date_filter)
        except AttributeError:
            raise HTTPException(status_code=400, detail="DATE_FILTER_INVALID")
        if start_date and hasattr(self.model, date_filter):
            stmt = stmt.where(date_filter_column >= convert_to_datetime(start_date))
        if end_date and hasattr(self.model, date_filter):
            stmt = stmt.filter(date_filter_column <= convert_to_datetime(end_date))
        if column_filter and hasattr(self.model, column_filter):
            column_in_object = getattr(self.model, column_filter)
            stmt = stmt.filter(column_in_object == column_filter_value)
        if user.sudo and user_id:
            try:
                user_id_column = getattr(self.model, "user_id")
            except AttributeError:
                raise HTTPException(
                    status_code=400, detail="Table has no user_id column"
                )
            stmt = stmt.filter(user_id_column == user_id)
        if not user.sudo and hasattr(self.model, "user"):
            stmt = stmt.where(self.model.user == user)  # type: ignore
        stmt = stmt.order_by(self.model.id)  # type: ignore
        stmt = stmt.offset(skip).limit(limit)
        objects = await db.execute(stmt)
        return objects.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        schema_in: CreateSchemaType,
        user: models.UserDB | None = None,
    ) -> ModelType:
        """Create a new object."""
        new_object = self.model(**schema_in.model_dump())
        if user and hasattr(new_object, "user_id"):
            setattr(new_object, "user_id", user.id)
        db.add(new_object)
        await db.commit()
        await db.refresh(new_object)
        return new_object

    async def update(
        self, db: AsyncSession, update_schema: UpdateSchemaType, object: ModelType
    ) -> ModelType:
        """Update an existing object."""
        # object_to_json = jsonable_encoder(object.__dict__)
        object_to_json = object.__dict__
        # update_data = update_schema.dict(exclude_unset=True)
        update_data = update_schema.model_dump(exclude_unset=True)
        for field in object_to_json:
            if field in update_data:
                setattr(object, field, update_data[field])
        db.add(object)
        await db.commit()
        await db.refresh(object)
        return object

    async def remove(self, db: AsyncSession, object: ModelType) -> None:
        """Remove an object from the database."""
        await db.delete(object)
        await db.commit()
        return None

    async def count(
        self,
        db: AsyncSession,
        user_id: int | UUID,
        sudo: bool = False,
        start_date: str | None = None,
        end_date: str | None = None,
        date_filter: str = "created_at",
    ):
        """Counts total entries"""
        stmt = select(func.count(self.model.id))  # type: ignore
        try:
            date_filter_column = getattr(self.model, date_filter)
        except AttributeError:
            raise HTTPException(status_code=400, detail="DATE_FILTER_INVALID")

        if start_date and hasattr(self.model, date_filter):
            stmt = stmt.filter(date_filter_column > convert_to_datetime(start_date))
        if end_date and hasattr(self.model, date_filter):
            stmt = stmt.filter(date_filter_column < (convert_to_datetime(end_date) + timedelta(days=1)))

        if not sudo and hasattr(self.model, 'user_id'):
            stmt = stmt.filter(self.model.user_id == user_id)  # type: ignore

        result = await db.execute(stmt)
        return result.scalar()
