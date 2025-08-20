#!/usr/bin/env python3

import asyncio
import aiosqlite


async def asyncfetchusers(db_name: str = "mydatabase.db"):
    """
    Fetch all users asynchronously
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def asyncfetcholder_users(db_name: str = "mydatabase.db"):
    """
    Fetch users older than 40 asynchronously
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """
    Run both queries concurrently and print results
    """
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
