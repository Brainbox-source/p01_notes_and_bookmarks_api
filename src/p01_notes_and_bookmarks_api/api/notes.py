from uuid import UUID

import asyncpg
from fastapi import APIRouter, HTTPException, Request

from ..db.notes import (
    fetch_all_notes,
    fetch_note,
    insert_note,
    modify_note,
    remove_note,
)
from ..schemas.note import Note, NoteEntry, NoteModification
from .dependencies import get_db_pool

# create a router specifically for notes
router = APIRouter(prefix="/notes", tags=["Notes"])

POSTGRES_ERROR = asyncpg.PostgresError


# api route and endpoint to create a note
@router.post("/", response_model=Note, status_code=201)
async def create_note(note_data: NoteEntry, request: Request):
    """create a new note"""
    pool = get_db_pool(request)

    try:
        record = await insert_note(pool, note_data)

        return dict(record)
    except POSTGRES_ERROR:
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
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to fetch notes")


# api route and endpoint to fetch a note
@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: UUID, request: Request):
    """retrieve a specific note by its id"""
    pool = get_db_pool(request)

    try:
        record = await fetch_note(pool, note_id)

        if not record:
            raise HTTPException(status_code=404, detail="note not found")

        return dict(record)
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to fetch note")


# api route and endpoint to update a note
@router.patch("/{note_id}", response_model=Note)
async def update_note(note_id: UUID, new_data: NoteModification, request: Request):
    """update a specific note"""
    pool = get_db_pool(request)

    # exclude_unset=True strips out any fields the user didn't explicitly send
    update_data = new_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="no fields provided for update.")

    try:
        record = await modify_note(pool, note_id, update_data)

        if not record:
            raise HTTPException(status_code=404, detail="note not found")

        return dict(record)
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to update note.")


# api route and endpoint to delete a note
@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: UUID, request: Request):
    """delete a spceific note"""
    pool = get_db_pool(request)

    try:
        deleted = await remove_note(pool, note_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="note not found")

        # return nothing if successful
        return
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to delete a note")
