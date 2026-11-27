"""Load submitted text into the RAG document model without persistence."""

from uuid import uuid4

from src.main.app.services.rag_service.domain.document import Document


class TextDocumentLoader:
    """Each load creates a transient document; it does not write to storage."""

    def load(self, *, title: str, content: str) -> Document:
        if not isinstance(title, str):
            raise ValueError("title must be a non-empty string")
        return Document(
            document_id=str(uuid4()),
            title=title.strip(),
            content=content,
            source="inline",
        )
