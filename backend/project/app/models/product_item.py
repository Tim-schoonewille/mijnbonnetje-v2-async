from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict
from pydantic import Field
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import ReceiptEntryIDFieldDBMixin
from app.models.base import StoreIDFieldDBMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import ReceiptEntryDB
    from app.models import StoreDB


class ProductItemDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    ReceiptEntryIDFieldDBMixin,
    StoreIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "product_items"
    purchase_date: Mapped[Optional[str]]
    name: Mapped[str]
    price: Mapped[Optional[float]]
    quantity: Mapped[Optional[int]] = mapped_column(default=1)

    user: Mapped["UserDB"] = relationship(back_populates="product_items")
    receipt_entry: Mapped["ReceiptEntryDB"] = relationship(
        back_populates="product_items"
    )
    store: Mapped["StoreDB"] = relationship(back_populates="product_items")


class ProductItem(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    TimeStampSchemaMixin,
):
    receipt_entry_id: int | UUID
    store_id: int | UUID | None = None
    purchase_date: str | None = None
    name: str
    price: float | None
    quantity: int | None
    model_config = ConfigDict(from_attributes=True)


class ProductItemCreate(CamelBase):
    receipt_entry_id: int | UUID
    store_id: int | UUID | None = None
    purchase_date: str | None = None
    name: str
    price: float | None = Field(default=1)
    quantity: int | None = Field(default=1)


class ProductItemUpdate(CamelBase):
    receipt_entry_id: int | UUID | None = None
    store_id: int | UUID | None = None
    purchase_date: str | None = None
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
