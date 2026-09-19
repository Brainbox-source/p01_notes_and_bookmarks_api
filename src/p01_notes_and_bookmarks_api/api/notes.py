import asyncpg
from fastapi import APIRouter, HTTPException, Request

from ..db.notes import insert_note
from ..schemas.note import Note, NoteEntry

# create a router specifically for notes
router = APIRouter(prefix="/notes", tags=["Notes"])


# dependency to get the database pool
def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool


@router.post("/", response_model=Note, status_code=201)
async def create_note(note_data: NoteEntry, request: Request):
    """create a new note"""
    pool = get_db_pool(request)

    try:
        record = await insert_note(pool, note_data)
        return dict(record)
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="failed to create a note")
