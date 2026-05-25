"""CSV export module."""

from pathlib import Path
import pandas as pd

from utils.constants import EXPORT_FIELDS
from utils.helpers import ensure_parent


def export_csv(rows: list[dict], output_path: Path) -> Path:
    ensure_parent(output_path)
    frame = pd.DataFrame(rows)
    for field in EXPORT_FIELDS:
        if field not in frame.columns:
            frame[field] = ""
    frame = frame[EXPORT_FIELDS]
    frame.to_csv(output_path, index=False)
    return output_path
