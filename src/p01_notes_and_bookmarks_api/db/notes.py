from uuid import UUID

import asyncpg

from ..schemas.note import NoteEntry

POOL = asyncpg.Pool
RECORD = asyncpg.Record


# db logic to insert a note
async def insert_note(pool: POOL, note_data: NoteEntry) -> RECORD:
    """inserts a new note into the database and returns the created record."""

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
async def fetch_all_notes(pool: POOL) -> list[RECORD]:
    """fetch all notes, ordered from newest to oldest"""

    query = """
        SELECT * FROM notes
        ORDER BY updated_at DESC;
    """

    async with pool.acquire() as connection:
        records = await connection.fetch(query)

        return records


# db logic to fetch a note by its ID
async def fetch_note(pool: POOL, note_id: UUID) -> RECORD | None:
    """fetches a single note by its id. returns None if not found"""

    query = """
        SELECT * FROM notes
        WHERE id = $1;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, note_id)

        return record


# db logic to modify a note
async def modify_note(pool: POOL, note_id: UUID, new_data: dict) -> RECORD | None:
    """modifies a note and returns the updated record. returns None if note to be modified not found."""

    query = """
        UPDATE notes
        SET
            title = COALESCE($1, title),
            content = COALESCE($2, content),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = $3
        RETURNING *;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            query, new_data.get("title"), new_data.get("content"), note_id
        )

        return record


# db logic to delete a note
async def remove_note(pool: POOL, note_id: UUID) -> bool:
    """deletes a note by its id. returns True if deleted, False if not found."""

    query = """
        DELETE FROM notes
        WHERE id = $1
        RETURNING id;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, note_id)
        # if record was not None, a row was actually deleted
        return record is not None
