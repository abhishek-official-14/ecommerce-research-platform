"""Delay helpers for anti-bot pacing."""

import asyncio
import random


async def random_delay(min_delay: float, max_delay: float) -> None:
    await asyncio.sleep(random.uniform(min_delay, max_delay))
