"""Validation and normalization utilities."""

import re


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split()).strip()


def parse_number(value: str | None) -> float | None:
    if not value:
        return None
    cleaned = re.sub(r"[^0-9.]", "", value)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None
