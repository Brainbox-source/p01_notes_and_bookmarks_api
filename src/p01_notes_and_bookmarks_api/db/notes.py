import asyncpg

from ..schemas.note import NoteEntry


# db logic to insert a note
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


# db logic to fetch all notes
async def fetch_all_notes(pool: asyncpg.Pool) -> list[asyncpg.Record]:
    """fetch all notes from the database, ordered from newest to oldest"""
    query = """
        SELECT * FROM notes
        ORDER BY created_at DESC;
    """

    # borrow a connection, run the query, and return the connection to the pool
    async with pool.acquire() as connection:
        records = await connection.fetch(query)

        return records
