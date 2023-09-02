import pickle
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from app import crud
from app import models
from app.config import settings
from app.config import CachedItemPrefix
from app.utilities.core.dependencies import GetCache
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.dependencies import SudoUser
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.log import log_traffic
from app.utilities.core.redis import cache_item


router = APIRouter(prefix=f"{settings.URL_PREFIX}/sub/tier", tags=["tier"])


@router.get("/", response_model=list[models.Tier])
@log_traffic()
async def read_all_tiers(
    params: ParametersDepends,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """Returns all subscription tiers (requires verified token)"""
    results = await crud.tier.get_multi(db, user, **params)
    return results


@router.get("/{tier_id}", response_model=models.Tier)
@log_traffic()
@cache_item(CachedItemPrefix.TIER, "tier_id")
async def read_specific_tier(
    tier_id: int | UUID,
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    """
    Return specific tier information. (requires verified token)

    Raises:\n
        404: {detail: "TIER_NOT_FOUND"}
    """
    tier_in_db = await crud.tier.get(db, tier_id)
    if tier_in_db is None:
        raise HTTPException(status_code=404, detail="TIER_NOT_FOUND")
    return tier_in_db


@router.post("/", response_model=models.Tier, status_code=201)
@log_traffic()
async def create_new_tier(
    input_schema: models.TierCreate,
    sudo: SudoUser,
    request: Request,
    db: GetDB,
):
    """ Create a new Tier (requires sudo token) """
    new_tier = await crud.tier.create(db, input_schema, sudo)
    return new_tier


@router.patch("/{tier_id}", response_model=models.Tier)
@log_traffic()
async def update_tier(
    tier_id: int | UUID,
    update_schema: models.TierUpdate,
    user: SudoUser,
    request: Request,
    redis: GetCache,
    db: GetDB,
):
    """
    Update tier information. (requires sudo token)

    Raises:\n
        404: {detail: "TIER_NOT_FOUND"}
    """
    tier_in_db = await crud.tier.get(db, tier_id)
    if tier_in_db is None:
        raise HTTPException(status_code=404, detail="TIER_NOT_FOUND")
    updated_tier = await crud.tier.update(
        db=db,
        update_schema=update_schema,
        object=tier_in_db,
    )
    redis.set(
        f"{CachedItemPrefix.TIER}{tier_id}",
        value=pickle.dumps(updated_tier),
        ex=settings.CACHE_EXPIRATION_TIME,
    )
    return updated_tier


@router.delete("/{tier_id}")
@log_traffic()
async def delete_tier(
    tier_id: int | UUID,
    user: SudoUser,
    redis: GetCache,
    request: Request,
    db: GetDB,
):
    """
    Delete specific tier. (requires sudo token)

    Raises:\n
        404: {detail: "TIER_NOT_FOUND"}
    """
    tier_in_db = await crud.tier.get(db, tier_id)
    if tier_in_db is None:
        raise HTTPException(status_code=404, detail="TIER_NOT_FOUND")
    await crud.tier.remove(db, tier_in_db)
    redis.delete(CachedItemPrefix.TIER + str(tier_id))
    return {"message": "Tier deleted"}
