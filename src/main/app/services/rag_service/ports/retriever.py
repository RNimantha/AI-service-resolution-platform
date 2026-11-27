"""Interface for a retrieval adapter owned by rag_service."""

from typing import Protocol

from src.main.app.services.rag_service.domain.retrieval_query import RetrievalQuery
from src.main.app.services.rag_service.domain.retrieved_chunk import RetrievedChunk
from src.main.app.shared.contracts import RequestContext


class Retriever(Protocol):
    """Providers must enforce scope, freshness, and the query result limit."""

    async def retrieve(
        self, *, query: RetrievalQuery, context: RequestContext
    ) -> tuple[RetrievedChunk, ...]:
        """Retrieve evidence or raise an adapter error; do not fabricate results."""
        ...
