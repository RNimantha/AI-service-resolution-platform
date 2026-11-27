"""Transport validation for the inline document preview endpoint."""

from pydantic import BaseModel, ConfigDict, Field

from src.main.app.services.rag_service import (
    MAX_DOCUMENT_CHARACTERS,
    MAX_DOCUMENT_TITLE_CHARACTERS,
)


class DocumentPreviewRequest(BaseModel):
    """Accept only a title and bounded text, with no filesystem or URL input."""

    model_config = ConfigDict(extra="forbid", strict=True)

    title: str = Field(min_length=1, max_length=MAX_DOCUMENT_TITLE_CHARACTERS)
    content: str = Field(min_length=1, max_length=MAX_DOCUMENT_CHARACTERS)
