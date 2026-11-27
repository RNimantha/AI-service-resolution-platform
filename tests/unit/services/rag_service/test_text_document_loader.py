"""Behavior checks for text preservation, validation, and preview boundaries."""

import unittest
from uuid import UUID

from src.main.app.services.rag_service import (
    MAX_DOCUMENT_CHARACTERS,
    MAX_DOCUMENT_TITLE_CHARACTERS,
    TextDocumentLoader,
)


class TestTextDocumentLoader(unittest.TestCase):
    def setUp(self):
        self.loader = TextDocumentLoader()

    def test_preserves_multilingual_text_and_layout(self):
        content = "  Router instructions\r\nසිංහල\nதமிழ்\n"
        document = self.loader.load(title="  Router manual  ", content=content)

        self.assertEqual(document.title, "Router manual")
        self.assertEqual(document.content, content)
        self.assertEqual(document.source, "inline")
        self.assertEqual(document.character_count, len(content))
        self.assertEqual(document.word_count, 4)
        self.assertEqual(UUID(document.document_id).version, 4)

    def test_preview_stops_at_200_characters_without_truncating_the_document(self):
        content = "a" * 250
        document = self.loader.load(title="Manual", content=content)

        self.assertEqual(len(document.preview), 200)
        self.assertEqual(document.content, content)
        self.assertEqual(document.character_count, 250)

    def test_rejects_blank_or_non_text_input(self):
        for title, content in ((" ", "Text"), ("Manual", "\n\t"), (None, "Text"), ("Manual", 1)):
            with self.subTest(title=title, content=content), self.assertRaises(ValueError):
                self.loader.load(title=title, content=content)

    def test_accepts_limits_and_rejects_input_over_limits(self):
        document = self.loader.load(
            title="a" * MAX_DOCUMENT_TITLE_CHARACTERS,
            content="a" * MAX_DOCUMENT_CHARACTERS,
        )
        self.assertEqual(document.character_count, MAX_DOCUMENT_CHARACTERS)
        for title, content in (
            ("a" * (MAX_DOCUMENT_TITLE_CHARACTERS + 1), "Text"),
            ("Manual", "a" * (MAX_DOCUMENT_CHARACTERS + 1)),
        ):
            with self.subTest(title_length=len(title)), self.assertRaises(ValueError):
                self.loader.load(title=title, content=content)

    def test_each_preview_has_a_transient_identity(self):
        first = self.loader.load(title="Manual", content="Same source text")
        second = self.loader.load(title="Manual", content="Same source text")
        self.assertNotEqual(first.document_id, second.document_id)
