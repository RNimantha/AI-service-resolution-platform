"""Framework-independent text document for the RAG ingestion pipeline."""

from dataclasses import dataclass

MAX_DOCUMENT_TITLE_CHARACTERS = 200
MAX_DOCUMENT_CHARACTERS = 100_000
DOCUMENT_PREVIEW_CHARACTERS = 200


@dataclass(frozen=True, slots=True)
class Document:
    """Preserve source text; validation also applies to non-HTTP callers."""

    document_id: str
    title: str
    content: str
    source: str

    def __post_init__(self) -> None:
        for name in ("document_id", "title", "content", "source"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if len(self.title) > MAX_DOCUMENT_TITLE_CHARACTERS:
            raise ValueError(f"title must not exceed {MAX_DOCUMENT_TITLE_CHARACTERS} characters")
        if len(self.content) > MAX_DOCUMENT_CHARACTERS:
            raise ValueError(f"content must not exceed {MAX_DOCUMENT_CHARACTERS} characters")

    @property
    def character_count(self) -> int:
        return len(self.content)

    @property
    def word_count(self) -> int:
        """Count whitespace-separated units, not tokenizer tokens."""
        return len(self.content.split())

    @property
    def preview(self) -> str:
        return self.content[:DOCUMENT_PREVIEW_CHARACTERS]
