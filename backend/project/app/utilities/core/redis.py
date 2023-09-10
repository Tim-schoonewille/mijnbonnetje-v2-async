import pickle
from functools import wraps
from uuid import UUID

from fastapi import HTTPException
from redis import Redis  # type: ignore

from app.config import settings, CachedItemPrefix


def cache():
    return Redis(host="localhost", port="6379", password=settings.REDIS_PASSWORD)


def get_cached_attempts(id: int | str | UUID, key_prefix: str, client: Redis):
    key = f"{key_prefix}_{id}"
    attempts = client.get(key)
    return pickle.loads(attempts) if attempts else 0


def register_attempt_to_cache(
    id: int | str | UUID,
    key_prefix: str,
    current_attempts: int,
    ex: int,
    client: Redis,
) -> int:
    key = f"{key_prefix}_{id}"
    current_attempts += 1
    client.set(key, pickle.dumps(current_attempts), ex=ex)
    return current_attempts


def redis_login_attempts(id: int | UUID, client: Redis):
    return get_cached_attempts(
        id=id, key_prefix=settings.REDIS_LOGIN_PREFIX, client=client
    )


def register_login_attempt(
    id: int | UUID,
    current_attempts: int,
    client: Redis,
):
    return register_attempt_to_cache(
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


def get_cached_item(
    cache: Redis,
    prefix: CachedItemPrefix,
    id: int | UUID,
    user_id: int | UUID | None = None,
):
    """ Helper function to receive an item from cache"""
    cached_item = cache.get(f'{prefix}{id}')
    if not cached_item:
        return
    cached_item = pickle.loads(cached_item)
    if not user_id:
        return cached_item
    if cached_item.user_id != user_id:
        raise HTTPException(status_code=403, detail="ACCESS_DENIED")
    return cached_item