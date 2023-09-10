import pickle
from functools import wraps
from uuid import UUID

from fastapi import HTTPException
from redis import Redis  # type: ignore
from redis import asyncio as aioredis
from redis.asyncio import Redis as AsyncRedis

from app.config import settings, CachedItemPrefix


def cache():
    return Redis(host="localhost", port="6379", password=settings.REDIS_PASSWORD)


async def async_cache():
    redis = aioredis.from_url(f'redis://:{settings.REDIS_PASSWORD}@localhost:6379')
    async with redis.client() as client:
        yield client


async def get_cached_attempts(id: int | str | UUID, key_prefix: str, client: AsyncRedis):
    key = f"{key_prefix}_{id}"
    attempts = await client.get(key)
    return pickle.loads(attempts) if attempts else 0


async def register_attempt_to_cache(
    id: int | str | UUID,
    key_prefix: str,
    current_attempts: int,
    ex: int,
    client: AsyncRedis,
) -> int:
    key = f"{key_prefix}_{id}"
    current_attempts += 1
    await client.set(key, pickle.dumps(current_attempts), ex=ex)
    return current_attempts


async def redis_login_attempts(id: int | UUID, client: AsyncRedis):
    return await get_cached_attempts(
        id=id, key_prefix=settings.REDIS_LOGIN_PREFIX, client=client
    )


async def register_login_attempt(
    id: int | UUID,
    current_attempts: int,
    client: AsyncRedis,
):
    return await register_attempt_to_cache(
        id=id,
        key_prefix=settings.REDIS_LOGIN_PREFIX,
        current_attempts=current_attempts,
        ex=settings.LOGIN_LOCKOUT_TIME,
        client=client,
    )


def cache_item(prefix: CachedItemPrefix, id_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            item_id = kwargs.get(id_name)
            client = cache()
            cached_item = client.get(prefix + str(item_id))
            if cached_item:
                return pickle.loads(cached_item)
            result = await func(*args, **kwargs)
            client.set(
                name=f"{prefix}{item_id}",
                value=pickle.dumps(result),
                ex=settings.CACHE_EXPIRATION_TIME,
            )
            return result

        return wrapper

    return decorator


async def get_cached_item(
    cache: AsyncRedis,
    prefix: CachedItemPrefix,
    id: int | UUID,
    user_id: int | UUID | None = None,
):
    """ Helper function to receive an item from cache"""
    cached_item = await cache.get(f'{prefix}{id}')
    if not cached_item:
        return
    cached_item = pickle.loads(cached_item)
    if not user_id:
        return cached_item
    if cached_item.user_id != user_id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return cached_item



# import asyncio
# from redis import asyncio as aioredis


# async def main() -> None:
#     redis = aioredis.from_url('redis://:REDIS_PASSWORD@localhost:6379')
#     async with redis.client() as conn:
#         await conn.set('async-key', 'async-value', ex=400)
#         value = await conn.get('async-key')
#     print('Value of async key "async-key" is: ', value)
#     return None


# if __name__ == '__main__':
#     asyncio.run(main())