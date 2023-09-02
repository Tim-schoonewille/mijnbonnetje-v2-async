from datetime import date
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from typing import List

from fastapi import HTTPException
from pydantic import ConfigDict
from pydantic import field_validator
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import TierIDFieldDBMixin
from app.models.base import TierIDFieldSchemaMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin

if TYPE_CHECKING:
    from app.models import PaymentDB
    from app.models import UserDB
    from app.models import TierDB
    from app.models import Tier
    from app.models import Payment


class SubscriptionDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    TierIDFieldDBMixin,
    TimeStampDBMixin,
    Base
):
    __tablename__ = "subscriptions"
    start_date: Mapped[date]
    end_date: Mapped[Optional[date]]
    # tier_id: Mapped[int] = mapped_column(ForeignKey("tiers.id"))
    active: Mapped[bool] = mapped_column(default=False)

    user: Mapped["UserDB"] = relationship(back_populates="subscriptions")
    payments: Mapped[List["PaymentDB"]] = relationship(
        back_populates="subscription", cascade="all,delete"
    )
    tier: Mapped["TierDB"] = relationship(back_populates="subscriptions")


class SubscriptionBase(TierIDFieldSchemaMixin):
    start_date: date
    end_date: date
    # tier_id: int


class Subscription(
    IDFieldSchemaMixin, UserIDFieldSchemaMixin, TimeStampSchemaMixin, SubscriptionBase
):
    active: bool
    model_config = ConfigDict(from_attributes=True)


class SubscriptionCreate(CamelBase, SubscriptionBase):
    start_date: date
    end_date: date
    # tier_id: int

    @field_validator('start_date')
    def validate_start_date_is_not_before_today(cls, value):
        if value < date.today():
            raise HTTPException(
               status_code=422,
               detail="Start date can't be before current date"
            )
        return value


class SubscriptionCreateSchema(CamelBase, TierIDFieldSchemaMixin):
    start_date: date
    # tier_id: int


class SubscriptionUpdate(CamelBase):
    start_date: date | None = None
    end_date: date | None = None
    active: bool | None = None


class SubscriptionWithTier(Subscription):
    tier: "Tier"
    payments: list["Payment"] | None


class SubscriptionsWithTierAndMetaData(CamelBase):
    amount: int
    subscriptions: list[SubscriptionWithTier]
