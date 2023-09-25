import pickle
import httpx

from redis.asyncio import Redis as AsyncRedis

from app.config import CachedItemPrefix


class ProxyInCache:
    def __init__(self, ip_with_port: str):
        self.ip_with_port: str = ip_with_port
        self.total_calls = 0

    def __repr__(self) -> str:
        return f'http://{self.ip_with_port}'

    def increment_total_calls(self) -> None:
        self.total_calls += 1

    async def test_proxy(self) -> bool:
        # 189.232.115.108:8080
        proxies = {
            'http://': f'http://{self.ip_with_port}',
            'https://': f'http://{self.ip_with_port}',
        }

        endpoint = 'https://jsonplaceholder.typicode.com/todos/1'
        ip_endpoint = 'https://api.ipify.org?format=json'
        ipv4 = 'http://ipv4.icanhazip.com'
        accepted_status_codes = [200, 201, 202, 203, 204, 205]
        async with httpx.AsyncClient(proxies=proxies, verify=True) as client:
            response = await client.get(ipv4, timeout=10)
            print(response.text)
            if response.status_code in accepted_status_codes:
                return True
        return False


async def get_working_proxy(cache: AsyncRedis, proxy_ips: list[str]) -> str:
    for proxy in proxy_ips:
        cached_proxy = await get_proxy_from_cache(cache=cache, proxy_ip=proxy)
        if cached_proxy is None:
            cached_proxy = await create_cached_proxy(cache=cache, proxy_ip=proxy)
        if cached_proxy.total_calls == 5:
            continue
        cached_proxy.increment_total_calls()
        print('total amount called:', cached_proxy.total_calls)
        await update_proxy_in_cache(cache=cache, proxy_object=cached_proxy)
        return cached_proxy.ip_with_port


async def get_proxy_from_cache(cache: AsyncRedis, proxy_ip: str) -> ProxyInCache | None:
    pickled_proxy_in_cache = await cache.get(f'{CachedItemPrefix.PROXY_IP}{proxy_ip}')
    if pickled_proxy_in_cache is None:
        return None
    print('DEBUG GET PROXY, THIS IS PICKLED:', pickled_proxy_in_cache)
    proxy_in_cache = pickle.loads(pickled_proxy_in_cache)
    print('DEBUG UNPICKLED PROXY IN CACHE:', proxy_in_cache)
    return proxy_in_cache


async def create_cached_proxy(cache: AsyncRedis, proxy_ip: str) -> ProxyInCache:
    new_proxy_in_cache = ProxyInCache(ip_with_port=proxy_ip)
    print('DEBUG CREATE PROXY IN CACHE', new_proxy_in_cache)

    await cache.set(
        name=f'{CachedItemPrefix.PROXY_IP}{proxy_ip}',
        value=pickle.dumps(new_proxy_in_cache),
        ex=3600
    )

    return new_proxy_in_cache


async def update_proxy_in_cache(cache: AsyncRedis, proxy_object: ProxyInCache) -> None:
    ttl_from_proxy_in_cache = await cache.ttl(f'{CachedItemPrefix.PROXY_IP}{proxy_object.ip_with_port}')
    print(ttl_from_proxy_in_cache)
    await cache.set(
        name=f'{CachedItemPrefix.PROXY_IP}{proxy_object.ip_with_port}',
        value=pickle.dumps(proxy_object),
        ex=ttl_from_proxy_in_cache
    )
