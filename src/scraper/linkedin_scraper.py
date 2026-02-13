import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from .base_scraper import BaseScraper
import urllib.parse

class LinkedInScraper(BaseScraper):
    async def scrape(self, roles: List[str], locations: List[str]) -> List[Dict]:
        results = []
        async with async_playwright() as p:
            browser = await self.get_browser(p)
            page = await browser.new_page()
            
            for role in roles:
                for location in locations:
                    query = f"{role} {location}"
                    encoded_query = urllib.parse.quote(query)
                    url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={urllib.parse.quote(location)}&f_TPR=r86400" # Last 24 hours
                    
                    print(f"Scraping LinkedIn for: {query}")
                    await page.goto(url)
                    await page.wait_for_timeout(5000) # Wait for initial load
                    
                    # Scroll to load more jobs
                    for _ in range(3):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)
                    
                    job_cards = await page.query_selector_all(".base-card")
                    for card in job_cards[:20]: # Limit to top 20 per query for now
                        try:
                            title = await (await card.query_selector(".base-search-card__title")).inner_text()
                            company = await (await card.query_selector(".base-search-card__subtitle")).inner_text()
                            location_text = await (await card.query_selector(".job-search-card__location")).inner_text()
                            link = await (await card.query_selector(".base-card__full-link")).get_attribute("href")
                            
                            results.append({
                                "title": title.strip(),
                                "company": company.strip(),
                                "location": location_text.strip(),
                                "link": link.split('?')[0] if link else "",
                                "source": "LinkedIn"
                            })
                        except Exception as e:
                            print(f"Error parsing job card: {e}")
                            continue
            
            await browser.close()
        return results
