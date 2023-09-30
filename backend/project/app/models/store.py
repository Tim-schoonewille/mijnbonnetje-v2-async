from typing import Optional
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


from app.models.base import Base, UserIDFieldSchemaMixin
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import ReceiptEntryDB
    from app.models import ReceiptEntry
    from app.models import ProductItemDB


# store_users_association_table = Table(
#     "stores_users",
#     Base.metadata,
#     Column("store_id", ForeignKey("stores.id"), primary_key=True),
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
# )


class StoreDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "stores"
    name: Mapped[str] = mapped_column(index=True)
    city: Mapped[Optional[str]]
    country: Mapped[Optional[str]]

    receipt_entries: Mapped[list["ReceiptEntryDB"]] = relationship(
        back_populates="store"
    )
    user: Mapped["UserDB"] = relationship(back_populates="stores")
    product_items: Mapped[list["ProductItemDB"]] = relationship(back_populates="store")


class Store(IDFieldSchemaMixin, UserIDFieldSchemaMixin, TimeStampSchemaMixin):
    name: str
    city: str | None = None
    country: str | None = None
    model_config = ConfigDict(from_attributes=True)


class StoreCreate(CamelBase):
    name: str
    city: str | None = None
    country: str | None = None


class StoreUpdate(CamelBase):
    name: str | None = None
    city: str | None = None
    country: str | None = None


class StoreWithReceiptEntries(Store):
    receipt_entries: list["ReceiptEntry"]
