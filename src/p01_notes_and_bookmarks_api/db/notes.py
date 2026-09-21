from uuid import UUID

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

    async with pool.acquire() as connection:
        records = await connection.fetch(query)

        return records


# db logic to fetch a single note by its ID
async def fetch_note_by_id(pool: asyncpg.Pool, note_id: UUID) -> asyncpg.Record | None:
    """fetches a single note by its uuid. returns None if not found"""

    query = """
        SELECT * FROM notes
        WHERE id = $1;
    """

    async with pool.acquire() as connection:
        record = await connection.fetchrow(query, note_id)

        return record


# db logic to update a note
async def update_note(
    pool: asyncpg.Pool, note_id: UUID, new_data: dict
) -> asyncpg.Record | None:
    """updates a note and returns the updated record. returns None if note to be updated not found."""

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


# note for gemini
# i am using Modern Python (3.10+). While from typing import Optional was the standard approach for years, the creator of FastAPI now officially recommends avoiding it in modern Python in favor of the | None syntax or Union.
# i also changed the schema name from NoteUpdate to NoteModification, and i changed update_data to new_data for the db logic
