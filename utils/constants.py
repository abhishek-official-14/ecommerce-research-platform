"""Application constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
SESSION_DIR = BASE_DIR / "data" / "session"

MEESHO_BASE_URL = "https://www.meesho.com"
DEFAULT_TIMEOUT_MS = 30_000
EXPORT_FIELDS = [
    "title",
    "current_price",
    "original_price",
    "discount_percent",
    "rating",
    "review_count",
    "product_url",
    "image_url",
]
