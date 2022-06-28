#!/usr/bin/env python3
"""
:returns async generator time counter
"""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    :returns async generator time counter
    :return:
    :rtype:
    """
    s = time.perf_counter()
    tasks = [async_comprehension() for i in range(4)]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - s
    return elapsed
