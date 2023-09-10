import pickle
from typing import Annotated
from uuid import UUID
from uuid import uuid4

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from passlib.context import CryptContext
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models
from app.config import Settings
from app.config import get_settings
from app.config import settings
from app.db import get_db
from app.mongodb import get_mongo_db
from app.utilities.core.token import create_access_token
from app.utilities.core.token import extract_payload
from app.utilities.core.token import is_refresh_revoked
from app.utilities.core.token import retreive_token
from app.utilities.core.token import store_token
from app.utilities.core.token import token_is_expired
from app.utilities.core.token import token_is_valid
from app.utilities.core.token import register_refresh_token
from app.utilities.core.user_api_call_log import api_calls_exceeded
from app.utilities.core.user_api_call_log import get_api_call_limit


pwd_context = CryptContext(schemes=["bcrypt"])


def convert_to_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(plaintext_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plaintext_password, hashed_password)


def authenticate(plaintext_password: str, user: models.UserDB) -> bool:
    return verify_password_hash(plaintext_password, user.password)


def invalid_credentials():
    """Raises an HTTPException for invalid credentials (status_code=400)."""
    return HTTPException(status_code=400, detail="INVALID_CREDENTIALS")


async def register_new_login(
    user: models.UserDB, db: AsyncSession, req: Request, fresh: bool = False
) -> None:
    if req.client is None:
        return None
    new_login = models.LoginHistoryCreate(ip_address=req.client.host, fresh=fresh)
    await crud.login_history.create(db, new_login, user)
    return None


async def create_login_tokens(
    user: models.UserDB,
    res: Response,
    db: AsyncSession,
) -> dict:
    access_token = create_access_token(sub=user.email)
    jti_refresh_token = str(uuid4())
    refresh_token = create_access_token(
        sub=user.email,
        refresh=True,
        jti=jti_refresh_token,
    )
    store_token(res=res, key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token)
    store_token(res=res, key=settings.REFRESH_TOKEN_COOKIE_NAME, value=refresh_token)
    await register_refresh_token(user, db, jti_refresh_token)
    return {
        settings.ACCESS_TOKEN_COOKIE_NAME: access_token,
        settings.REFRESH_TOKEN_COOKIE_NAME: refresh_token,
    }


async def get_user(
    req: Request,
    res: Response,
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
) -> models.UserDB:
    access_token = retreive_token(req, key=settings.ACCESS_TOKEN_COOKIE_NAME)
    refresh_token = retreive_token(req, key=settings.REFRESH_TOKEN_COOKIE_NAME)
    token_refreshing = False

    if token_is_expired(access_token) and not token_is_valid(refresh_token):
        raise HTTPException(status_code=401, detail="TOKENS_EXPIRED")

    if token_is_expired(access_token) and token_is_valid(refresh_token):
        token_refreshing = True
        refresh_token_payload = extract_payload(refresh_token)
        if not await is_refresh_revoked(db, refresh_token_payload["jti"]):
            raise HTTPException(status_code=490, detail="REFRESH_TOKEN_REVOKED")
        print("REFRESHING!!!!!!!!!!!!!!!!!")
        access_token = create_access_token(
            sub=refresh_token_payload["sub"], fresh=False
        )
        access_token = models.Token(jwt=access_token)
        store_token(
            res=res, key=settings.ACCESS_TOKEN_COOKIE_NAME, value=access_token.jwt
        )
    payload = extract_payload(access_token)
    user = await crud.user.get_by_email(db, email=payload["sub"])
    if user is None:
        raise HTTPException(status_code=404, detail="INVALID_USER")

    if token_refreshing:
        await register_new_login(user, db, req, fresh=False)

    return user


async def get_verified_user(user: models.UserDB = Depends(get_user)) -> models.UserDB:
    if not user.verified:
        raise HTTPException(status_code=403, detail="EMAIL_NOT_VERIFIED")
    return user


async def get_user_api_call_log(
    user: Annotated[models.UserDB, Depends(get_verified_user)],
    mongo: AsyncIOMotorClient = Depends(get_mongo_db),
    settings: Settings = Depends(get_settings),
):
    api_call_limit = await get_api_call_limit(user)
    collection = mongo[settings.API_CALL_LOG_COLLECTION]
    no_authorization = await api_calls_exceeded(collection, user.id, api_call_limit)
    if no_authorization:
        raise HTTPException(status_code=403, detail="REQUEST_AMOUNT_EXCEEDED")
    return user


async def get_sudo(user: models.UserDB = Depends(get_user)) -> models.UserDB:
    if not user.sudo:
        raise HTTPException(status_code=403, detail="REQUIRES_SUDO")
    return user


async def get_fresh_user(
    user: Annotated[models.UserDB, Depends(get_verified_user)],
    req: Request,
) -> models.UserDB:
    access_token = retreive_token(req, key=settings.ACCESS_TOKEN_COOKIE_NAME)
    requires_fresh_login = HTTPException(status_code=401, detail="REQUIRES_FRESH_TOKEN")
    if token_is_expired(access_token):
        raise requires_fresh_login
    payload = extract_payload(access_token)
    token_is_fresh = payload.get("fresh", None)
    if not token_is_fresh:
        raise requires_fresh_login
    return user


async def register_new_otp(cache: AsyncRedis, user_id: int | UUID):
    new_otp = models.TwoFactorSchema(user_id=user_id)
    print(new_otp)
    await cache.set(
        name=settings.OTP_CACHE_PREFIX + str(new_otp.id),
        value=pickle.dumps(new_otp.model_dump()),
        ex=600,
    )
    return new_otp.model_dump()


async def get_otp_object(
    otp_cache_key: str, cache: AsyncRedis
) -> models.TwoFactorSchema | None:
    otp_pickled_object = await cache.get(otp_cache_key)
    if otp_pickled_object is None:
        return None

    otp_object = models.TwoFactorSchema(**pickle.loads(otp_pickled_object))
    return otp_object


async def verify_otp_session_id(
    session_id: UUID,
    otp: str,
    cache: AsyncRedis,
):
    otp_cache_key = settings.OTP_CACHE_PREFIX + str(session_id)
    otp_object = await get_otp_object(otp_cache_key, cache)
    if not otp_object:
        return False
    if otp_object.code != otp or otp_object.consumed:
        return False

    ttl_from_otp_cache = await cache.ttl(otp_cache_key)
    otp_object.consumed = True
    await cache.set(
        name=otp_cache_key,
        value=pickle.dumps(otp_object.model_dump()),
        ex=ttl_from_otp_cache,
    )
    return otp_object.user_id
