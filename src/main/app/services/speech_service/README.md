# speech_service

Streaming speech, audio sessions, interruptions, and telephone integration.

Public import: `src.main.app.services.speech_service`. Dependencies are managed by the root pyproject.toml.

## Components

| Folder | Responsibility |
| --- | --- |
| `stt/` | Speech recognition adapters |
| `tts/` | Speech synthesis adapters |
| `audio/` | Buffering, codecs, and turn detection |
| `telephony/` | Carrier and contact-center adapters |
| `ports/` | Speech provider interfaces |
| `clients/` | Conversation API clients |

## Development

Run `make setup` at the project root to install the application, then `make check`.
Add dependencies to the root pyproject.toml and update uv.lock after changes.
Use one class per Python file and keep every Python file below 750 lines.
Import this service's own modules explicitly. For local composition, import another service through its public package interface and declare the dependency. Use typed transport clients when services run independently. Do not import another service's internal modules.

Business components remain a scaffold. All FastAPI routes, schemas, dependencies, middleware, and app construction belong in src/main/app/controller.
