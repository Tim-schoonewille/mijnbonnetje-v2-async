from datetime import datetime
from typing import Annotated
from typing import Any
from typing import Optional
from uuid import uuid4
from uuid import UUID

# from humps import camelize
from pydantic import BaseModel
from pydantic import ConfigDict
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs

# from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedColumn
from sqlalchemy.types import JSON

from app.config import settings
from app.utilities.core.models import to_camel

if settings.ID_UUID is True:
    IDFieldDB = Mapped[UUID]
    OptionalIDFieldDB = Mapped[Optional[UUID]]
    id_field_db_default = uuid4
else:
    id_field_db_default = None  # type: ignore
    IDFieldDB = Mapped[int]  # type: ignore
    OptionalIDFieldDB = Mapped[Optional[int]]  # type: ignore


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


class IDFieldDBMixin:
    id: IDFieldDB = MappedColumn(primary_key=True, default=id_field_db_default)


class UserIDFieldDBMixin:
    user_id: IDFieldDB = MappedColumn(ForeignKey("users.id"))


class ReceiptEntryIDFieldDBMixin:
    receipt_entry_id: IDFieldDB = mapped_column(ForeignKey("receipt_entries.id"))


class ReceiptFileIDFieldDBMixin:
    receipt_file_id: IDFieldDB = mapped_column(ForeignKey("receipt_files.id"))


class SubscriptionIDFieldDBMixin:
    subscription_id: IDFieldDB = mapped_column(ForeignKey("subscriptions.id"))


class StoreIDFieldDBMixin:
    store_id: OptionalIDFieldDB = mapped_column(ForeignKey("stores.id"))


class TierIDFieldDBMixin:
    tier_id: IDFieldDB = mapped_column(ForeignKey("tiers.id"))


class TimeStampDBMixin:
    created_at: Mapped[datetime] = MappedColumn(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = MappedColumn(onupdate=func.now())


# pydantic base models
class CamelBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class IDFieldSchemaMixin(CamelBase):
    id: int | UUID
    # id: UUID


class UserIDFieldSchemaMixin:
    user_id: int | UUID
    # user_id: UUID


class SubscriptionIDFieldSchemaMixin:
    subscription_id: int | UUID
    # subscription_id: UUID


class TierIDFieldSchemaMixin:
    tier_id: int | UUID
    # tier_id: UUID


class TimeStampSchemaMixin(CamelBase):
    created_at: datetime
    updated_at: datetime | None = None
