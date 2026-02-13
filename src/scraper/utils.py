from playwright.async_api import async_playwright

async def fetch_job_description(url: str) -> str:
    if not url:
        return ""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(2000)
            
            # Simple heuristic: get all text from body or specific selectors
            content = await page.evaluate("document.body.innerText")
            await browser.close()
            return content[:5000] # Limit to 5000 chars
    except Exception as e:
        print(f"Error fetching description from {url}: {e}")
        return ""
