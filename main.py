"""CLI entrypoint for Phase 1 scraping pipeline."""

import argparse
import asyncio
from pathlib import Path

from loguru import logger

from exports.csv_export import export_csv
from exports.json_export import export_json
from scraper.search_scraper import run_search
from utils.constants import DATA_DIR
from utils.helpers import timestamped_filename
from utils.logger import setup_logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Meesho ecommerce intelligence scraper (Phase 1)")
    parser.add_argument("--keyword", required=True, help="Search keyword, e.g. 'mobile holder'")
    return parser.parse_args()


async def async_main() -> None:
    args = parse_args()
    setup_logger()
    rows = await run_search(args.keyword)

    csv_path = DATA_DIR / timestamped_filename(f"meesho_{args.keyword.replace(' ', '_')}", "csv")
    json_path = Path(str(csv_path).replace(".csv", ".json"))

    export_csv(rows, csv_path)
    export_json(rows, json_path)

    logger.info(f"Export complete: CSV={csv_path}")
    logger.info(f"Export complete: JSON={json_path}")


if __name__ == "__main__":
    asyncio.run(async_main())
