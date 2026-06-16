"""OA 采购验收会签脚本 - 依次用 tianhuiru 和 duxueyan 登录提交"""
import asyncio
from playwright.async_api import async_playwright

ACCOUNTS = [
    {"name": "tianhuiru", "user": "tianhuiru", "pass": "THR@1234"},
    {"name": "duxueyan",  "user": "duxueyan",  "pass": "dxy123456"},
]
OA_URL = "http://172.16.3.16/wui/index.html?#/?_key=k99ufk"

async def submit_acceptance(account):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page(); page.set_default_timeout(15000)
        name, user, pwd = account["name"], account["user"], account["pass"]
        print(f"\n[{name}] 登录...")
        await page.goto(OA_URL, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        await page.fill("#loginid", user); await page.fill("#userpassword", pwd)
        await page.click("button:has-text('登 录')"); await asyncio.sleep(6)
        print(f"[{name}] 查找验收表...")
        await asyncio.sleep(2)
        link = page.locator("a:has-text('采购验收流程')")
        if await link.count() == 0: await browser.close(); return False
        async with context.expect_page(timeout=15000) as npi: await link.first.click()
        fp = await npi.value; await fp.wait_for_load_state("networkidle"); await asyncio.sleep(4)
        print(f"[{name}] 提交...")
        await fp.locator("button:has-text('提 交')").first.click(); await asyncio.sleep(2)
        modal = fp.locator(".ant-modal:visible")
        await modal.wait_for(state="visible", timeout=8000)
        await modal.first.locator("button:has-text('确 定')").first.click()
        print(f"  ✓ {name} 会签完成")
        await asyncio.sleep(3); await browser.close(); return True

async def main():
    for acc in ACCOUNTS:
        await submit_acceptance(acc); await asyncio.sleep(2)
    print("\n✅ 所有会签完成!")

if __name__ == "__main__": asyncio.run(main())
