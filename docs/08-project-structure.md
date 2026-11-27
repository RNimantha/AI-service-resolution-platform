# Application Structure and Import Rules

The application uses the explicit Python namespace src.main.app. Business services live in services, HTTP concerns live in controller, and main.py composes and starts the application. The root project owns dependencies and the lockfile.

## Project layout

```text
ai-service-resolution-platform/
├── pyproject.toml
├── uv.lock
├── Makefile
├── AGENTS.md
├── src/
│   ├── __init__.py
│   └── main/
│       ├── __init__.py
│       └── app/
│           ├── __init__.py
│           ├── main.py
│           ├── controller/
│           │   ├── app_factory.py
│           │   ├── router.py
│           │   ├── health_controller.py
│           │   ├── rag_controller.py
│           │   ├── schemas/
│           │   ├── dependencies/
│           │   └── middleware/
│           ├── core/
│           │   └── composition.py
│           ├── shared/
│           │   └── contracts/
│           │       └── request_context.py
│           └── services/
│               ├── rag_service/
│               ├── agent_service/
│               ├── context_service/
│               ├── tool_service/
│               ├── case_service/
│               ├── workflow_service/
│               ├── speech_service/
│               ├── ml_service/
│               └── topology_service/
├── tests/
│   ├── unit/
│   │   └── services/
│   │       └── rag_service/
│   ├── integration/
│   └── contract/
├── scripts/
├── apps/web/
├── docs/
├── evals/
└── infra/
```

src is deliberately a Python package to support the requested src.main.app imports. The project no longer has separate per-service src folders or per-service dependency manifests. This is one application with modular service ownership.

## Application execution

The only application entry point is [src/main/app/main.py](../src/main/app/main.py):

```python
from src.main.app.controller.app_factory import create_app

app = create_app()

# main() starts Uvicorn with the app.
if __name__ == "__main__":
    main()
```

Run from the project root:

```sh
make setup
make run
```

The equivalent module command supports host and port options:

```sh
uv run --locked python -m src.main.app.main --host 127.0.0.1 --port 8000
```

Use the module command instead of executing the nested main.py by file path. It resolves the requested package namespace correctly. No root main.py remains.

For an ASGI process manager, the application target is src.main.app.main:app. Importing that module constructs the FastAPI app but does not start a server, create external clients, or load models. Development tooling remains separately executable.

## Controller ownership

All FastAPI and Starlette code belongs in src/main/app/controller:

| Component | Responsibility |
| --- | --- |
| app_factory.py | FastAPI construction, router registration, and future lifespan setup |
| router.py | Central router composition |
| health_controller.py | HTTP liveness route |
| schemas | HTTP request and response models, one class per file |
| dependencies | FastAPI dependency providers and authentication integration |
| middleware | HTTP middleware and exception handling |
| Future feature controllers | Thin HTTP adapters calling public service interfaces |

Business services should receive framework-independent data rather than FastAPI Request or HTTPException objects. HTTP errors and transport serialization belong to controllers. This router composition follows [FastAPI's multiple-file application guidance](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

The HTTP application provides GET /health/live, POST /rag/documents/preview for submitted text, and development API documentation at /docs. Liveness reports that the HTTP process responds; it does not claim model, database, or business-service readiness. Stored retrieval, generation, authenticated account access, and production provider adapters remain implementation work.

## Service ownership

| Service | Responsibility |
| --- | --- |
| rag_service | RAG, document ingestion, embeddings, retrieval, reranking, generation, storage, prompts |
| agent_service | Diagnostic graphs, bounded loops, and harness controls |
| context_service | Context assembly, memory, summaries, and freshness |
| tool_service | Authorized tools and operational integration adapters |
| case_service | Canonical case state, actions, audit, and outcomes |
| workflow_service | Durable cases, appointments, callbacks, and reconciliation |
| speech_service | STT, TTS, audio processing, and telephony adapters |
| ml_service | Features, training, fault prediction, and inference |
| topology_service | Network inventory and relationship queries |

The earlier empty api_gateway package is replaced by the central controller layer. Service-local api directories have been removed. Topology ingestion remains distinct from RAG document ingestion.

## RAG components

```text
src/main/app/services/rag_service/
├── __init__.py
├── application/rag_service.py
├── domain/
│   ├── retrieval_query.py
│   ├── retrieved_chunk.py
│   └── document.py
├── ports/retriever.py
├── ingestion/text_document_loader.py
├── chunking/
├── embeddings/
├── retrieval/
├── reranking/
├── generation/
├── storage/
├── clients/
└── prompts/
```

The public RAG interface includes RagService, Retriever, RetrievalQuery, RetrievedChunk, Document, and TextDocumentLoader. The guided implementation begins with [text document preview](rag/task-01-text-document-preview.md). They are explicitly exported by the RAG package initializer. A real retrieval provider must enforce access and freshness before returning data.

## Public imports

```python
from src.main.app.services.rag_service import RagService, RetrievalQuery, Retriever
from src.main.app.shared.contracts import RequestContext
```

Import internal modules directly only within their owning service. Cross-service callers use public package exports. Shared contracts must not depend on services or controllers.

The composition function in core receives a provider explicitly:

```python
from src.main.app.services.rag_service import RagService, Retriever


def build_rag_service(retriever: Retriever) -> RagService:
    return RagService(retriever=retriever)
```

Constructing RequestContext validates identifier shape; it does not grant permission or authenticate the caller. Controllers and operational adapters must enforce verified scope as those integrations are implemented.

## Dependencies and checks

Install from the root lockfile using make setup. Add dependencies to the root pyproject.toml and regenerate uv.lock. There are no separate service installations or workspace member manifests.

Run make check for structural checks, Ruff lint/format verification, and all discovered unit and integration tests. CI runs this finite verification command; it does not start the long-running API server.

The AST checker enforces:

- At most one class per Python file, including nested classes, protocols, and dataclasses.
- At most 749 physical lines, including comments and blank lines.
- Explicit imports without wildcards.
- Public cross-service interfaces rather than internal implementation imports.
- No services or controllers imported by shared contracts.
- No controller imports by services.
- FastAPI and Starlette imports confined to controller within the application.
- Valid syntax and the updated package namespace.

Static import checks cover ordinary absolute and relative imports. Review must still reject indirect or dynamic attempts to bypass ownership. Third-party environments, caches, generated builds, and runtime data are excluded.
