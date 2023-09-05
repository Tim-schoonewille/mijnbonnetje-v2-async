from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import ReceiptEntryIDFieldDBMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin
from app.models.base import UserIDFieldDBMixin
from app.models.base import UserIDFieldSchemaMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import ReceiptEntryDB
    from app.models import ReceiptScanDB


class ReceiptFileDB(
    IDFieldDBMixin,
    UserIDFieldDBMixin,
    ReceiptEntryIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "receipt_files"
    file_name: Mapped[str]
    file_path: Mapped[str]
    file_type: Mapped[str]
    file_size: Mapped[int]

    user: Mapped["UserDB"] = relationship(back_populates="receipt_files")
    receipt_entry: Mapped["ReceiptEntryDB"] = relationship(
        back_populates="receipt_files"
    )
    receipt_scans: Mapped[list["ReceiptScanDB"]] = relationship(
        back_populates="receipt_file"
    )


class ReceiptFile(
    IDFieldSchemaMixin,
    UserIDFieldSchemaMixin,
    TimeStampSchemaMixin,
):
    receipt_entry_id: int | UUID
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    model_config = ConfigDict(from_attributes=True)


class ReceiptFileCreate(CamelBase):
    receipt_entry_id: int | UUID
    file_name: str
    file_path: str
    file_type: str
    file_size: int


class ReceiptFileUpdate(CamelBase):
    file_name: str | None = None
    file_path: str | None = None
    file_type: str | None = None
    file_size: int | None = None
