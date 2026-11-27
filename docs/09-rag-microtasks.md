# RAG Implementation Micro Tasks

Build and understand one observable behavior at a time. After each task, run its example, inspect the output, read the changed code, and discuss any questions before starting the next task.

Task 1 is implemented and awaiting your run. All subsequent tasks are pending. Automated checks establish developer verification; they do not replace your learning checkpoint.

## Boundaries

- RAG models, loaders, splitting, embeddings, indexing, retrieval, ranking, generation, and RAG prompts belong under src/main/app/services/rag_service.
- FastAPI controllers, HTTP schemas, and dependency providers belong under src/main/app/controller.
- The application starts through src/main/app/main.py.
- Each Python file defines at most one class and contains fewer than 750 physical lines.
- Tests live under tests and preserve RAG ownership through service subfolders.
- Production credentials, customer data, recordings, and model weights remain outside source control.

## Task sequence

| Task | Small deliverable | What you will run or inspect | Status |
| --- | --- | --- | --- |
| 01 Text document preview | Document model, inline loader, preview endpoint | Submit text and inspect metadata and preview | Implemented, awaiting your run |
| 02 Text file upload | Bounded UTF-8 .txt upload using the document model | Upload a small file and compare its content | Pending |
| 03 Text normalization | Explicit cleanup with original text preserved | Compare original and normalized line breaks and spacing | Pending |
| 04 Chunk model | Chunk identity, document reference, and source offsets | Inspect a chunk and locate it in the source | Pending |
| 05 Basic text splitter | Deterministic character splitting with overlap | Run a small document through different chunk sizes | Pending |
| 06 Chunk preview endpoint | Expose real splitter output through a controller | Inspect chunk boundaries and overlapping text | Pending |
| 07 Embedding interface | Typed provider contract with model and dimension metadata | Understand the contract and run adapter boundary tests | Pending |
| 08 Real embedding adapter | One actual embedding model chosen for the corpus | Embed two passages and compare their real vectors | Pending |
| 09 Database foundation | Local PostgreSQL connection and first migration | Start the database and apply the schema | Pending |
| 10 Vector storage | pgvector document and chunk persistence | Store and read a versioned vector record | Pending |
| 11 Document indexing | Load, normalize, split, embed, and persist with duplicate protection | Index the same document twice and inspect stable records | Pending |
| 12 Access scope | Enforce verified scope and document permissions before stored retrieval | Confirm permitted records are visible and other scopes are excluded | Pending |
| 13 Vector retrieval | Embed a query and return ranked, permitted evidence | Search indexed manuals without an LLM | Pending |
| 14 Retrieval endpoint | Thin HTTP adapter to the real retrieval component | Submit a query and inspect passage IDs and scores | Pending |
| 15 Hybrid search | Keyword search combined with vector retrieval | Compare exact equipment-code and semantic queries | Pending |
| 16 Reranking | One evaluated reranker over retrieved candidates | Compare candidate order before and after reranking | Pending |
| 17 Generation interface | Explicit answer-generation input and output contracts | Inspect evidence, generation options, and error handling | Pending |
| 18 Real generation adapter | One actual model provider with bounded calls | Run an isolated grounded generation example | Pending |
| 19 Grounded answer assembly | RAG prompt and citation mapping using retrieved evidence | Inspect the context sent to the model and returned citations | Pending |
| 20 Answer endpoint | Connect query, retrieval, and generation through a controller | Ask a supported question and inspect the answer and sources | Pending |
| 21 Insufficient evidence | Explicit abstention and citation validation | Ask unsupported and conflicting-evidence questions | Pending |
| 22 Document lifecycle | Replace, delete, revoke, and reindex a document safely | Confirm obsolete evidence disappears from retrieval | Pending |
| 23 Retrieval evaluation | Reviewed queries and recall/ranking measurements | Compare retrieval variants on the same dataset | Pending |
| 24 Answer evaluation | Reviewed grounding and citation checks | Measure supported and unsupported question behavior | Pending |
| 25 Runtime observability | Trace IDs, timing, usage, and redacted failures | Follow one request through its recorded stages | Pending |
| 26 Resource limits | Timeouts, cancellation, upload/body limits, and rate controls | Exercise one controlled failure at a time | Pending |
| 27 Production qualification | Deployment configuration, load checks, and recovery evidence | Run a controlled pilot against agreed gates | Pending |

This sequence establishes a text-first RAG pipeline. Add PDF parsing, OCR, section-aware or tokenizer-aware chunking, and further providers as separate tasks after the baseline is measurable. The initial character splitter is a transparent baseline to evaluate, not an assumed optimal production strategy.

## Working agreement

1. Implement the current task and its necessary verification only.
2. Save an explanation, run command, expected output, and small experiment for that task.
3. Run developer checks and report their result.
4. You run the task and review how it works.
5. Resolve questions before you explicitly request the next task.

Do not mark a task as understood or user-validated merely because automated tests pass. Do not begin later tasks automatically.

## Current task

Start with [Task 1 text document preview](rag/task-01-text-document-preview.md). It needs no model key or database. The endpoint processes only the text supplied in that request and does not read stored account or customer records.
