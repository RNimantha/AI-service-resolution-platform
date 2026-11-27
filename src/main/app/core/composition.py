"""Import-only composition example; application execution belongs to main.py."""

from src.main.app.services.rag_service import RagService, Retriever


def build_rag_service(retriever: Retriever) -> RagService:
    """Composition roots inject a real adapter when it has been implemented."""
    return RagService(retriever=retriever)
