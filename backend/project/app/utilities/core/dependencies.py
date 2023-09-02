from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from redis import Redis  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.config import Settings, get_settings
from app.db import get_db
from app.mongodb import get_mongo_db
from app.utilities.core.auth import get_fresh_user
from app.utilities.core.auth import get_user_api_call_log
from app.utilities.core.auth import get_sudo
from app.utilities.core.auth import get_verified_user
from app.utilities.core.auth import get_user
from app.utilities.core.crud import parameters
from app.utilities.core.redis import cache


ActiveUser = Annotated[models.UserDB, Depends(get_user)]
FreshTokenUser = Annotated[models.UserDB, Depends(get_fresh_user)]
VerifiedUser = Annotated[models.UserDB, Depends(get_verified_user)]
SudoUser = Annotated[models.UserDB, Depends(get_sudo)]
UserLimitedAPICalls = Annotated[models.UserDB, Depends(get_user_api_call_log)]
GetDB = Annotated[AsyncSession, Depends(get_db)]
GetMongoDB = Annotated[AsyncIOMotorClient, Depends(get_mongo_db)]
GetSettings = Annotated[Settings, Depends(get_settings)]
ParametersDepends = Annotated[dict, Depends(parameters)]
GetCache = Annotated[Redis, Depends(cache)]
