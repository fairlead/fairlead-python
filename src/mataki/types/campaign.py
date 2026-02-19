from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations


class CampaignStatus(StrEnum):
    """Campaign status."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class CampaignAnnotations(Annotations):
    """Campaign-specific annotations."""


class Campaign(BaseModel):
    """A Mataki campaign."""

    id: str
    advertiser_id: str
    organization_id: str
    name: str
    status: CampaignStatus = CampaignStatus.DRAFT
    budget_total_cents: int | None = None
    budget_daily_cents: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: CampaignAnnotations = CampaignAnnotations()


__all__ = [
    "Campaign",
    "CampaignAnnotations",
    "CampaignStatus",
]
