from datetime import date
from typing import Optional
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models import Categories
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


class ReceiptEntryDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = 'receipt_entries'
    # store_id
    purchase_date: Mapped[Optional[date]]
    total_amount: Mapped[int] = mapped_column(default=0)
    warranty: Mapped[int] = mapped_column(default=365*2)
    category: Mapped[Categories] = mapped_column(default=Categories.OTHER)

    user: Mapped['UserDB'] = relationship(back_populates='receipt_entries')


class ReceiptEntry(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    TimeStampSchemaMixin,
):
    purchase_date: date
    total_amount: int | None = None
    warranty: int
    category: Categories
    model_config = ConfigDict(from_attributes=True)

    @field_validator('purchase_date')
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except ValueError:
            return ValueError('Invalid date format, expected YYY-MM-DD')


class ReceiptEntryCreate(CamelBase):
    purchase_date: date = Field(default_factory=lambda: str(date.today()))
    total_amount: int = Field(default=0)
    warranty: int = Field(default=365*2)
    category: Categories = Field(default=Categories.OTHER)

    @field_validator('purchase_date')
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(value)
        except ValueError:
            return ValueError('Invalid date format, expected YYY-MM-DD')


class ReceiptEntryUpdate(CamelBase):
    purchase_date: date | None = None
    total_amount: int | None = None
    warranty: int | None = None
    category: Categories | None = None
