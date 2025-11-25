# cfkiller/core/tls/utils_client.py
try:
    from curl_cffi.requests import AsyncClient
except Exception:
    AsyncClient = None
import random
import asyncio

FINGERPRINTS = [
    "chrome_120", "chrome_124", "chrome_131",
    "firefox_128", "safari_17", "edge_131"
]

async def spoofed_request(url: str, fingerprint: str = None, proxy: str = None):
    fp = fingerprint or random.choice(FINGERPRINTS)
    timeout = 15

    if AsyncClient is None:
        raise RuntimeError("curl-cffi AsyncClient is not available. Please install curl-cffi to use spoofed_request()")

    async with AsyncClient(impersonate=fp, timeout=timeout, proxy=proxy) as client:
        try:
            resp = await client.get(url, headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            return resp.status_code, resp.headers
        except Exception as e:
            return None, str(e)
