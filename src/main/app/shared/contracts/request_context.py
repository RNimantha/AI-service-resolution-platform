"""Identifiers supplied by trusted authentication and service-scope middleware."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestContext:
    """Carries verified scope; construction alone does not grant authority."""

    correlation_id: str
    principal_id: str
    tenant_id: str
    service_id: str

    def __post_init__(self) -> None:
        for name in ("correlation_id", "principal_id", "tenant_id", "service_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
