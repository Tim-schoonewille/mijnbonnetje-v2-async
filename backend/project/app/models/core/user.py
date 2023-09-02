from typing import TYPE_CHECKING
from typing import List

from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import field_validator
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.utilities.core.models import check_password_requirements

if TYPE_CHECKING:
    from app.models import Item
    from app.models import ItemDB
    from app.models import LoginHistoryDB
    from app.models import PaymentDB
    from app.models import RefreshTokenDB
    from app.models import SubscriptionDB


class UserDB(IDFieldDBMixin, TimeStampDBMixin, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    verified: Mapped[bool] = mapped_column(default=False)
    sudo: Mapped[bool] = mapped_column(default=False)
    two_factor: Mapped[bool] = mapped_column(default=False)

    # login_history: Mapped[List['LoginHistoryDB']] = relationship(
    #   back_populates='user', lazy='selectin'
    # )
    login_history: Mapped[List["LoginHistoryDB"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[List["RefreshTokenDB"]] = relationship(back_populates="user")
    subscriptions: Mapped[List["SubscriptionDB"]] = relationship(back_populates="user")
    payments: Mapped[List["PaymentDB"]] = relationship(back_populates="user")
    items: Mapped[List["ItemDB"]] = relationship(back_populates="user")

    def __repr__(self):
        return f'<User({self.id}) {self.email}>'


class User(IDFieldSchemaMixin, TimeStampSchemaMixin):
    email: EmailStr
    password: str
    active: bool
    verified: bool
    sudo: bool
    two_factor: bool
    model_config = ConfigDict(from_attributes=True)


class UserWithItems(User):
    items: List["Item"]


class UserCreate(CamelBase):
    email: EmailStr
    password: str

    # @field_validator('password')
    # def password_validation(cls, value):
    #     return check_password_requirements(cls, value)


class UserUpdateBase(CamelBase):
    pass


class UserUpdate(UserUpdateBase):
    email: EmailStr | None = None
    password: str | None = None
    active: bool | None = None
    verified: bool | None = None
    sudo: bool | None = None


class UserUpdatePassword(UserUpdateBase):
    old_password: str
    new_password: str

    # @field_validator('new_password')
    # def new_password_validation(cls, value):
    #     return check_password_requirements(cls, value)


class UserUpdateTwoFactor(UserUpdateBase):
    two_factor: bool


class UserLogin(UserCreate):
    pass


class RequestNewPassword(CamelBase):
    email: EmailStr


class ValidateRequestNewPassword(CamelBase):
    new_password: str

    # @field_validator('new_password')
    # def new_password_validation(cls, value):
    #     return check_password_requirements(cls, value)
