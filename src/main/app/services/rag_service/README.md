# rag_service

All retrieval-augmented generation components, including document ingestion and RAG prompts.

Public import: `src.main.app.services.rag_service`. Dependencies are managed by the root pyproject.toml.

## Components

| Folder | Responsibility |
| --- | --- |
| `application/` | RAG orchestration |
| `domain/` | RAG domain models |
| `ports/` | Provider and repository interfaces |
| `ingestion/` | Document parsing, OCR, and metadata extraction |
| `chunking/` | Document segmentation |
| `embeddings/` | Embedding adapters |
| `retrieval/` | Keyword and vector retrievers |
| `reranking/` | Ranking and fusion |
| `generation/` | Grounded answer generation |
| `storage/` | Document, chunk, and vector persistence |
| `clients/` | External provider clients |

## Development

Run `make setup` at the project root to install the application, then `make check`.
Add dependencies to the root pyproject.toml and update uv.lock after changes.
Use one class per Python file and keep every Python file below 750 lines.
Import this service's own modules explicitly. For local composition, import another service through its public package interface and declare the dependency. Use typed transport clients when services run independently. Do not import another service's internal modules.

Task 1 implements the framework-independent Document and TextDocumentLoader. Other RAG components remain later work. All FastAPI routes, schemas, dependencies, middleware, and app construction belong in src/main/app/controller.

## Guided implementation

Follow [the micro task plan](../../../../../docs/09-rag-microtasks.md). Begin with [Task 1 text document preview](../../../../../docs/rag/task-01-text-document-preview.md), run it, and discuss questions before requesting Task 2.

Public components for Task 1:

```python
from src.main.app.services.rag_service import Document, TextDocumentLoader
```
