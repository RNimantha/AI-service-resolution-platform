# Task 1 Text Document Preview

The first RAG component accepts a title and text, creates a validated Document, and returns a preview. This establishes the boundary between HTTP handling and ingestion behavior before adding files, chunks, embeddings, storage, or generation.

Status: Implemented and awaiting your run.

## Learning outcome

You should be able to explain where document validation belongs, why the loader receives plain Python values, how the controller gets its dependency, and why previewing a document does not index it.

## Request flow

```text
POST /rag/documents/preview
→ DocumentPreviewRequest validates HTTP input
→ get_text_document_loader supplies a loader
→ rag_controller calls TextDocumentLoader.load
→ the loader constructs Document
→ Document validates its data and exposes counts and preview
→ the controller maps it to DocumentPreviewResponse
```

Document and TextDocumentLoader are framework-independent. They can be reused by future file ingestion and indexing without calling FastAPI. Request and response schemas describe the HTTP interface; they have a separate responsibility from the document model.

## Files to read in order

| Order | File | Responsibility |
| --- | --- | --- |
| 1 | [document.py](../../src/main/app/services/rag_service/domain/document.py) | Document fields, validation, character count, whitespace word count, preview |
| 2 | [text_document_loader.py](../../src/main/app/services/rag_service/ingestion/text_document_loader.py) | Generate a transient ID and construct a document from submitted text |
| 3 | [RAG public exports](../../src/main/app/services/rag_service/__init__.py) | Expose components through the public import path |
| 4 | [document_preview_request.py](../../src/main/app/controller/schemas/document_preview_request.py) | Validate the incoming JSON shape |
| 5 | [document_preview_response.py](../../src/main/app/controller/schemas/document_preview_response.py) | Define the returned JSON shape |
| 6 | [rag_dependencies.py](../../src/main/app/controller/dependencies/rag_dependencies.py) | Supply the stateless loader to FastAPI |
| 7 | [rag_controller.py](../../src/main/app/controller/rag_controller.py) | Call the loader and translate document validation errors to HTTP 422 |
| 8 | [router.py](../../src/main/app/controller/router.py) | Register the RAG controller |

Each class has its own file. Functions and router modules do not need a class.

## Run the application

Open a terminal at the project root:

```sh
cd /Users/nimantha/Nimantha-PP/ai-service-resolution-platform
make setup
make run
```

The API listens on 127.0.0.1:8000 by default. Keep that terminal running. Open http://127.0.0.1:8000/docs in a browser to use the interactive API documentation, or submit the request from a second terminal.

## Submit a document

```sh
curl -sS -X POST http://127.0.0.1:8000/rag/documents/preview \
  -H 'Content-Type: application/json' \
  -d '{"title":"Router troubleshooting","content":"Restart the router. Wait 30 seconds."}'
```

Expected shape:

```json
{
  "document_id": "a-generated-UUID",
  "title": "Router troubleshooting",
  "source": "inline",
  "character_count": 36,
  "word_count": 6,
  "preview": "Restart the router. Wait 30 seconds."
}
```

The UUID changes on each request. It identifies this transient preview; there is no saved document to fetch later. Content stays in memory for request processing and is not written to a document store by this component.

## Try these experiments

| Experiment | Expected behavior | Concept |
| --- | --- | --- |
| Add spaces around the title | Leading and trailing title spaces are removed | Loader preparation |
| Add line breaks or Sinhala/Tamil text to content | Original content and line breaks are preserved | Source fidelity |
| Submit more than 200 content characters | Counts cover all content; preview contains the first 200 characters | Preview versus source |
| Submit spaces only as content | HTTP 422 with a validation error | Semantic validation |
| Add a file_path or another unknown JSON field | HTTP 422 | Explicit input contract |
| Submit over 100000 content characters | HTTP 422 | Document field limit |
| Submit the same document twice | Different preview IDs | Transient identity versus persistence |

Titles are limited to 200 characters. Content is limited to 100000 characters. These are field limits after JSON parsing; transport-level body limits are a later task. Character counts use Python string length. Word counts use whitespace separation, not a model tokenizer or language-specific segmentation.

## Verify directly without HTTP

The same loader can be imported from your Python environment:

```python
from src.main.app.services.rag_service import TextDocumentLoader

loader = TextDocumentLoader()
document = loader.load(title="Router manual", content="Check the power light.")

print(document.title)
print(document.character_count)
print(document.preview)
```

This is reusable component code. The application execution entry point remains src/main/app/main.py.

## Run checks

```sh
make check
```

Focused loader checks:

```sh
uv run --locked python -m unittest \
  tests.unit.services.rag_service.test_text_document_loader -v
```

Focused HTTP checks:

```sh
uv run --locked python -m unittest \
  tests.integration.services.rag_service.test_document_preview -v
```

Tests cover Unicode and layout preservation, preview boundaries, blank input, character limits, transient identities, unexpected fields, and HTTP validation.

## Checkpoint before Task 2

Run a successful preview and one invalid request. Read Document and TextDocumentLoader, then follow the controller mapping. Confirm you can explain the difference between previewing, chunking, embedding, and indexing.

Share your result or questions before requesting Task 2, which adds a bounded UTF-8 .txt upload. Task 2 has not been implemented.

## Framework references

- [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/) explains the Pydantic request boundary.
- [FastAPI errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) explains HTTPException in controllers.
- [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/) describes field constraints.
