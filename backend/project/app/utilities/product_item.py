from uuid import UUID
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models


def remove_leading_digits(string: str) -> str:
    parsed_string = []
    letter_encountered = False
    for letter in string:
        if letter.isdigit() and not letter_encountered:
            continue
        if letter.isspace() and not letter_encountered:
            continue
        if letter.isalpha():
            letter_encountered = True
        parsed_string.append(letter)
    return ''.join(parsed_string)


def new_remove_leading_digits(string: str) -> str:
    letter_encountered = False
    return ''.join([letter for letter in string if not letter.isdigit() or letter.isalpha() or (letter.isspace() and not letter_encountered) or (letter_encountered := True)])


async def create_product_entries(
    db: AsyncSession,
    user: models.UserDB,
    entry_id: int | UUID,
    purchase_date: str,
    store_id: int | UUID,
    items: list[dict[str, Any]],
    total_amount: int,
) -> None:
    for item in items:
        if 'btw' in item['description'].lower():
            continue
        if 'totaal' in item['description'].lower():
            continue
        if total_amount == item['amount'] and len(items) < 3:
            print('item:', item)
            continue
        product_item_schema = models.ProductItemCreate(
            receipt_entry_id=entry_id,
            store_id=store_id,
            purchase_date=purchase_date,
            name=remove_leading_digits(item["description"]),
            price=item["amount"],
            quantity=int(item["qty"]) if item["qty"] is not None else 1,
        )
        await crud.product_item.create(db, product_item_schema, user)
