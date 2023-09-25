import httpx
import asyncio
import os


class ProxyScanner:
    def __init__(self, proxy_file: str, api_endpoint: str):
        self.proxy_file: str = proxy_file
        self.untested_proxies: list[str] = self.fetch_proxies_from_file()
        self.working_proxies: list[str] = []
        self.api_endpoint = api_endpoint
        self.accepted_status_codes = [200, 201, 202, 203, 204, 205]

    def fetch_proxies_from_file(self) -> list[str]:
        print(os.getcwd())
        with open('./app/tasks/utils/proxies.txt', "r") as f:
            return [proxy.strip() for proxy in f.readlines()]

    async def test_proxy(self, proxy: str) -> bool:
        print(f"[...] Testing proxy: {proxy}")
        proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"}
        async with httpx.AsyncClient(
            proxies=proxies, verify=True  # type: ignore
        ) as client:
            try:
                response = await client.get(self.api_endpoint, timeout=3)
                print(f"[-] {proxy} status - code: {response.status_code}")
                if response.status_code in self.accepted_status_codes:
                    self.working_proxies.append(proxy)
                    return True
            except Exception:
                # print(f'[??] Proxy: {proxy} failed with error {e}')
                return False
        return False

    async def test_all_proxies(self):
        tasks = [self.test_proxy(proxy) for proxy in self.untested_proxies]
        results = await asyncio.gather(*tasks)
        return results

    def extract_working_proxies(self):
        with open("working_proxies.txt", "a") as file:
            file.writelines(
                [f"{working_proxy}\n" for working_proxy in self.working_proxies]
            )