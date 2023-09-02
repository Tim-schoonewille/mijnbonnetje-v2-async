from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import User


class ItemDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "items"
    name: Mapped[str]
    description: Mapped[str]

    user: Mapped["UserDB"] = relationship(back_populates="items")


class ItemBase(CamelBase):
    name: str
    description: str | None = None


class Item(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    TimeStampSchemaMixin,
    ItemBase,
):
    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemWithUser(Item):
    user: "User"
