"""Application entry point: python -m src.main.app.main."""

import argparse

import uvicorn

from src.main.app.controller.app_factory import create_app

app = create_app()


def main() -> None:
    """Start the HTTP server; importing the module only exposes the ASGI app."""
    parser = argparse.ArgumentParser(description="Run the AI Service Resolution API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    arguments = parser.parse_args()
    uvicorn.run(app, host=arguments.host, port=arguments.port)


if __name__ == "__main__":
    main()
