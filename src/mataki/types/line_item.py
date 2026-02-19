from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations


class BidderType(StrEnum):
    """Line item bidder type."""

    SPONSORED_LISTING = "sponsored_listing"


class LineItemStatus(StrEnum):
    """Line item status."""

    ACTIVE = "active"
    PAUSED = "paused"


class LineItemAnnotations(Annotations):
    """Line item-specific annotations."""


class LineItem(BaseModel):
    """A Mataki line item."""

    id: str
    campaign_id: str
    organization_id: str
    bidder_type: BidderType = BidderType.SPONSORED_LISTING
    status: LineItemStatus = LineItemStatus.ACTIVE
    bid_strategy: str
    bid_amount_cents: int
    targeting: dict[str, object] = {}
    priority: int = 0
    delivery_goal: dict[str, object] | None = None
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: LineItemAnnotations = LineItemAnnotations()


__all__ = [
    "BidderType",
    "LineItem",
    "LineItemAnnotations",
    "LineItemStatus",
]
