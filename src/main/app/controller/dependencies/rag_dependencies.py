"""HTTP dependency wiring for the first RAG ingestion component."""

from src.main.app.services.rag_service import TextDocumentLoader


def get_text_document_loader() -> TextDocumentLoader:
    """Provide the stateless loader without initializing models or databases."""
    return TextDocumentLoader()
