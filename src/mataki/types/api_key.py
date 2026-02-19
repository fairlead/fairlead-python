from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from mataki.types.shared import Annotations, Audit


class Role(StrEnum):
    """API key role determining default permissions."""

    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class Environment(StrEnum):
    """API key environment scope."""

    LIVE = "live"
    TEST = "test"


class ApiKeyAnnotations(Annotations):
    """API key-specific annotations."""

    last_used: Audit | None = None


class ApiKey(BaseModel):
    """A Mataki API key."""

    id: str
    organization_id: str
    name: str
    key_prefix: str
    key_suffix: str
    role: Role
    scopes: list[str]
    environment: Environment
    is_active: bool = True
    expires_at: datetime | None = None
    tags: list[str] = []
    labels: dict[str, str] = {}
    annotations: ApiKeyAnnotations = ApiKeyAnnotations()


class CreateApiKeyResponse(BaseModel):
    """Response from creating an API key, including the raw secret shown once."""

    api_key: ApiKey
    raw_key: str


__all__ = [
    "ApiKey",
    "ApiKeyAnnotations",
    "CreateApiKeyResponse",
    "Environment",
    "Role",
]
