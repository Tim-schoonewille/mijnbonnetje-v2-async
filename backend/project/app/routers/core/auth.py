from typing import Union
from uuid import uuid4
from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from redis import Redis  # type: ignore
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import models
from app.config import Settings
from app.config import settings
from app.utilities.core.auth import authenticate
from app.utilities.core.auth import convert_to_hash
from app.utilities.core.auth import create_login_tokens
from app.utilities.core.auth import get_otp_object
from app.utilities.core.auth import invalid_credentials
from app.utilities.core.auth import register_new_login
from app.utilities.core.auth import register_new_otp
from app.utilities.core.auth import verify_otp_session_id
from app.utilities.core.dependencies import ActiveUser
from app.utilities.core.dependencies import FreshTokenUser
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import GetAsyncCache
from app.utilities.core.dependencies import GetSettings
from app.utilities.core.dependencies import SudoUser
from app.utilities.core.dependencies import VerifiedUser
from app.utilities.core.email import send_verification_code_email
from app.utilities.core.email import send_request_new_password_email
from app.utilities.core.log import log_traffic
from app.utilities.core.redis import redis_login_attempts
from app.utilities.core.redis import register_login_attempt
from app.utilities.core.token import consume_refresh_tokens
from app.utilities.core.token import create_email_verification_token
from app.utilities.core.token import create_password_token
from app.utilities.core.token import extract_payload
from app.utilities.core.token import token_is_expired
from app.utilities.core.token import token_is_valid
from app.utilities.core.two_factor import send_otp


router = APIRouter(prefix=f"{settings.URL_PREFIX}/auth", tags=["auth"])


@router.post("/signup", response_model=models.User, status_code=201)
@log_traffic()
async def register_new_user(
    schema_in: models.UserCreate,
    request: Request,
    bg_tasks: BackgroundTasks,
    db: GetDB,
):
    """
    Register a new user.\n

    Check if the user is already registered. \n
    Hash the user's password for security. \n
    Create a new user record in the database. \n
    Generate an email verification token. \n
    Send an email to the user with the verification token. \n

    Raises: \n
        400: If the user is already registered. (detail: 'DUPLICATE_EMAIL')
    """
    return await handle_signup(schema_in, bg_tasks, db)


@router.post("/login", response_model=dict[str, str])
@log_traffic()
async def login_user(
    schema_in: models.UserLogin,
    bg_tasks: BackgroundTasks,
    request: Request,
    response: Response,
    db: GetDB,
    settings: GetSettings,
    redis_client: GetAsyncCache,
):
    """
    Log in a user and return access and refresh tokens.

    Retrieve the user from the database based on email.
    Check login attempts and account lock status.
    Authenticate the user's password.
    Consume existing refresh tokens.
    Register the new login and issue new tokens.

    Raises: \n
        400: invalid credentials: {detail: 'INVALID_CREDENTIALS'} \n
        401: too many login attempts: {detail: 'LOCKED_OUT}
    """
    return await handle_login(
        email=schema_in.email,
        password=schema_in.password,
        bg_tasks=bg_tasks,
        request=request,
        response=response,
        settings=settings,
        cache=redis_client,
        db=db,
    )


@router.get("/logout")
@log_traffic()
async def logout(
    user: ActiveUser,
    request: Request,
    res: Response,
    db: GetDB,
    settings: GetSettings,
):
    """
    Log out a user and revoke tokens.

    Revoke refresh tokens associated with the user.
    Delete access and refresh tokens from cookies.
    """
    return await handle_logout(user=user, res=res, settings=settings, db=db)


@router.get("/verify-token")
@log_traffic()
async def verify_token(
    user: VerifiedUser,
    request: Request,
):
    """
    Verify an access token.

    No additional logic, simply indicate token verification.
    Raises:\n
        401: {detail: 'TOKENS_EXPIRED'}\n
        401: {detail: 'REFRESH_TOKEN_REVOKED'}\n
        403: {detail: 'EMAIL_NOT_VERIFIED'}\n
        404: {detail: 'INVALID_USER}
    """
    return handle_token()


@router.get("/verify-fresh-token")
@log_traffic()
async def verify_fresh_token(
    user: FreshTokenUser,
    request: Request,
) -> dict[str, bool]:
    """
    Verify that token is a fresh token.

    Raises:\n
        401: {detail: 'TOKENS_EXPIRED'}\n
        401: {detail: 'REFRESH_TOKEN_REVOKED'}\n
        403: {detail: 'EMAIL_NOT_VERIFIED'}\n
        404: {detail: 'INVALID_USER}\n
        401: {detail: 'REQUIRES_FRESH_TOKEN'}
    """
    return {"fresh": True}


