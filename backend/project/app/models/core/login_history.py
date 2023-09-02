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


class LoginHistoryDB(IDFieldDBMixin, UserIDFieldDBMixin, TimeStampDBMixin, Base):
    __tablename__ = "login_history"
    ip_address: Mapped[str]
    fresh: Mapped[bool] = mapped_column(default=False)
    user: Mapped["UserDB"] = relationship(
        back_populates="login_history", lazy="selectin"
    )


class LoginHistory(IDFieldSchemaMixin, UserIDFieldSchemaMixin, TimeStampSchemaMixin):
    ip_address: str
    fresh: bool
    model_config = ConfigDict(from_attributes=True)


class LoginHistoryCreate(CamelBase):
    ip_address: str
    fresh: bool


class LoginHistoryUpdate(CamelBase):
    pass
