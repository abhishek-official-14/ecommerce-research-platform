"""Resilient selector registry and fallback definitions."""

from dataclasses import dataclass


@dataclass(slots=True)
class SelectorBundle:
    primary: str
    secondary: str
    xpath: str
    text: str
    relative: str


PRODUCT_CARD = SelectorBundle(
    primary="a[href*='/product/']",
    secondary="[data-testid*='product'] a[href*='/product/']",
    xpath="xpath=//a[contains(@href, '/product/')]",
    text=r"text=/₹|Rs\./i",
    relative="xpath=//*[contains(@href, '/product/')]/ancestor::*[self::article or self::div][1]",
)

FIELD_SELECTORS = {
    "title": SelectorBundle(
        primary="h3, [data-testid*='title']",
        secondary="[aria-label*='title' i]",
        xpath="xpath=.//h3 | .//*[contains(@data-testid,'title')]",
        text="text=/[A-Za-z]{3,}/",
        relative="xpath=.//*[self::h1 or self::h2 or self::h3][1]",
    ),
    "current_price": SelectorBundle(
        primary=r"text=/₹\s*[0-9,]+/",
        secondary="[data-testid*='price']",
        xpath="xpath=.//*[contains(text(),'₹')][1]",
        text=r"text=/₹\s*[0-9,]+/",
        relative="xpath=.//*[contains(@data-testid,'price') or contains(text(),'₹')][1]",
    ),
    "original_price": SelectorBundle(
        primary="s, del, [data-testid*='mrp']",
        secondary="text=/MRP|Original/i",
        xpath="xpath=.//s | .//del",
        text=r"text=/₹\s*[0-9,]+/",
        relative="xpath=.//*[contains(@style,'line-through')][1]",
    ),
    "discount_percent": SelectorBundle(
        primary="text=/% off/i",
        secondary="[data-testid*='discount']",
        xpath="xpath=.//*[contains(translate(text(),'OFF','off'),'off') and contains(text(),'%')][1]",
        text="text=/%/",
        relative="xpath=.//*[contains(text(),'%')][1]",
    ),
    "rating": SelectorBundle(
        primary="[aria-label*='rating' i], [data-testid*='rating']",
        secondary=r"text=/\b[0-5](\.[0-9])?\b/",
        xpath="xpath=.//*[contains(@aria-label,'rating') or contains(@data-testid,'rating')][1]",
        text=r"text=/\b[0-5](\.[0-9])?\b/",
        relative="xpath=.//*[contains(text(),'★') or contains(text(),'rating')][1]",
    ),
    "review_count": SelectorBundle(
        primary=r"text=/[0-9,]+\s*(reviews|ratings)/i",
        secondary="[data-testid*='review']",
        xpath="xpath=.//*[contains(translate(text(),'REVIEWSRATINGS','reviewsratings'),'reviews') or contains(translate(text(),'REVIEWSRATINGS','reviewsratings'),'ratings')][1]",
        text=r"text=/\([0-9,]+\)/",
        relative="xpath=.//*[contains(text(),'review') or contains(text(),'rating')][1]",
    ),
    "image_url": SelectorBundle(
        primary="img",
        secondary="[data-testid*='image'] img, img[data-src]",
        xpath="xpath=.//img[1]",
        text="img",
        relative="xpath=.//*[self::picture or self::img][1]//img | .//img[1]",
    ),
}