@router.get("/verify-sudo-token")
@log_traffic()
async def verify_sudo_token(user: SudoUser, request: Request) -> dict[str, bool]:
    """
    Verify user/token has sudo rights.

    Raises:\n
        401: {detail: 'TOKENS_EXPIRED'}\n
        401: {detail: 'REFRESH_TOKEN_REVOKED'}\n
        403: {detail: 'EMAIL_NOT_VERIFIED'}\n
        404: {detail: 'INVALID_USER}\n
        403: {detail: 'REQUIRES_SUDO'}
    """
    return {"sudo": True}


@router.post("/email/verify/new")
@log_traffic()
async def request_email_verification_code(
    schema: models.RequestNewPassword,
    request: Request,
    bgtasks: BackgroundTasks,
    db: GetDB
):
    """
    Request a new email verification code.

    Generate a new email verification token.
    Send an email to the user with the verification token.

    Raised:\n
        404: {detail:"INVALID_EMAIL"}\n
        400: {detail: 'ALREADY_VERIFIED}\n
    """
    return await handle_new_verification_code(schema.email, bgtasks, db)


@router.get("/email/verify/")
@log_traffic()
async def verify_email(token: str, request: Request, db: GetDB):
    """
    Verify a user's email address.

    Validate the email verification token.
    Verify the user's email address in the database.

    Raises:\n
        400: {detail: 'INVALID_TOKEN}\n
        404: {detail: "USER_NOT_FOUND"}
    """
    return await handle_verify_email(token=token, db=db)


@router.post("/password/reset")
@log_traffic()
async def request_new_password_token(
    schema: models.RequestNewPassword,
    request: Request,
    bg_tasks: BackgroundTasks,
    db: GetDB,
):
    """
    Request a new password reset token.

    Check if the email exists in the database.
    Generate a new password reset token.

    Raises:\n
        404: {detail: 'INVALID_EMAIL'}
    """
    return await handle_new_password_token(email=schema.email, db=db, tasks=bg_tasks)


@router.post("/password/reset/verify")
@log_traffic()
async def verify_new_password_request(
    schema: models.ValidateRequestNewPassword,
    token: str,
    request: Request,
    db: GetDB,
):
    """
    Verify a new password reset request.

    Validate the password reset token.
    Update the user's password in the database.

    Raises:\n
        401: {detail: 'INVALID_OR_EXPIRED_TOKEN'}\n
        400: {detail: 'INVALID_TOKEN_SUB'}\n
    """
    return await handle_verify_new_password_request(
        new_password=schema.new_password, raw_password_token=token, db=db
    )


@router.get("/twofactor/", response_model=models.Tokens)
async def handle_two_factor_otp(
    otp_session_id: UUID,
    otp: str,
    request: Request,
    response: Response,
    cache: GetAsyncCache,
    db: GetDB,
):
    """
    Verify two factor OTP

    Raises:\n
        401: {detail: 'INVALID_OTP}\n
        404: {detail: 'USER_NOT_FOUND'}

    """
    user_id = await verify_otp_session_id(
        cache=cache,
        session_id=otp_session_id,
        otp=otp,
    )
    if not user_id:
        raise HTTPException(status_code=401, detail="INVALID_OTP")
    user = await crud.user.get(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    await register_new_login(user, db, request, fresh=True)
    return await create_login_tokens(user, response, db)


@router.patch("/twofactor/enable/{action}")
# @log_traffic()
async def update_two_factor_authentication(
    action: bool,
    user: FreshTokenUser,
    db: GetDB,
):
    """
    Enable or disable two factor authentication.
    """
    schema = models.UserUpdateTwoFactor(two_factor=action)
    await crud.user.update(db, schema, user)
    return dict(TwoFactorEnabled=action)


@router.get("/twofactor/renew")
async def twofactor_renew(
    otp_session_id: UUID,
    cache: GetAsyncCache,
):
    """
    Request a new OTP for two factor authentication.

    Raises:\n
        400: {detail: 'INVALID_SESSION_ID}
    """
    otp_cache_key = settings.OTP_CACHE_PREFIX + str(otp_session_id)
    otp_object_in_cache = await get_otp_object(otp_cache_key, cache)
    if otp_object_in_cache is None:
        raise HTTPException(status_code=400, detail="INVALID_SESSION_ID")

    await cache.delete(otp_cache_key)
    return await register_new_otp(cache, otp_object_in_cache.user_id)


# CONTROLLER LOGIC


async def handle_signup(
    schema: models.UserCreate, bg_tasks: BackgroundTasks, db: AsyncSession
) -> dict[str, str]:
    user = await crud.user.get_by_email(db, schema.email)
    if user:
        raise HTTPException(status_code=400, detail="DUPLICATE_EMAIL")
    schema.password = convert_to_hash(schema.password)
    user = await crud.user.create(db=db, schema_in=schema)
    email_verification_token = create_email_verification_token(user.email)
    send_verification_code_email(user.email, email_verification_token, bg_tasks)
    return user


async def handle_login(
    email: str,
    password: str,
    bg_tasks: BackgroundTasks,
    request: Request,
    response: Response,
    settings: Settings,
    cache: AsyncRedis,
    db: AsyncSession,
) -> dict[str, str]:
    user: models.UserDB = await crud.user.get_by_email(db, email)
    if user is None:
        raise invalid_credentials()
    login_attempts = await redis_login_attempts(user.id, cache)
    if login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
        raise HTTPException(status_code=401, detail="LOCKED_OUT")

    if not authenticate(plaintext_password=password, user=user):
        await register_login_attempt(user.id, login_attempts, cache)
        raise invalid_credentials()

    await consume_refresh_tokens(user=user, db=db)
    if user.two_factor:
        new_otp = await register_new_otp(cache=cache, user_id=user.id)
        send_otp(email, new_otp, bg_tasks)
        return dict(TwoFactor="sent")
    await register_new_login(user, db, request, fresh=True)
    return await create_login_tokens(user, response, db)


async def handle_logout(
    user: models.UserDB, res: Response, settings: Settings, db: AsyncSession
) -> dict[str, str]:
    await crud.refresh_token.revoke(db, user.id)
    res.delete_cookie(settings.ACCESS_TOKEN_COOKIE_NAME, domain=settings.DOMAIN)
    res.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME, domain=settings.DOMAIN)
    return dict(message="Logged off")


