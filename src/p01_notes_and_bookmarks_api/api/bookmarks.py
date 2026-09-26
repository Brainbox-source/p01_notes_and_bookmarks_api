import asyncpg
from fastapi import APIRouter, HTTPException, Request

from ..db.bookmarks import fetch_all_bookmarks, insert_bookmark
from ..schemas.bookmark import Bookmark, BookmarkEntry
from .dependencies import get_db_pool

# router specifically for bookmarks
router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

POSTGRES_ERROR = asyncpg.PostgresError


# api route and endpoint to create a bookmark
@router.post("/", response_model=Bookmark, status_code=201)
async def create_bookmark(bookmark_data: BookmarkEntry, request: Request):
    """create a new bookmark"""
    pool = get_db_pool(request)

    try:
        record = await insert_bookmark(pool, bookmark_data)

        return dict(record)
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to create a bookmark")


# api route and endpoint to fetch all bookmarks
@router.get("/", response_model=list[Bookmark])
async def get_all_bookmarks(request: Request):
    """retrieve all bookmarks"""
    pool = get_db_pool(request)

    try:
        records = await fetch_all_bookmarks(pool)

        return [dict(record) for record in records]
    except POSTGRES_ERROR:
        raise HTTPException(status_code=500, detail="failed to fetch all bookmarks")
