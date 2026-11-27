"""Dependency boundary checks for scoped retrieval and error propagation."""

import unittest
from unittest.mock import AsyncMock

from src.main.app.services.rag_service import RagService
from src.main.app.services.rag_service.domain.retrieval_query import RetrievalQuery
from src.main.app.services.rag_service.domain.retrieved_chunk import RetrievedChunk
from src.main.app.services.rag_service.ports.retriever import Retriever
from src.main.app.shared.contracts import RequestContext


class TestRagService(unittest.IsolatedAsyncioTestCase):
    async def test_forwards_the_exact_request_context_to_the_provider(self):
        context = RequestContext("request-1", "principal-1", "tenant-1", "service-1")
        query = RetrievalQuery("router disconnects")
        chunks = (RetrievedChunk("manual-1", "chunk-1", "Approved procedure"),)
        retriever = AsyncMock(spec=Retriever)
        retriever.retrieve.return_value = chunks

        result = await RagService(retriever).retrieve(query=query, context=context)

        self.assertEqual(result, chunks)
        retriever.retrieve.assert_awaited_once_with(query=query, context=context)

    async def test_provider_failures_are_not_disguised_as_empty_results(self):
        context = RequestContext("request-1", "principal-1", "tenant-1", "service-1")
        retriever = AsyncMock(spec=Retriever)
        retriever.retrieve.side_effect = PermissionError("Access denied")

        with self.assertRaises(PermissionError):
            await RagService(retriever).retrieve(
                query=RetrievalQuery("router disconnects"), context=context
            )

    def test_rejects_blank_queries_and_invalid_limits(self):
        for text, limit in ((" ", 5), ("router", 0), ("router", 51), ("router", True)):
            with self.subTest(text=text, limit=limit), self.assertRaises(ValueError):
                RetrievalQuery(text=text, limit=limit)

    def test_rejects_missing_context_identifiers(self):
        with self.assertRaises(ValueError):
            RequestContext("request-1", "principal-1", "tenant-1", " ")
