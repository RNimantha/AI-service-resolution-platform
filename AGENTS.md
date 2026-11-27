# Project engineering rules

## Git workflow

- Create and use a separate `feature/<descriptive-name>` branch for each new piece of work.
- Commit and push all relevant project changes on the feature branch. Keep credentials, local data, and generated artifacts excluded.
- Do not commit or push directly to `main` unless the user explicitly requests it.
- Before pushing, run `git fetch --prune origin` and rebase the feature branch onto `origin/main` to keep history linear. Incorporate any remote feature-branch commits before rebasing; do not discard collaborators' work.
- Use a normal push when it is a fast-forward. After rebasing previously pushed feature commits, use `git push --force-with-lease` with an explicit expected remote commit; if the lease fails, inspect and reconcile the remote changes before retrying.
- Never use plain `--force` or rewrite `main` history. Keep commits focused and run the required checks before pushing.

## Python files

- Define at most one class in each Python file, including nested classes, protocols, dataclasses, enums, and exceptions.
- Keep every Python file below 750 physical lines, including comments and blank lines. The maximum is 749.
- Use snake_case filenames and focused modules. Functions and initializers may have zero classes.
- Use explicit imports. Do not use wildcard imports, dynamic loading to evade boundaries, or sys.path modifications.
- Export public service interfaces explicitly from their package initializers.

## Application structure

- src/main/app/main.py is the sole application execution entry point. Run it with python -m src.main.app.main.
- Main composes the HTTP app and starts Uvicorn only inside the __name__ guard. Importing it may construct an ASGI app but must not start a server, contact providers, or load models.
- All FastAPI and Starlette code belongs in src/main/app/controller, including routers, schemas, dependencies, middleware, exception handlers, and the app factory.
- All RAG components belong in src/main/app/services/rag_service, including document ingestion, chunking, embeddings, retrieval, reranking, generation, storage, and RAG prompts.
- Other business services live in src/main/app/services. They must not depend on controllers or HTTP framework classes.
- Use public service imports such as from src.main.app.services.rag_service import RagService. A service must not import another service's internal modules.
- Framework-independent shared contracts live in src/main/app/shared/contracts and must not import services or controllers.
- Composition belongs in src/main/app/core. Inject providers explicitly; do not hard-code credentials or initialize clients on import.
- The root pyproject.toml and uv.lock manage the single application and its dependencies.
- Development tools such as scripts/check_structure.py may retain their own CLI guards.
- Do not create placeholder implementations that claim to authenticate, retrieve production data, book appointments, or run models.

## Verification

- Run make check after code or dependency changes and make structure after structural changes.
- Add focused behavioral tests for meaningful changes and regressions.
- Keep tests under tests, preserving service ownership through subfolders.
- Update docs/08-project-structure.md when ownership or imports change.
- Keep production data, credentials, recordings, and model weights outside source control.

## RAG learning checkpoints

- Follow docs/09-rag-microtasks.md one task at a time.
- The user runs and understands each task before requesting the next. Do not implement later tasks automatically.
- Each task needs a small runnable example, explanation, expected result, and appropriate developer verification.
- Keep developer verification separate from user validation. A passing test suite does not mean the user has run or understood a task.
