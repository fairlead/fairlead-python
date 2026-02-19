from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
import respx

from mataki import AsyncMataki, Mataki

BASE_URL = "https://api.mataki.dev"


@pytest.fixture()
def mock_api() -> Iterator[respx.MockRouter]:
    with respx.mock(base_url=BASE_URL) as mock:
        yield mock


@pytest.fixture()
def client() -> Iterator[Mataki]:
    with Mataki(api_key="mk_test_abc123") as c:
        yield c


@pytest.fixture()
def async_client() -> AsyncMataki:
    return AsyncMataki(api_key="mk_test_abc123")


# --- Response factories ---


def org_json(
    *,
    id: str = "org_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test Org",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "name": name,
        "api_version": None,
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def api_key_json(
    *,
    id: str = "key_7mN3pR9xK2wLvY8cJH4fQ",
    name: str = "Test Key",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "name": name,
        "key_prefix": "mk_test_",
        "key_suffix": "abc1",
        "role": "member",
        "scopes": [],
        "environment": "test",
        "is_active": True,
        "expires_at": None,
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None, "last_used": None},
        **overrides,
    }


def list_response(
    data: list[dict[str, Any]],
    *,
    offset: int = 0,
    limit: int = 25,
    total_results: int | None = None,
) -> dict[str, Any]:
    return {
        "data": data,
        "pagination": {"offset": offset, "limit": limit, "total_results": total_results},
        "meta": {},
    }


def advertiser_json(
    *,
    id: str = "adv_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test Advertiser",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "name": name,
        "external_id": None,
        "status": "active",
        "metadata": {},
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def campaign_json(
    *,
    id: str = "cmp_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test Campaign",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "advertiser_id": "adv_4K7fR9pLm2nQwXvY8cJH3",
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "name": name,
        "status": "draft",
        "budget_total_cents": None,
        "budget_daily_cents": None,
        "start_date": None,
        "end_date": None,
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def line_item_json(
    *,
    id: str = "li_4K7fR9pLm2nQwXvY8cJH3",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "campaign_id": "cmp_4K7fR9pLm2nQwXvY8cJH3",
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "bidder_type": "sponsored_listing",
        "status": "active",
        "bid_strategy": "cpc",
        "bid_amount_cents": 150,
        "targeting": {},
        "priority": 0,
        "delivery_goal": None,
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def ad_json(
    *,
    id: str = "ad_4K7fR9pLm2nQwXvY8cJH3",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "line_item_id": "li_4K7fR9pLm2nQwXvY8cJH3",
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "ad_type": "listing_ref",
        "external_item_id": None,
        "quality_score": "1.00",
        "metadata": {},
        "status": "active",
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def placement_json(
    *,
    id: str = "plc_4K7fR9pLm2nQwXvY8cJH3",
    name: str = "Test Placement",
    **overrides: Any,
) -> dict[str, Any]:
    return {
        "id": id,
        "organization_id": "org_4K7fR9pLm2nQwXvY8cJH3",
        "name": name,
        "slug": "test-placement",
        "ad_format": "sponsored_listing",
        "max_ads": 3,
        "rules": {},
        "bidder_config": {},
        "tags": [],
        "labels": {},
        "annotations": {"created": None, "updated": None},
        **overrides,
    }


def error_response(
    *,
    type: str = "not_found_error",
    message: str = "Not found",
    code: int = 404,
    request_id: str = "req_123",
    details: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "error": {
            "type": type,
            "message": message,
            "code": code,
            "request_id": request_id,
            "details": details,
        }
    }
