import asyncpg

from ..schemas.note import NoteEntry


async def insert_note(pool: asyncpg.Pool, note_data: NoteEntry) -> asyncpg.Record:
    """Inserts a new note into the database and returns the created record."""

    query = """
        INSERT INTO notes(title, content)
        VALUES($1, $2)
        RETURNING *;
    """

    # borrow a connection, run the query, and return the connection to the pool
    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, note_data.title, note_data.content)

        return record
