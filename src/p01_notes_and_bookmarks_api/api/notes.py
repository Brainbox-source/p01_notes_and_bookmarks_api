from uuid import UUID

import asyncpg
from fastapi import APIRouter, HTTPException, Request

from ..db.notes import fetch_all_notes, fetch_note_by_id, insert_note
from ..schemas.note import Note, NoteEntry

# create a router specifically for notes
router = APIRouter(prefix="/notes", tags=["Notes"])


# dependency to get the database pool
def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool


# api route and endpoint to create a note
@router.post("/", response_model=Note, status_code=201)
async def create_note(note_data: NoteEntry, request: Request):
    """create a new note"""
    pool = get_db_pool(request)

    try:
        record = await insert_note(pool, note_data)
        return dict(record)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="failed to create a note")


# api route and endpoint to fetch all notes
@router.get("/", response_model=list[Note])
async def get_all_notes(request: Request):
    """retrieve all notes"""
    pool = get_db_pool(request)

    try:
        records = await fetch_all_notes(pool)
        # convert the list of asyncpg.Records into a list of standard dictionaries
        return [dict(record) for record in records]
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="failed to fetch notes")


# api route and endpoint to fetch a single note
@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: UUID, request: Request):
    """retrieve a specific note by its id"""
    pool = get_db_pool(request)

    try:
        record = await fetch_note_by_id(pool, note_id)

        if not record:
            raise HTTPException(status_code=404, detail="note not found")

        return dict(record)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="failed to fetch note")
