from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models


async def create_or_get_store_id(db: AsyncSession, user: models.UserDB, name: str) -> int | UUID:
    list_stores = await crud.store.search(db, user, name)
    if not list_stores:
        print('CREATING STORE............')
        store_create_schema = models.StoreCreate(
            name=name,
            city='Brunssum'
        )
        store = await crud.store.create(db, store_create_schema, user)
        return store.id
    print('GETTING STORE!!!!!!')
    store = list_stores[0]
    return store.id


async def add_user_to_store(db: AsyncSession, user: models.UserDB, store_id: int | UUID) -> None:
    store = await crud.store.get(db, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
    await store.awaitable_attrs.users
    if user not in store.users:
        store.users.append(user)
        # await db.commit()
