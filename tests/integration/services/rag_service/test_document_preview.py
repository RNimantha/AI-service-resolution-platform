"""HTTP contract checks for inline document validation and preview."""

import unittest

import httpx

from src.main.app.controller.app_factory import create_app
from src.main.app.services.rag_service import MAX_DOCUMENT_CHARACTERS


class TestDocumentPreview(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=create_app()), base_url="http://test"
        )

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_returns_the_document_summary(self):
        content = "Restart the router. Wait 30 seconds."
        response = await self.client.post(
            "/rag/documents/preview", json={"title": "Router troubleshooting", "content": content}
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["title"], "Router troubleshooting")
        self.assertEqual(result["source"], "inline")
        self.assertEqual(result["character_count"], len(content))
        self.assertEqual(result["word_count"], 6)
        self.assertEqual(result["preview"], content)
        self.assertIn("document_id", result)

    async def test_blank_input_returns_a_validation_error(self):
        for payload in (
            {"title": " ", "content": "Text"},
            {"title": "Manual", "content": "\n\t"},
        ):
            with self.subTest(payload=payload):
                response = await self.client.post("/rag/documents/preview", json=payload)
                self.assertEqual(response.status_code, 422)

    async def test_oversized_and_unexpected_input_is_rejected(self):
        for payload in (
            {"title": "Manual", "content": "a" * (MAX_DOCUMENT_CHARACTERS + 1)},
            {"title": "Manual", "content": "Text", "file_path": "/not-an-accepted-input"},
            {"title": "Manual", "content": 123},
        ):
            with self.subTest(keys=list(payload)):
                response = await self.client.post("/rag/documents/preview", json=payload)
                self.assertEqual(response.status_code, 422)
