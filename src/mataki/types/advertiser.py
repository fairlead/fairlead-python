from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations


class AdvertiserStatus(StrEnum):
    """Advertiser status."""

    ACTIVE = "active"
    PAUSED = "paused"


class AdvertiserAnnotations(Annotations):
    """Advertiser-specific annotations."""


class Advertiser(BaseModel):
    """A Mataki advertiser."""

    id: str
    organization_id: str
    name: str
    external_id: str | None = None
    status: AdvertiserStatus = AdvertiserStatus.ACTIVE
    metadata: dict[str, object] = {}
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: AdvertiserAnnotations = AdvertiserAnnotations()


__all__ = [
    "Advertiser",
    "AdvertiserAnnotations",
    "AdvertiserStatus",
]
