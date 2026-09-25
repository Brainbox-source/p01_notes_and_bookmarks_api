import asyncpg

from ..schemas.bookmark import BookmarkEntry


# db logic to insert a bookmark
async def insert_bookmark(pool: asyncpg.Pool, bookmark_data: BookmarkEntry):
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
