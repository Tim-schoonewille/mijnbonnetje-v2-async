from datetime import date
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict
from pydantic import Field
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models import Categories
from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import StoreIDFieldDBMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import ReceiptFileDB
    from app.models import StoreDB


class ReceiptEntryDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    StoreIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "receipt_entries"
    purchase_date: Mapped[Optional[str]]
    total_amount: Mapped[int] = mapped_column(default=0)
    warranty: Mapped[int] = mapped_column(default=0)
    category: Mapped[Categories] = mapped_column(default=Categories.OTHER)

    user: Mapped["UserDB"] = relationship(back_populates="receipt_entries")
    store: Mapped[list["StoreDB"]] = relationship(back_populates="receipt_entries")
    receipt_files: Mapped[list['ReceiptFileDB']] = relationship(
        back_populates='receipt_entry'
    )


class ReceiptEntry(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    TimeStampSchemaMixin,
):
    store_id: int | UUID | None = None
    purchase_date: str
    total_amount: int | None = None
    warranty: int
    category: Categories
    model_config = ConfigDict(from_attributes=True)


class ReceiptEntryCreate(CamelBase):
    store_id: int | UUID | None = None
    purchase_date: str = Field(default_factory=lambda: str(date.today()))
    total_amount: int = Field(default=0)
    warranty: int = Field(default=0)
    category: Categories = Field(default=Categories.OTHER)


class ReceiptEntryUpdate(CamelBase):
    store_id: int | UUID | None = None
    purchase_date: date | None = None
    total_amount: int | None = None
    warranty: int | None = None
    category: Categories | None = None
