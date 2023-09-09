from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models


async def create_product_entries(
    db: AsyncSession,
    user: models.UserDB,
    entry_id: int | UUID,
    store_id: int | UUID,
    items: list[dict]
):
    for item in items:
        product_item_schema = models.ProductItemCreate(
            receipt_entry_id=entry_id,
            store_id=store_id,
            name=item['description'],
            price=item['amount'],
            quantity=int(item['qty']) if item['qty'] is not None else 1,
        )
        await crud.product_item.create(db, product_item_schema, user)
