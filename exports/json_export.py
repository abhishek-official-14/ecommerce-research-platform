"""JSON export module."""

from pathlib import Path
import json

from utils.helpers import ensure_parent


def export_json(rows: list[dict], output_path: Path) -> Path:
    ensure_parent(output_path)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
    return output_path
