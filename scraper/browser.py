"""Playwright browser manager with persistent session support."""

from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, BrowserContext, Page
from utils.config import settings
from utils.constants import SESSION_DIR
from scraper.anti_bot import random_user_agent


@asynccontextmanager
async def browser_page() -> Page:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        ua = random_user_agent()
        if settings.session_persistence:
            context: BrowserContext = await p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=settings.headless,
                user_agent=ua,
                viewport={"width": 1366, "height": 768},
            )
        else:
            browser = await p.chromium.launch(headless=settings.headless)
            context = await browser.new_context(user_agent=ua, viewport={"width": 1366, "height": 768})

        page = context.pages[0] if context.pages else await context.new_page()
        page.set_default_timeout(settings.nav_timeout_ms)
        try:
            yield page
        finally:
            await context.close()
