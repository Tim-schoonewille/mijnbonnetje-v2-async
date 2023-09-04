from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.base import CamelBase
from app.models.base import IDFieldDBMixin
from app.models.base import IDFieldSchemaMixin
from app.models.base import ReceiptFileIDFieldDBMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin


if TYPE_CHECKING:
    from app.models import UserDB
    from app.models import ReceiptFileDB


class ReceiptScanDB(
    IDFieldDBMixin,
    ReceiptFileIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = 'receipt_scans'
    scan: Mapped[str]

    receipt_file: Mapped['ReceiptFileDB'] = relationship(back_populates='receipt_scans')


class ReceiptScan(IDFieldSchemaMixin, TimeStampSchemaMixin):
    receipt_file_id: int | UUID
    scan: str
    model_config = ConfigDict(from_attributes=True)


class ReceiptScanCreate(CamelBase):
    receipt_file_id: int | UUID
    scan: str


class ReceiptScanUpdate(CamelBase):
    pass
