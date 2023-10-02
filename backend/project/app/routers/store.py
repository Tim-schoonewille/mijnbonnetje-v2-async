from uuid import UUID

from fastapi import APIRouter, HTTPException


from app import crud, models
from app.config import settings
from app.utilities.core.dependencies import (
    VerifiedUser,
    GetDB,
    ParametersDepends,
    SudoUser,
)

router = APIRouter(prefix=settings.URL_PREFIX + "/store", tags=["store"])


@router.post("/", response_model=models.Store, status_code=201)
async def create_store(user: VerifiedUser, schema: models.StoreCreate, db: GetDB):
    """Creates a store (requires verified user token)"""
    return await crud.store.create(db, schema, user)


@router.get("/search", response_model=list[models.Store])
async def search_store(q: str, user: VerifiedUser, db: GetDB):
    """Search for a store by parameter q (string) requires verified user token"""
    return await crud.store.search(db, user, q)


@router.get("/user", response_model=list[models.Store])
async def read_user_stores(user_: VerifiedUser, db: GetDB):
    print("USER:::::", user_)
    await user_.awaitable_attrs.stores
    return user_.stores


@router.get("/{store_id}", response_model=models.Store)
async def read_specific_store(store_id: int | UUID, user: VerifiedUser, db: GetDB):
    """Reads a specific store from DB (requires verified user token)

    Raises:\n
        404: {detail: "STORE_NOT_FOUND"}
    """
    store = await crud.store.get(db, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
    return store


@router.get("/", response_model=list[models.Store])
async def read_multiple_stores(
    params: ParametersDepends, user: VerifiedUser, db: GetDB
):
    """Returns a list of stores with parameter filter (requires verified user token)"""
    return await crud.store.get_multi(db, user, **params)


@router.patch("/{store_id}", response_model=models.Store)
async def update_store(
    store_id: int | UUID, update_schema: models.StoreUpdate, sudo: VerifiedUser, db: GetDB
):
    """Update specific store (requires sudo login)
    c
        Raises:\n
            404: {detail: "STORE_NOT_FOUND"}
    """
    store_in_db = await crud.store.get(db, store_id)
    if store_in_db is None:
        raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
    return await crud.store.update(db, update_schema, store_in_db)


@router.delete("/{store_id}")
async def delete_store(store_id: int | UUID, sudo: SudoUser, db: GetDB):
    """delete specific store (requires sudo login)
    c
        Raises:\n
            404: {detail: "STORE_NOT_FOUND"}
    """
    store_in_db = await crud.store.get(db, store_id)
    if store_in_db is None:
        raise HTTPException(status_code=404, detail="STORE_NOT_FOUND")
    await crud.store.remove(db, store_in_db)
    return dict(message="STORE_DELETED")
