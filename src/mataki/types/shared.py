from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Audit(BaseModel):
    """Tracks who performed an action and when."""

    at: datetime
    by: str


class Annotations(BaseModel):
    """System-managed metadata attached to every entity."""

    model_config = ConfigDict(extra="allow")

    created: Audit | None = None
    updated: Audit | None = None


class OffsetPaginationMeta(BaseModel):
    """Pagination metadata returned with list responses."""

    offset: int
    limit: int
    total_results: int | None = None


__all__ = [
    "Annotations",
    "Audit",
    "OffsetPaginationMeta",
]
