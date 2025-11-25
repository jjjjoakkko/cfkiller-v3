# cfkiller/core/browser/manager.py
import undetected_playwright as upw
from playwright.async_api import async_playwright
import asyncio

class BrowserPool:
    def __init__(self, pool_size: int = 80):
        self.pool_size = pool_size
        self.semaphore = asyncio.Semaphore(pool_size)
        self.playwright = None

    async def start(self):
        self.playwright = await upw.playwright.start()

    async def stop(self):
        if self.playwright:
            await self.playwright.stop()

    async def visit(self, url: str, proxy: str = None):
        async with self.semaphore:
            browser = await self.playwright.chromium.launch(
                headless=True,
                proxy={"server": proxy} if proxy else None
            )
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            # stealth plugin
            await context.add_init_script(path="stealth.min.js")

            page = await context.new_page()
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(1000 + random.randint(0, 2000))
            except:
                pass
            finally:
                await context.close()
                await browser.close()