from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict
# from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import SubscriptionIDFieldDBMixin
from app.models.base import SubscriptionIDFieldSchemaMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin


if TYPE_CHECKING:
    from app.models import SubscriptionDB
    from app.models import UserDB


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    SubscriptionIDFieldDBMixin,
    TimeStampDBMixin,
    Base
):
    __tablename__ = "payments"
    # subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    payment_date: Mapped[Optional[datetime]]
    external_id: Mapped[UUID]
    amount: Mapped[int]
    method: Mapped[Optional[str]]
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.PENDING)

    subscription: Mapped["SubscriptionDB"] = relationship(
        back_populates="payments",
    )
    user: Mapped["UserDB"] = relationship(back_populates="payments")


class Payment(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    SubscriptionIDFieldSchemaMixin,
    TimeStampSchemaMixin
):
    # subscription_id: int
    payment_date: datetime | None = None
    external_id: UUID
    amount: int
    method: str | None = None
    status: PaymentStatus

    model_config = ConfigDict(from_attributes=True)


class PaymentCreateSchema(CamelBase):
    subscription_id: int | UUID


class PaymentCreate(CamelBase, SubscriptionIDFieldSchemaMixin):
    # subscription_id: int
    external_id: UUID
    amount: int


class PaymentUpdate(CamelBase):
    payment_date: datetime | None = None
    amount: int | None = None
    method: str | None = None
    status: PaymentStatus | None = None


class UpdatePayment(CamelBase):
    method: str
    status: PaymentStatus
