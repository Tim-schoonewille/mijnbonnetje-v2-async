from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models
from app.config import settings
from app.db import get_db
from app.utilities.core.auth import authenticate
from app.utilities.core.auth import convert_to_hash
from app.utilities.core.dependencies import FreshTokenUser
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.log import log_traffic


router = APIRouter(
    prefix=f"{settings.URL_PREFIX}/user",
    tags=["user"],
)


@router.get("/self", response_model=models.User)
# @log_traffic()
async def get_self(
    user: VerifiedUser,
    request: Request,
    db: GetDB,
):
    return user


@router.patch("", response_model=models.User)
async def update_self(user: FreshTokenUser, schema: models.UserUpdate, db: GetDB):
    return await crud.user.update(db, schema, user)


@router.patch("/change/password")
@log_traffic()
async def user_change_password(
    user: FreshTokenUser,
    new_password_schema: models.UserUpdatePassword,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Change user password. (requires fresh token)

    Raises:\n
        401: {detail: "INVALID_CREDENTIALS"}
    """
    if not authenticate(new_password_schema.old_password, user):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")

    new_password = convert_to_hash(new_password_schema.new_password)
    await crud.user.update_password(db, user, new_password)
    await db.run_sync(lambda sess: user.id)
    await crud.refresh_token.revoke(db, user.id)
    return {"succes": "Password updated"}
