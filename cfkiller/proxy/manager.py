# cfkiller/proxy/manager.py
import asyncio
import aiohttp
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Proxy:
    url: str
    latency: float = 9999
    fails: int = 0
    alive: bool = True
    country: str = "?"

class ProxyManager:
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxies = self._load_proxies(proxy_file)
        self.lock = asyncio.Lock()

    def _load_proxies(self, file: str) -> List[Proxy]:
        if not os.path.exists(file):
            return []
        return [Proxy(url=line.strip()) for line in open(file) if line.strip()]

    async def health_check_all(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self._check_proxy(session, p) for p in self.proxies]
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _check_proxy(self, session: aiohttp.ClientSession, proxy: Proxy):
        try:
            start = asyncio.get_event_loop().time()
            async with session.get("https://api.ipify.org", proxy=proxy.url, timeout=8) as resp:
                proxy.latency = asyncio.get_event_loop().time() - start
                proxy.alive = True
                proxy.country = resp.headers.get("CF-IPCountry", "?")
        except:
            proxy.alive = False
            proxy.fails += 1

    async def get_best(self, country: str = None) -> Optional[Proxy]:
        async with self.lock:
            candidates = [p for p in self.proxies if p.alive]
            if country:
                candidates = [p for p in candidates if p.country == country]
            if not candidates:
                return None
            return min(candidates, key=lambda p: p.latency)