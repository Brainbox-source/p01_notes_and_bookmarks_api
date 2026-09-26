from uuid import UUID

import asyncpg

from ..schemas.bookmark import BookmarkEntry

POOL = asyncpg.Pool
RECORD = asyncpg.Record


# db logic to insert a bookmark
async def insert_bookmark(pool: POOL, bookmark_data: BookmarkEntry) -> RECORD:
    """inserts a new bookmark into the database and returns the record."""

    query = """
        INSERT INTO bookmarks(title, url, description)
        VALUES($1, $2, $3)
        RETURNING *
    """

    # borrow a connection, run the query, and return the connection to the pool
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            query, bookmark_data.title, bookmark_data.url, bookmark_data.description
        )

        return record


# db logic to fetch all bookmarks
async def fetch_all_bookmarks(pool: POOL) -> list[RECORD]:
    """fetch all bookmarks, ordered from newest to oldest"""

    query = """
        SELECT * FROM bookmarks
        ORDER BY updated_at DESC;
    """

    async with pool.acquire() as connection:
        records = await connection.fetch(query)

        return records


# db logic to fecth a single bookmark by its ID
async def fetch_bookmark(pool: POOL, bookmark_id: UUID) -> RECORD | None:
    """fetches a single bookmark by its id. returns None if not cound"""

    query = """
        SELECT * FROM NOTES
        WHERE id = $1;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, bookmark_id)

        return record
