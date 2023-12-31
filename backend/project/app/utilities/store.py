from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis as AsyncRedis

from app import crud
from app import models
from app.config import CachedItemPrefix


async def create_or_get_store_id(
    db: AsyncSession, user: models.UserDB, name: str
) -> int | UUID:
    list_stores = await crud.store.search(db, user, name)
    if not list_stores:
        store_create_schema = models.StoreCreate(name=name, city="Brunssum")
        store = await crud.store.create(db, store_create_schema, user)
        return store.id
    store = list_stores[0]
    return store.id


async def get_store(
    db: AsyncSession, store_id: int | UUID
) -> models.StoreDB:
    print('in function, get_store: store id is: ', store_id)
    store = await crud.store.get(db, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
    return store


async def add_store_to_user(
    db: AsyncSession,
    cache: AsyncRedis,
    user: models.UserDB,
    store_id: int | UUID,
) -> None:
    store = await get_store(db, store_id)
    await user.awaitable_attrs.stores
    if store not in user.stores:
        print('appending store to user')
        user.stores.append(store)


async def remove_user_from_store(
    db: AsyncSession, cache: AsyncRedis, user: models.UserDB, store_id: int | UUID
) -> None:
    print('removing from store..')
    store = await get_store(db, store_id)
    await user.awaitable_attrs.stores
    if store in user.stores:
        await cache.delete(f'{CachedItemPrefix.STORES}{user.id}')
        await crud.store.remove(db, store)


async def entries_related_to_store(
    db: AsyncSession, user: models.UserDB, store_id: int
) -> bool:
    entries_with_store = await crud.receipt_entry.get_multi(
        db=db, user=user, column_filter_int="store_id", column_filter_int_value=store_id
    )
    print(entries_with_store)
    if len(entries_with_store) == 1:
        print('in function: no entries related')
        return False
    return True
