from uuid import UUID
import pickle

from fastapi import APIRouter, HTTPException, Request

from app import crud
from app import models
from app.utilities.core.dependencies import GetCache
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.dependencies import UserLimitedAPICalls
from app.config import settings
from app.config import CachedItemPrefix
from app.utilities.core.log import log_traffic


router = APIRouter(prefix=f"{settings.URL_PREFIX}/item", tags=["item"])


@router.get("/", response_model=list[models.Item])
@log_traffic()
async def read_all_items(
    params: ParametersDepends,
    request: Request,
    user: VerifiedUser,
    db: GetDB,
):
    all_items = await crud.item.get_multi(db, user, **params)
    return all_items


@router.get("/{item_id}", response_model=models.Item)
@log_traffic()
async def read_specific_ite_with_cache(
    item_id: int | UUID,
    user: VerifiedUser,
    request: Request,
    redis: GetCache,
    db: GetDB,
):
    cached_item = redis.get(f"{CachedItemPrefix.ITEM}{item_id}")
    if cached_item:
        cached_item = pickle.loads(cached_item)
        if cached_item.user_id != user.id and not user.sudo:
            raise HTTPException(status_code=403, detail="Not your item")
        return cached_item

    item = await crud.item.get(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != user.id and not user.sudo:
        raise HTTPException(status_code=401, detail="Not your Item")

    redis.set(
        name=f"{CachedItemPrefix.ITEM}{item_id}",
        value=pickle.dumps(item),
        ex=settings.CACHE_EXPIRATION_TIME,
    )
    return item


@router.post("/", response_model=models.Item)
# @log_traffic()
async def create_new_item(
    input_schema: models.ItemCreate,
    user: UserLimitedAPICalls,
    request: Request,
    db: GetDB,
):
    new_item = await crud.item.create(db, input_schema, user)
    return new_item


@router.patch("/{item_id}", response_model=models.Item)
@log_traffic()
async def update_specific_item(
    item_id: int | UUID,
    update_schema: models.ItemUpdate,
    user: VerifiedUser,
    request: Request,
    redis: GetCache,
    db: GetDB,
):
    item = await crud.item.get(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != user.id or not user.sudo:
        raise HTTPException(status_code=401, detail="Not your Item")
    updated_item = await crud.item.update(db, update_schema, item)
    redis.set(
        name=f"{CachedItemPrefix.ITEM}{item_id}",
        value=pickle.dumps(updated_item),
        ex=settings.CACHE_EXPIRATION_TIME,
    )
    return updated_item


@router.delete("/{item_id}")
@log_traffic()
async def delete_specific_item(
    item_id: int | UUID,
    user: VerifiedUser,
    request: Request,
    redis: GetCache,
    db: GetDB,
):
    item = await crud.item.get(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != user.id or not user.sudo:
        raise HTTPException(status_code=401, detail="Not your Item")
    await crud.item.remove(db, item)
    redis.delete(f"{CachedItemPrefix.ITEM}{item_id}")
    return {"message": "Item deleted"}
