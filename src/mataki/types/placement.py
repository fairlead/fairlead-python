from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations


class AdFormat(StrEnum):
    """Placement ad format."""

    SPONSORED_LISTING = "sponsored_listing"
    NATIVE = "native"


class PlacementAnnotations(Annotations):
    """Placement-specific annotations."""


class Placement(BaseModel):
    """A Mataki placement."""

    id: str
    organization_id: str
    name: str
    slug: str
    ad_format: AdFormat
    max_ads: int = 3
    rules: dict[str, object] = {}
    bidder_config: dict[str, object] = {}
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: PlacementAnnotations = PlacementAnnotations()


__all__ = [
    "AdFormat",
    "Placement",
    "PlacementAnnotations",
]
