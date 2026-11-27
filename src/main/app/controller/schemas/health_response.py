"""HTTP response for process liveness, independent of model readiness."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """A running API process can answer this without configured AI providers."""

    status: Literal["ok"] = "ok"
