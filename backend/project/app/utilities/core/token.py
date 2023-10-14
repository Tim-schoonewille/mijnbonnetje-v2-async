from datetime import datetime
from datetime import timedelta
from typing import Any

from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from jose import ExpiredSignatureError
from jose import JWTError
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app import crud
from app import models
from app.config import get_settings


settings = get_settings()


def create_token(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)


def create_access_token(
    sub: str, refresh: bool = False, fresh: bool | None = True, jti: str = str(uuid4())
) -> str:
    seconds = settings.ACCES_TOKEN_EXPIRES
    if refresh:
        seconds = settings.REFRESH_TOKEN_EXPIRES
    expires = datetime.utcnow() + timedelta(seconds=seconds)
    payload = {"sub": sub, "exp": expires, "fresh": fresh, "jti": jti}
    token = create_token(payload)
    return token


def create_email_verification_token(sub: str) -> str:
    expires = datetime.utcnow() + timedelta(seconds=settings.EMAIL_TOKEN_EXPIRES)
    return create_token({"sub": str(sub), "exp": expires, "_type": "email"})


def create_password_token(sub: str, jti: str) -> str:
    expires = datetime.utcnow() + timedelta(seconds=settings.PASSWORD_TOKEN_EXPIRES)
    return create_token(
        {
            "sub": sub,
            "exp": expires,
            "jti": jti,
            "_type": "password",
        }
    )


def extract_payload(token: models.Token) -> dict:
    payload = jwt.decode(
        token.jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    return payload


def token_is_expired(token: models.Token) -> bool:
    try:
        extract_payload(token)
    except ExpiredSignatureError:
        return True
    except JWTError:
        return True
    return False


def token_is_valid(token: models.Token) -> bool:
    try:
        extract_payload(token)
    except JWTError:
        return False
    return True


def store_token(res: Response, key: str, value: str) -> None:
    res.set_cookie(
        key=key,
        value=value,
        httponly=True,
        domain=settings.DOMAIN,
        secure=settings.COOKIE_SECURE,
        max_age=settings.REFRESH_TOKEN_EXPIRES * 2,
        samesite='lax',
    )


def retreive_token(req: Request, key: str):
    token = req.cookies.get(key)

    if token is None:
        raise HTTPException(status_code=410, detail=f"NO_{key}_TOKEN")
    return models.Token(jwt=token)


async def register_refresh_token(
    user: models.UserDB, db: AsyncSession, jti: str
) -> None:
    new_refresh_token_registration = models.RefreshTokenCreate(jti=jti)
    await crud.refresh_token.create(db, new_refresh_token_registration, user)
    return None


async def consume_refresh_tokens(
    user: models.UserDB,
    db: AsyncSession,
) -> None:
    for refresh_token in await user.awaitable_attrs.refresh_tokens:
        if not refresh_token.consumed:
            refresh_token.consumed = True
            refresh_token.date_consumed = datetime.utcnow()


async def is_refresh_revoked(db: AsyncSession, jti: str) -> bool:
    refresh_token_in_db = await crud.refresh_token.get_by_token(db, jti)
    if refresh_token_in_db is None:
        return False
    return not refresh_token_in_db.consumed
