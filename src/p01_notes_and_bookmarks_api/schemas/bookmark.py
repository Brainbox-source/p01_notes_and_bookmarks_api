from pydantic import BaseModel, Field


# schema for incoming bookmark data
class BookmarkEntry(BaseModel):
    title: str = Field(..., max_length=255, description="the title of the bookmark")
    url: str = Field(
        ...,
        max_length=2083,
        description="the web address of the specific webpage for quick access",
    )
    description: str | None = Field(
        default=None, description="additional details for the bookmark"
    )
