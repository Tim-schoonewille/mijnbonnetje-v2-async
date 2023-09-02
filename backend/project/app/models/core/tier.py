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


if TYPE_CHECKING:
    from app.models import SubscriptionDB


class TierDB(IDFieldDBMixin, TimeStampDBMixin, Base):
    __tablename__ = "tiers"
    name: Mapped[str]
    price: Mapped[int]
    duration: Mapped[int]
    description: Mapped[str]

    # based on the app:
    api_call_limit: Mapped[int]

    subscriptions: Mapped["SubscriptionDB"] = relationship(back_populates="tier")


class Tier(
    IDFieldSchemaMixin,
    TimeStampSchemaMixin,
):
    name: str
    price: int
    duration: int
    description: str

    # based on app:
    api_call_limit: int
    model_config = ConfigDict(from_attributes=True)


class TierCreate(CamelBase):
    name: str
    price: int
    duration: int
    description: str
    api_call_limit: int


class TierUpdate(CamelBase):
    name: str | None = None
    price: int | None = None
    duration: int | None = None
    description: str | None = None
    api_call_limit: int | None = None
