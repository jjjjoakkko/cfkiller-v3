#!/usr/bin/env python3
import asyncio
import os
from cfkiller.core.tls.utils_client import spoofed_request

async def main():
    url = os.environ.get("TARGET") or "https://example.com"
    requests = int(os.environ.get("REQUESTS", 100))
    tasks = [spoofed_request(url) for _ in range(requests)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    successes = len([r for r in results if isinstance(r, tuple) and r[0] == 200])
    print(f"Successes: {successes} / {requests}")

if __name__ == '__main__':
    asyncio.run(main())
