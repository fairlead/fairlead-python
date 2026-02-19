from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations


class AdType(StrEnum):
    """Ad format type."""

    LISTING_REF = "listing_ref"
    NATIVE = "native"
    DISPLAY = "display"


class AdStatus(StrEnum):
    """Ad status."""

    ACTIVE = "active"
    PAUSED = "paused"


class AdAnnotations(Annotations):
    """Ad-specific annotations."""


class Ad(BaseModel):
    """A Mataki ad."""

    id: str
    line_item_id: str
    organization_id: str
    ad_type: AdType
    external_item_id: str | None = None
    quality_score: float | str = "1.00"
    metadata: dict[str, object] = {}
    status: AdStatus = AdStatus.ACTIVE
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: AdAnnotations = AdAnnotations()


__all__ = [
    "Ad",
    "AdAnnotations",
    "AdStatus",
    "AdType",
]