def handle_token() -> dict[str, bool]:
    return dict(token=True)


async def handle_new_verification_code(
    email: str, bgtasks: BackgroundTasks, db: AsyncSession,
) -> dict[str, str]:
    user = await crud.user.get_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail='INVALID_EMAIL')
    if user.verified:
        raise HTTPException(status_code=400, detail="ALREADY_VERIFIED")

    email_verification_code = create_email_verification_token(user.email)
    send_verification_code_email(user.email, email_verification_code, bgtasks)
    return dict(message="NEW_VERIFICATION_CODE_SENT")


# async def handle_new_verification_code(
#     user: models.UserDB, bgtasks: BackgroundTasks
# ) -> dict[str, str]:
#     if user.verified:
#         raise HTTPException(status_code=400, detail="ALREADY_VERIFIED")

#     email_verification_code = create_email_verification_token(user.email)
#     send_verification_code_email(user.email, email_verification_code, bgtasks)
#     return dict(message="NEW_VERIFICATION_CODE_SENT")


async def handle_verify_email(token: str, db: AsyncSession) -> dict[str, str]:
    email_token = models.Token(jwt=token)
    if not token_is_valid(email_token) or token_is_expired(email_token):
        raise HTTPException(status_code=400, detail="INVALID_TOKEN")

    payload = extract_payload(email_token)
    user_email, _type = payload["sub"], payload["_type"]
    if _type != "email":
        raise HTTPException(status_code=400, detail="INVALID_TOKEN")

    await crud.user.verify_email(db, user_email)
    return dict(status="verified")


async def handle_new_password_token(email: str, db: AsyncSession, tasks: BackgroundTasks) -> dict[str, str]:
    db_user: models.UserDB = await crud.user.get_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="INVALID_EMAIL")

    jti = str(uuid4())
    token = create_password_token(sub=str(db_user.id), jti=jti)
    send_request_new_password_email(to=email, code=token, bg_tasks=tasks)
    return dict(token=token)


async def handle_verify_new_password_request(
    new_password: str,
    raw_password_token: str,
    db: AsyncSession,
) -> dict[str, str]:
    password_token = models.Token(jwt=raw_password_token)
    if not token_is_valid(password_token) and token_is_expired(password_token):
        raise HTTPException(status_code=401, detail="INVALID_OR_EXPIRED_TOKEN")

    payload = extract_payload(password_token)
    user_id, _type = int(payload["sub"]), payload["_type"]
    if _type != "password":
        raise HTTPException(status_code=401, detail="INVALID_OR_EXPIRED_TOKEN")

    user_in_db = await crud.user.get(db, user_id)
    if user_in_db is None:
        raise HTTPException(status_code=400, detail="INVALID_TOKEN_SUB")

    new_password = convert_to_hash(new_password)
    await crud.user.update_password(db, user_in_db, new_password)
    await crud.refresh_token.revoke(db, user_id)
    return dict(message="Password updated!")
