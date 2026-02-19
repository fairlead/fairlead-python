from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.placement import AdFormat, Placement

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class PlacementsResource:
    """Synchronous placements API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[Placement]:
        """List placements with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``ad_format = native``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of placements. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/placements", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/placements",
            params=params,
            model=Placement,
        )

    def get(self, entity_id: str) -> Placement:
        """Get a placement by ID.

        Args:
            entity_id: Placement ID (e.g. ``plc_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/placements/{entity_id}")
        return Placement.model_validate(response.json())

    def create(
        self,
        *,
        name: str,
        slug: str,
        ad_format: AdFormat | str,
        max_ads: int | None = None,
        rules: Dict[str, object] | None = None,
        bidder_config: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Placement:
        """Create a new placement.

        Args:
            name: Display name (1-255 characters).
            slug: URL-safe slug identifier.
            ad_format: Ad format (sponsored_listing, native).
            max_ads: Maximum number of ads to serve (default 3).
            rules: Placement rules configuration.
            bidder_config: Bidder configuration overrides.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            slug=slug,
            ad_format=ad_format,
            max_ads=max_ads,
            rules=rules,
            bidder_config=bidder_config,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", "/placements", json=body)
        return Placement.model_validate(response.json())

    def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        slug: str | None = None,
        ad_format: AdFormat | str | None = None,
        max_ads: int | None = None,
        rules: Dict[str, object] | None = None,
        bidder_config: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Placement:
        """Update a placement. Only provided fields are changed.

        Args:
            entity_id: Placement ID.
            name: New display name, or None to leave unchanged.
            slug: New slug, or None to leave unchanged.
            ad_format: New ad format, or None to leave unchanged.
            max_ads: New max ads, or None to leave unchanged.
            rules: New rules, or None to leave unchanged.
            bidder_config: New bidder config, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            slug=slug,
            ad_format=ad_format,
            max_ads=max_ads,
            rules=rules,
            bidder_config=bidder_config,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("PATCH", f"/placements/{entity_id}", json=body)
        return Placement.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete a placement.

        Args:
            entity_id: Placement ID.
        """
        self._client._request("DELETE", f"/placements/{entity_id}")


class AsyncPlacementsResource:
    """Asynchronous placements API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[Placement]:
        """List placements with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``ad_format = native``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of placements. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/placements", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/placements",
            params=params,
            model=Placement,
        )

    async def get(self, entity_id: str) -> Placement:
        """Get a placement by ID.

        Args:
            entity_id: Placement ID (e.g. ``plc_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/placements/{entity_id}")
        return Placement.model_validate(response.json())

    async def create(
        self,
        *,
        name: str,
        slug: str,
        ad_format: AdFormat | str,
        max_ads: int | None = None,
        rules: Dict[str, object] | None = None,
        bidder_config: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Placement:
        """Create a new placement.

        Args:
            name: Display name (1-255 characters).
            slug: URL-safe slug identifier.
            ad_format: Ad format (sponsored_listing, native).
            max_ads: Maximum number of ads to serve (default 3).
            rules: Placement rules configuration.
            bidder_config: Bidder configuration overrides.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            slug=slug,
            ad_format=ad_format,
            max_ads=max_ads,
            rules=rules,
            bidder_config=bidder_config,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", "/placements", json=body)
        return Placement.model_validate(response.json())

    async def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        slug: str | None = None,
        ad_format: AdFormat | str | None = None,
        max_ads: int | None = None,
        rules: Dict[str, object] | None = None,
        bidder_config: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Placement:
        """Update a placement. Only provided fields are changed.

        Args:
            entity_id: Placement ID.
            name: New display name, or None to leave unchanged.
            slug: New slug, or None to leave unchanged.
            ad_format: New ad format, or None to leave unchanged.
            max_ads: New max ads, or None to leave unchanged.
            rules: New rules, or None to leave unchanged.
            bidder_config: New bidder config, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            slug=slug,
            ad_format=ad_format,
            max_ads=max_ads,
            rules=rules,
            bidder_config=bidder_config,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("PATCH", f"/placements/{entity_id}", json=body)
        return Placement.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete a placement.

        Args:
            entity_id: Placement ID.
        """
        await self._client._request("DELETE", f"/placements/{entity_id}")


# --- Private helpers ---


def _list_params(
    *,
    query: str | None,
    sort: str | None,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {"offset": offset, "limit": limit}
    if query is not None:
        params["query"] = query
    if sort is not None:
        params["sort"] = sort
    return params


def _create_body(
    *,
    name: str,
    slug: str,
    ad_format: AdFormat | str,
    max_ads: int | None,
    rules: dict[str, object] | None,
    bidder_config: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "name": name,
        "slug": slug,
        "ad_format": str(ad_format),
    }
    if max_ads is not None:
        body["max_ads"] = max_ads
    if rules is not None:
        body["rules"] = rules
    if bidder_config is not None:
        body["bidder_config"] = bidder_config
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _update_body(
    *,
    name: str | None,
    slug: str | None,
    ad_format: AdFormat | str | None,
    max_ads: int | None,
    rules: dict[str, object] | None,
    bidder_config: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if slug is not None:
        body["slug"] = slug
    if ad_format is not None:
        body["ad_format"] = str(ad_format)
    if max_ads is not None:
        body["max_ads"] = max_ads
    if rules is not None:
        body["rules"] = rules
    if bidder_config is not None:
        body["bidder_config"] = bidder_config
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
