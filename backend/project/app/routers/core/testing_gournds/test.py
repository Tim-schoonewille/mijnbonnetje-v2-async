import pickle
from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app import models
from app.mongodb import get_mongo_db
from app.crud.mongodb.mongo_crud import read_mongo_collection
from app.config import PROXY_IPS, settings
from app.utilities.core.auth import get_user_api_call_log
from app.utilities.get_proxy import ProxyInCache, get_working_proxy
from app.utilities.core.dependencies import GetAsyncCache, VerifiedUser


router = APIRouter(prefix=f"{settings.URL_PREFIX}/test", tags=["test"])


@router.get("/api-call-log-limit")
async def mongo_request_limit_get(
    user: Annotated[models.UserDB, Depends(get_user_api_call_log)],
):
    """Test route te check wether the the amount of API requests is limited"""
    return {"hello": "world"}


@router.get("/get-collection")
async def read_collection(
    collection: str, mongodb: AsyncIOMotorClient = Depends(get_mongo_db)
):
    all_ = await read_mongo_collection(mongodb=mongodb, collection=collection)
    results = [models.ApiCallLog(**result) for result in all_]
    return results


@router.get('/test-proxy')
async def test_proxy(proxy: str = '185.162.229.188:80'):
    new_proxy = ProxyInCache(proxy)
    print(proxy)
    print(await new_proxy.test_proxy())
    return [1]


@router.get('/test-proxy-cache-return')
async def test_proxy_cache_return(
    user: VerifiedUser,
    cache: GetAsyncCache,
):
    proxies_pickled = await cache.get('proxies')
    if proxies_pickled is None:
        return {'error': 'no proxies in cache'}
    proxies = pickle.loads(proxies_pickled)
    ip = await get_working_proxy(cache)
    return ip


@router.get('/test-working-proxy-list-in-cache')
async def test_working_proxy_list_in_cache(user: VerifiedUser, cache: GetAsyncCache):
    proxies_pickled = await cache.get('proxies')
    if proxies_pickled is None:
        return {'error': 'no proxies in cache'}
    proxies = pickle.loads(proxies_pickled)
    print(proxies)
    return proxies