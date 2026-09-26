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
            query,
            bookmark_data.title,
            str(bookmark_data.url),
            bookmark_data.description,
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


# db logic to fecth a bookmark by its ID
async def fetch_bookmark(pool: POOL, bookmark_id: UUID) -> RECORD | None:
    """fetches a single bookmark by its id. returns None if not cound"""

    query = """
        SELECT * FROM bookmarks
        WHERE id = $1;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, bookmark_id)

        return record


# db logic to modify a bookmark
async def modify_bookmark(
    pool: POOL, bookmark_id: UUID, new_data: dict
) -> RECORD | None:
    """modifies a bookmark and returns the updated record. returns None if bookmark to be modified not found."""

    query = """
        UPDATE bookmarks
        SET
            title = COALESCE($1, title),
            url = COALESCE($2, url),
            description = COALESCE($3, description),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = $4
        RETURNING *;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            query,
            new_data.get("title"),
            str(new_data.get("url")),
            new_data.get("description"),
            bookmark_id,
        )

        return record


# db logic to delete a bookmark
async def remove_bookmark(pool: POOL, bookmark_id: UUID) -> bool:
    """deletes a bookmark by its id. returns True if deleted, False if not found."""

    query = """
        DELETE FROM bookmarks
        WHERE id = $1
        RETRUNING id:
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, bookmark_id)

        return record is not None
