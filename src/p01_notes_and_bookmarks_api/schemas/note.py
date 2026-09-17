from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# schema for incoming data when creating a note
class NoteCreate(BaseModel):
    title: str = Field(..., max_length=255, description="The title of the note")
    content: str = Field(..., description="The main body of the note")


# schema for outgoing data when returning a note
class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    # pydantic v2 configuration to allow parsing from asyncpg Records
    model_config = ConfigDict(from_attributes=True)
