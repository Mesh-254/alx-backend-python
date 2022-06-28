#!/usr/bin/env python3
"""
:returns a random number between 0 and 10
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    :returns a random number between 0 and 10
    :return:
    :rtype:
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
