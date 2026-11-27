"""A retrieved passage with identifiers for source attribution."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    """An adapter returns only passages permitted for the request context."""

    document_id: str
    chunk_id: str
    text: str
    score: float | None = None
