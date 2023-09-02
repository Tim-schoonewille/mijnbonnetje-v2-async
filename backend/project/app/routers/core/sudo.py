from enum import Enum
from typing import Sequence
from uuid import UUID

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from app import crud
from app import models
from app.config import settings
from app.utilities.core.dependencies import GetDB
from app.utilities.core.dependencies import GetMongoDB
from app.utilities.core.dependencies import SudoUser
from app.utilities.core.dependencies import ParametersDepends
from app.utilities.core.log import log_traffic
from app.utilities.core.user_api_call_log import get_user_api_call_log


router = APIRouter(prefix=f"{settings.URL_PREFIX}/sudo", tags=["sudo"])


@router.get("/login-records", response_model=list[models.LoginHistory])
@log_traffic()
async def read_login_records(
    params: ParametersDepends,
    request: Request,
    user: SudoUser,
    db: GetDB,
):
    """
    Retrieves a list of login history records for the specified user.
    Requires authentication as a sudo user.
    """

    results = await crud.login_history.get_multi(db, user, **params)
    return results


@router.get("/refresh-tokens", response_model=list[models.RefreshToken])
@log_traffic()
async def read_refresh_tokens(
    params: ParametersDepends,
    user: SudoUser,
    request: Request,
    db: GetDB,
) -> Sequence[models.RefreshTokenDB]:
    """
    Retrieves a list of refresh tokens associated with the provided user.
    Requires authentication as a sudo user.
    """

    results = await crud.refresh_token.get_multi(db, user, **params)
    return results


class SudoUpdateActions(str, Enum):
    ASSIGN = "assign"
    REVOKE = "revoke"


@router.post("/refresh-token/revoke")
@log_traffic()
async def revoke_refresh_tokens_from_user(
    user_id: int | UUID,
    sudo: SudoUser,
    request: Request,
    db: GetDB,
):
    """
    Revokes refresh tokens for a specific user identified by user ID.
    Requires authentication as a sudo user.
    """

    await crud.refresh_token.revoke(db, user_id)
    return {"succes": "Tokens revoked."}


@router.patch("/user/update-sudo/{user_id}")
@log_traffic()
async def update_user_sudo_status(
    user_id: int | UUID,
    user: SudoUser,
    request: Request,
    action: SudoUpdateActions,
    db: GetDB,
):
    """
    Updates the sudo status of a user identified by their ID.
    Requires authentication as a sudo user.
    Accepts an action to either assign or revoke sudo privileges.

    Raises:\n
        400: {detail: "INVALID_ACTION"}\n
        404: {detail: ""USER_NOT_FOUND}
    """

    await crud.user.sudo(db, user_id, action)
    return {"succes": "sudo status updated"}


class ActiveUpdateActions(str, Enum):
    ENABLE = ("enable",)
    DISABLE = "disable"


@router.patch("/user/active/{user_id}")
@log_traffic()
async def update_user_active_status(
    user_id: int | UUID,
    sudo: SudoUser,
    action: ActiveUpdateActions,
    request: Request,
    db: GetDB,
):
    """
    Updates the active status of a user identified by their ID.
    Requires authentication as a sudo user.
    Accepts an action to either enable or disable the account.

    Raises:\n
        400: {detail: "INVALID_ACTION"}\n
        404: {detail: "USER_NOT_FOUND"}
    """

    if action == "enable":
        await crud.user.enable(db, user_id)
        return {"succes": "Account enabled"}
    elif action == "disable":
        await crud.user.disable(db, user_id)
        return {"succes": "Account disabled"}
    else:
        raise HTTPException(status_code=400, detail="INVALID_ACTION")


@router.get("/user", response_model=list[models.User])
@log_traffic()
async def sudo_read_all_users(
    user: SudoUser,
    params: ParametersDepends,
    request: Request,
    db: GetDB,
):
    """
    Retrieves a list of all users based on provided parameters.
    Requires authentication as a sudo user.
    Useful for viewing user information with sudo privileges.
    """

    all_users = await crud.user.get_multi(db, user, **params)
    return all_users


@router.get("/user/{user_id}", response_model=models.UserWithItems)
@log_traffic()
async def sudo_read_specific_user(
    user_id: int | UUID,
    sudo: SudoUser,
    request: Request,
    db: GetDB,
):
    """
    Retrieves information about a specific user identified by user ID.
    Requires authentication as a sudo user.

    Raises:\n
        404: {detail: "USER_NOT_FOUND"}
    """

    specific_user = await crud.user.get(db, user_id)
    if specific_user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    await specific_user.awaitable_attrs.items
    return specific_user


@router.get("/user-api-call-log", response_model=list[models.ApiCallLog])
@log_traffic()
async def read_all_api_call_logs(
    sudo: SudoUser,
    request: Request,
    mongodb: GetMongoDB,
):
    """
    Retrieves a list of all API call logs.
    Requires authentication as a sudo user.
    Useful for viewing API call history.
    """

    all_api_call_logs = await crud.mongo_crud.read_mongo_collection(
        mongodb=mongodb, collection=settings.API_CALL_LOG_COLLECTION
    )
    return [models.ApiCallLog(**log) for log in all_api_call_logs]


@router.get("/user-api-call-log/{user_id}", response_model=models.ApiCallLog)
@log_traffic()
async def read_api_call_log_from_user(
    user_id: int,
    sudo: SudoUser,
    request: Request,
    mongodb: GetMongoDB,
):
    """
    Retrieves API call logs for a specific user identified by user ID.
    Requires authentication as a sudo user.

    Raises:\n
        404: {detail: "LOGS_NOT_FOUND"}
    """

    log = await get_user_api_call_log(
        collection=mongodb[settings.API_CALL_LOG_COLLECTION], user_id=user_id
    )
    if not log:
        raise HTTPException(status_code=404, detail="LOGS_NOT_FOUND")
    return log


@router.get("/api-traffic", response_model=models.TrafficLogwithMetaData)
@log_traffic()
async def read_api_traffic(
    sudo: SudoUser,
    request: Request,
    mongodb: GetMongoDB,
):
    api_traffic = await crud.mongo_crud.read_mongo_collection(
        mongodb=mongodb, collection=settings.API_TRAFFIC_COLLECTION
    )

    api_traffic_to_schema = [models.TrafficLog(**log) for log in api_traffic]
    return {"total": len(api_traffic_to_schema), "traffic_log": api_traffic_to_schema}
