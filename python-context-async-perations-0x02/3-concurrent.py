#!/usr/bin/env python3

import asyncio
import aiosqlite


async def async_fetch_users():
    # Fetch users from the database
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            for row in users:
                print(row)
            return users


async def async_fetch_older_users():
    # Fetch older users from the database
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            for row in users:
                print(row)
            return users


async def fetch_concurrently():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )


asyncio.run(fetch_concurrently())
