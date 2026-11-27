# case_service

Canonical case state, conversations, actions, outcomes, and audit records.

Public import: `src.main.app.services.case_service`. Dependencies are managed by the root pyproject.toml.

## Components

| Folder | Responsibility |
| --- | --- |
| `application/` | Case use cases |
| `domain/` | Case domain models |
| `repositories/` | Case persistence |
| `ports/` | Repository and event interfaces |

## Development

Run `make setup` at the project root to install the application, then `make check`.
Add dependencies to the root pyproject.toml and update uv.lock after changes.
Use one class per Python file and keep every Python file below 750 lines.
Import this service's own modules explicitly. For local composition, import another service through its public package interface and declare the dependency. Use typed transport clients when services run independently. Do not import another service's internal modules.

Business components remain a scaffold. All FastAPI routes, schemas, dependencies, middleware, and app construction belong in src/main/app/controller.
