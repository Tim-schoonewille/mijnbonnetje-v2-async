from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import ConfigDict
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
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


class RefreshTokenDB(IDFieldDBMixin, UserIDFieldDBMixin, TimeStampDBMixin, Base):
    __tablename__ = "refresh_tokens"

    jti: Mapped[str] = mapped_column(index=True)
    consumed: Mapped[bool] = mapped_column(default=False)
    date_consumed: Mapped[datetime | None]
    user: Mapped["UserDB"] = relationship(back_populates="refresh_tokens")


class RefreshToken(IDFieldSchemaMixin, UserIDFieldSchemaMixin, TimeStampSchemaMixin):
    jti: str
    consumed: bool
    date_consumed: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class RefreshTokenCreate(CamelBase):
    jti: str


class RefreshTokenUpdate(CamelBase):
    consumed: bool
    date_consumed: datetime
