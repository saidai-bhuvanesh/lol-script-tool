import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from .base_scraper import BaseScraper

class RemoteOkScraper(BaseScraper):
    async def scrape(self, roles: List[str], locations: List[str]) -> List[Dict]:
        results = []
        async with async_playwright() as p:
            browser = await self.get_browser(p)
            page = await browser.new_page()
            
            url = "https://remoteok.com/remote-jobs"
            print(f"Scraping RemoteOK")
            await page.goto(url)
            await page.wait_for_timeout(5000)
            
            job_rows = await page.query_selector_all("tr.job")
            for row in job_rows[:30]:
                try:
                    title = await (await row.query_selector("h2")).inner_text()
                    company = await (await row.query_selector("h3")).inner_text()
                    location_text = "Remote" # Usually remoteok is remote
                    # Get link
                    link_el = await row.query_selector("a.preventLink")
                    link = await link_el.get_attribute("href") if link_el else ""
                    if link and not link.startswith("http"):
                        link = "https://remoteok.com" + link
                    
                    # Filter by role keywords
                    if any(role.lower() in title.lower() for role in roles):
                        results.append({
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": location_text,
                            "link": link,
                            "source": "RemoteOK"
                        })
                except Exception as e:
                    print(f"Error parsing RemoteOK row: {e}")
                    continue
            
            await browser.close()
        return results
