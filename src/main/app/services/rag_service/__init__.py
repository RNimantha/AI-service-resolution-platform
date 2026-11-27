"""Public entry point for RAG components; importing does not initialize providers."""

from src.main.app.services.rag_service.application.rag_service import RagService
from src.main.app.services.rag_service.domain.document import (
    MAX_DOCUMENT_CHARACTERS,
    MAX_DOCUMENT_TITLE_CHARACTERS,
    Document,
)
from src.main.app.services.rag_service.domain.retrieval_query import RetrievalQuery
from src.main.app.services.rag_service.domain.retrieved_chunk import RetrievedChunk
from src.main.app.services.rag_service.ingestion.text_document_loader import TextDocumentLoader
from src.main.app.services.rag_service.ports.retriever import Retriever

__all__ = [
    "MAX_DOCUMENT_CHARACTERS",
    "MAX_DOCUMENT_TITLE_CHARACTERS",
    "Document",
    "RagService",
    "RetrievalQuery",
    "RetrievedChunk",
    "Retriever",
    "TextDocumentLoader",
]
