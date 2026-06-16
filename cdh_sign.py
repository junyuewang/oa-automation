"""大恒光电每日签到 - 9:00-10:00随机执行"""
import asyncio, random
from playwright.async_api import async_playwright

CDH_USER = "junyuewang"
CDH_PASS = "T#0808am"

async def sign():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])
        page = await browser.new_page(viewport={"width": 1440, "height": 900}); page.set_default_timeout(15000)
        try:
            await page.goto("https://www.cdhbuy.com/login/login", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)
            await page.fill("input[placeholder*='用户名']", CDH_USER)
            await page.fill("input[placeholder*='密码']", CDH_PASS)
            await page.locator("button:visible:has-text('登录')").click(); await asyncio.sleep(5)
            await page.locator("a:has-text('签到')").first.click(); await asyncio.sleep(3)
            btn = page.locator("a:has-text('立即签到')").first
            if await btn.count() > 0:
                await btn.click(); await asyncio.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    delay = random.randint(0, 59) * 60 + random.randint(0, 59)
    import time; time.sleep(delay)
    asyncio.run(sign())
