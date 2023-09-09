from typing import Any
from typing import Optional
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
from app.models.base import ReceiptFileIDFieldDBMixin
from app.models.base import TimeStampDBMixin
from app.models.base import TimeStampSchemaMixin


if TYPE_CHECKING:
    from app.models import ReceiptEntryDB
    from app.models import ReceiptFileDB


class ReceiptScanDB(
    IDFieldDBMixin,
    ReceiptEntryIDFieldDBMixin,
    ReceiptFileIDFieldDBMixin,
    TimeStampDBMixin,
    Base,
):
    __tablename__ = "receipt_scans"
    scan: Mapped[str]
    scan_json: Mapped[Optional[dict[str, Any]]]
    receipt_entry: Mapped["ReceiptEntryDB"] = relationship(
        back_populates="receipt_scans"
    )
    receipt_file: Mapped["ReceiptFileDB"] = relationship(back_populates="receipt_scans")


class ReceiptScan(IDFieldSchemaMixin, TimeStampSchemaMixin):
    receipt_entry_id: int | UUID
    receipt_file_id: int | UUID
    scan: str
    # scan_json: dict[str, Any]
    model_config = ConfigDict(from_attributes=True)


class ReceiptScanCreate(CamelBase):
    receipt_entry_id: int | UUID
    receipt_file_id: int | UUID
    scan: str


class ReceiptScanUpdate(CamelBase):
    scan_json: dict[str, Any]
