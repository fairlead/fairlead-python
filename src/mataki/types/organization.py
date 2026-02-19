from __future__ import annotations

from pydantic import BaseModel

from mataki.types.shared import Annotations


class OrganizationAnnotations(Annotations):
    """Organization-specific annotations."""


class Organization(BaseModel):
    """A Mataki organization."""

    id: str
    name: str
    api_version: str | None = None
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: OrganizationAnnotations = OrganizationAnnotations()


__all__ = [
    "Organization",
    "OrganizationAnnotations",
]
