"""Shared helper functions."""

from pathlib import Path
from datetime import datetime


def timestamped_filename(prefix: str, ext: str) -> str:
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{stamp}.{ext}"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
