#!/usr/bin/env python3
import asyncio
import aiosqlite


async def async_fetch_users(db_name="mydatabase.db"):
    """Fetch all users asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users(db_name="mydatabase.db"):
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", results[0])
    print("Users older than 40:", results[1])


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
