from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


# schema for incoming bookmark data
class BookmarkEntry(BaseModel):
    title: str = Field(..., max_length=255, description="the title of the bookmark")
    url: HttpUrl = Field(
        ...,
        description="the web address of the specific webpage for quick access",
    )
    description: str | None = Field(
        default=None, description="additional details for the bookmark"
    )


# schema for outgoing data when returning a bookmark
class Bookmark(BaseModel):
    id: UUID
    title: str
    url: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    # parse from asyncpg Records
    model_config = ConfigDict(from_attributes=True)
