"""HTTP representation of a validated transient document."""

from pydantic import BaseModel


class DocumentPreviewResponse(BaseModel):
    document_id: str
    title: str
    source: str
    character_count: int
    word_count: int
    preview: str
