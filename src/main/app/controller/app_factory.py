"""Construct the HTTP application without starting a server or model clients."""

from fastapi import FastAPI

from src.main.app.controller.router import router


def create_app() -> FastAPI:
    application = FastAPI(title="AI Service Resolution Platform", version="0.1.0")
    application.include_router(router)
    return application
