# from typing import Optional
# from typing import TYPE_CHECKING
# from typing import Union

# from pydantic import ConfigDict

# from app.models.base import CamelBase


# if TYPE_CHECKING:
#     from app.models import ReceiptEntry
#     from app.models import ReceiptFile
#     from app.models import ReceiptScan
#     from app.models import Store
#     from app.models import ProductItem


# class Receipt(ReceiptEntry):
#     receipt_files: list['ReceiptFile']
#     receipt_scans: list['ReceiptScan']
#     store: Union['Store', None] = None
#     product_items: list['ProductItem'] | None = None
