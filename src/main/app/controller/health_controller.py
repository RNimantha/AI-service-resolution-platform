"""Liveness endpoints; authenticated business routes are future work."""

from fastapi import APIRouter

from src.main.app.controller.schemas.health_response import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    """Report API process liveness without claiming provider readiness."""
    return HealthResponse()
