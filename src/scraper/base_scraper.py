from abc import ABC, abstractmethod
from typing import List, Dict
import asyncio
from playwright.async_api import async_playwright

class BaseScraper(ABC):
    def __init__(self):
        self.jobs = []

    @abstractmethod
    async def scrape(self, roles: List[str], locations: List[str]) -> List[Dict]:
        pass

    async def get_browser(self, playwright):
        return await playwright.chromium.launch(headless=True)
