"""Anti-bot safe utilities and human-like browsing behavior."""

from fake_useragent import UserAgent
from playwright.async_api import Page
from tenacity import retry, stop_after_attempt, wait_random
from loguru import logger
import random


def random_user_agent() -> str:
    try:
        return UserAgent().random
    except Exception:
        logger.warning("Failed to generate fake UA; using safe fallback.")
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


@retry(stop=stop_after_attempt(3), wait=wait_random(min=0.5, max=1.8), reraise=True)
async def human_scroll(page: Page, max_scrolls: int) -> None:
    previous_height = 0
    for idx in range(max_scrolls):
        step = random.randint(500, 1300)
        await page.mouse.wheel(0, step)
        await page.wait_for_timeout(random.randint(500, 1400))
        current_height = await page.evaluate("document.body.scrollHeight")
        logger.debug(f"Scroll {idx + 1}/{max_scrolls} | height={current_height}")
        if current_height <= previous_height:
            await page.wait_for_timeout(900)
        previous_height = current_height
