"""Meesho search scraping implementation for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable

from loguru import logger
from playwright.async_api import Locator, Page
from tenacity import retry, stop_after_attempt, wait_exponential

from scraper.anti_bot import human_scroll
from scraper.browser import browser_page
from scraper.selectors import FIELD_SELECTORS, PRODUCT_CARD, SelectorBundle
from utils.config import settings
from utils.constants import MEESHO_BASE_URL
from utils.delays import random_delay
from utils.validator import normalize_text


@dataclass(slots=True)
class ProductRecord:
    title: str = ""
    current_price: str = ""
    original_price: str = ""
    discount_percent: str = ""
    rating: str = ""
    review_count: str = ""
    product_url: str = ""
    image_url: str = ""


def _selector_chain(bundle: SelectorBundle) -> Iterable[str]:
    return [bundle.primary, bundle.secondary, bundle.xpath, bundle.text, bundle.relative]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=4), reraise=False)
async def safe_locator(base: Locator | Page, bundle: SelectorBundle) -> Locator | None:
    for selector in _selector_chain(bundle):
        try:
            target = base.locator(selector).first
            if await target.count() > 0:
                return target
        except Exception as exc:
            logger.debug(f"Selector failure for '{selector}': {exc}")
    return None


async def safe_get_text(base: Locator | Page, bundle: SelectorBundle) -> str:
    node = await safe_locator(base, bundle)
    if not node:
        logger.warning("All text selector fallbacks failed.")
        return ""
    try:
        text = await node.inner_text(timeout=2_500)
        return normalize_text(text)
    except Exception as exc:
        logger.warning(f"Text extraction failed: {exc}")
        return ""


async def safe_get_attribute(base: Locator | Page, bundle: SelectorBundle, attr: str) -> str:
    node = await safe_locator(base, bundle)
    if not node:
        logger.warning(f"All attribute selector fallbacks failed for {attr}.")
        return ""
    try:
        value = await node.get_attribute(attr, timeout=2_500)
        return normalize_text(value)
    except Exception:
        return ""


class MeeshoSearchScraper:
    async def search(self, keyword: str) -> list[ProductRecord]:
        query = keyword.strip().replace(" ", "%20")
        search_url = f"{MEESHO_BASE_URL}/search?q={query}"
        logger.info(f"Starting scrape for '{keyword}' => {search_url}")

        async with browser_page() as page:
            await page.goto(search_url, wait_until="domcontentloaded")
            await random_delay(settings.min_delay, settings.max_delay)
            await human_scroll(page, settings.max_scrolls)
            return await self._extract_products(page)

    async def _extract_products(self, page: Page) -> list[ProductRecord]:
        cards = await self._product_cards(page)
        products: list[ProductRecord] = []

        for idx in range(min(await cards.count(), settings.max_products)):
            card = cards.nth(idx)
            data = ProductRecord(
                title=await safe_get_text(card, FIELD_SELECTORS["title"]),
                current_price=await safe_get_text(card, FIELD_SELECTORS["current_price"]),
                original_price=await safe_get_text(card, FIELD_SELECTORS["original_price"]),
                discount_percent=await safe_get_text(card, FIELD_SELECTORS["discount_percent"]),
                rating=await safe_get_text(card, FIELD_SELECTORS["rating"]),
                review_count=await safe_get_text(card, FIELD_SELECTORS["review_count"]),
                product_url=await safe_get_attribute(card, PRODUCT_CARD, "href"),
                image_url=await safe_get_attribute(card, FIELD_SELECTORS["image_url"], "src"),
            )

            if data.product_url.startswith("/"):
                data.product_url = f"{MEESHO_BASE_URL}{data.product_url}"

            products.append(data)
            if (idx + 1) % 10 == 0:
                logger.info(f"Extracted {idx + 1} products")

        logger.info(f"Extraction complete. Collected {len(products)} product rows")
        return products

    async def _product_cards(self, page: Page) -> Locator:
        locator = await safe_locator(page, PRODUCT_CARD)
        if locator:
            return locator.locator("xpath=ancestor::*[self::div or self::article][1]")
        logger.warning("Product card selector failed. Falling back to broad container locator.")
        return page.locator("main div")


async def run_search(keyword: str) -> list[dict]:
    scraper = MeeshoSearchScraper()
    rows = await scraper.search(keyword)
    return [asdict(item) for item in rows]
