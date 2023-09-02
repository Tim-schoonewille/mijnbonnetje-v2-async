from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from app.config import Settings
from app.config import get_settings
from app.config import settings

from app.utilities.core.log import log_traffic


router = APIRouter(prefix=f"{settings.URL_PREFIX}/health", tags=["health-check"])


@router.get("/ping")
@log_traffic()
async def pong(request: Request, settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.ENVIRONMENT,
        "testing": settings.TESTING,
    }
