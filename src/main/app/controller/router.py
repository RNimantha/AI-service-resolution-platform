"""Central registration for HTTP controllers."""

from fastapi import APIRouter

from src.main.app.controller.health_controller import router as health_router
from src.main.app.controller.rag_controller import router as rag_router

router = APIRouter()
router.include_router(health_router)
router.include_router(rag_router)
