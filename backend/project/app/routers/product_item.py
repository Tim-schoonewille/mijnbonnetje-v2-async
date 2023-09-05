from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException


from app import crud
from app import models
from app.config import settings
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import ParametersDepends


router = APIRouter(prefix=settings.URL_PREFIX + '/product-item', tags=['product-item'])


@router.post('/', response_model=models.ProductItem, status_code=201)
async def create_product_item(
    user: VerifiedUser,
    schema: models.ProductItemCreate,
    db: GetDB,
):
    """Create a product item, requires verified user token """
    return await crud.product_item.create(db, schema, user)


@router.get('/', response_model=list[models.ProductItem])
async def read_multiple_product_items(
    user: VerifiedUser,
    params: ParametersDepends,
    db: GetDB,
):
    """Read multiple product items.
    Query parameters for filters.
    requires verified user otken
    """
    return await crud.product_item.get_multi(db, user, **params)


@router.get('/{product_item_id}', response_model=models.ProductItem)
async def read_specific_product_item(
    product_item_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """ Read specific product item in database.

    Raises:\n
        404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED" }
    """
    product_item_in_db = await crud.product_item.get(db, product_item_id)
    if product_item_in_db is None:
        raise HTTPException(status_code=404, detail="PRODUCT_ITEM_NOT_FOUND")
    if product_item_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return product_item_in_db


@router.patch('/{product_item_id}', response_model=models.ProductItem)
async def update_specific_product_item(
    product_item_id: int | UUID,
    schema: models.ProductItemUpdate,
    user: VerifiedUser,
    db: GetDB,
):
    """ Update specific product item in database.

    Raises:\n
        404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED" }
    """
    product_item_in_db = await crud.product_item.get(db, product_item_id)
    if product_item_in_db is None:
        raise HTTPException(status_code=404, detail="PRODUCT_ITEM_NOT_FOUND")
    if product_item_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return await crud.product_item.update(db, schema, product_item_in_db)


@router.delete('/{product_item_id}', response_model=dict[str, str])
async def delete_specific_product_item(
    product_item_id: int | UUID,
    user: VerifiedUser,
    db: GetDB,
):
    """Delete specific product item in database.

    Raises:\n
        404: {detail: " PRODUCT_ITEM_NOT_FOUND"}
        403: {detail: "ACCESS_DENIED" }
    """
    product_item_in_db = await crud.product_item.get(db, product_item_id)
    if product_item_in_db is None:
        raise HTTPException(status_code=404, detail="PRODUCT_ITEM_NOT_FOUND")
    if product_item_in_db.user_id != user.id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    await crud.product_item.remove(db, product_item_in_db)
    return dict(message="PRODUCT_ITEM_DELETED")
