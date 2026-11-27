"""Validated input for a bounded retrieval request."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalQuery:
    """A query and a result limit; permissions come from RequestContext."""

    text: str
    limit: int = 5

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text must be a non-empty string")
        if type(self.limit) is not int or not 1 <= self.limit <= 50:
            raise ValueError("limit must be an integer between 1 and 50")
