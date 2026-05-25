"""Configuration management using environment variables."""

from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(slots=True)
class Settings:
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    max_products: int = int(os.getenv("MAX_PRODUCTS", "60"))
    max_scrolls: int = int(os.getenv("MAX_SCROLLS", "25"))
    min_delay: float = float(os.getenv("MIN_DELAY", "0.7"))
    max_delay: float = float(os.getenv("MAX_DELAY", "2.1"))
    nav_timeout_ms: int = int(os.getenv("NAV_TIMEOUT_MS", "45000"))
    session_persistence: bool = os.getenv("SESSION_PERSISTENCE", "true").lower() == "true"


settings = Settings()
