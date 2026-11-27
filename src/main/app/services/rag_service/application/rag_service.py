"""Application entry point that receives a retrieval dependency explicitly."""

from src.main.app.services.rag_service.domain.retrieval_query import RetrievalQuery
from src.main.app.services.rag_service.domain.retrieved_chunk import RetrievedChunk
from src.main.app.services.rag_service.ports.retriever import Retriever
from src.main.app.shared.contracts import RequestContext


class RagService:
    """Compose retrieval without assuming a provider or opening network clients."""

    def __init__(self, retriever: Retriever) -> None:
        self._retriever = retriever

    async def retrieve(
        self, *, query: RetrievalQuery, context: RequestContext
    ) -> tuple[RetrievedChunk, ...]:
        """Delegate with verified scope; authorization belongs in the real adapter."""
        return await self._retriever.retrieve(query=query, context=context)
