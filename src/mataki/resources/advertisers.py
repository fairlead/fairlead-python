from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.advertiser import Advertiser, AdvertiserStatus

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class AdvertisersResource:
    """Synchronous advertisers API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[Advertiser]:
        """List advertisers with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``name ~* %acme%``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of advertisers. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/advertisers", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/advertisers",
            params=params,
            model=Advertiser,
        )

    def get(self, entity_id: str) -> Advertiser:
        """Get an advertiser by ID.

        Args:
            entity_id: Advertiser ID (e.g. ``adv_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/advertisers/{entity_id}")
        return Advertiser.model_validate(response.json())

    def create(
        self,
        *,
        name: str,
        external_id: str | None = None,
        status: AdvertiserStatus | str | None = None,
        metadata: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Advertiser:
        """Create a new advertiser.

        Args:
            name: Display name (1-255 characters).
            external_id: External identifier for cross-system linking.
            status: Advertiser status (active, paused). Defaults to active.
            metadata: Arbitrary key-value metadata.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            external_id=external_id,
            status=status,
            metadata=metadata,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", "/advertisers", json=body)
        return Advertiser.model_validate(response.json())

    def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        external_id: str | None = None,
        status: AdvertiserStatus | str | None = None,
        metadata: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Advertiser:
        """Update an advertiser. Only provided fields are changed.

        Args:
            entity_id: Advertiser ID.
            name: New display name, or None to leave unchanged.
            external_id: New external ID, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            metadata: New metadata, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            external_id=external_id,
            status=status,
            metadata=metadata,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("PATCH", f"/advertisers/{entity_id}", json=body)
        return Advertiser.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete an advertiser.

        Args:
            entity_id: Advertiser ID.
        """
        self._client._request("DELETE", f"/advertisers/{entity_id}")


class AsyncAdvertisersResource:
    """Asynchronous advertisers API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[Advertiser]:
        """List advertisers with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``name ~* %acme%``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of advertisers. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/advertisers", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/advertisers",
            params=params,
            model=Advertiser,
        )

    async def get(self, entity_id: str) -> Advertiser:
        """Get an advertiser by ID.

        Args:
            entity_id: Advertiser ID (e.g. ``adv_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/advertisers/{entity_id}")
        return Advertiser.model_validate(response.json())

    async def create(
        self,
        *,
        name: str,
        external_id: str | None = None,
        status: AdvertiserStatus | str | None = None,
        metadata: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Advertiser:
        """Create a new advertiser.

        Args:
            name: Display name (1-255 characters).
            external_id: External identifier for cross-system linking.
            status: Advertiser status (active, paused). Defaults to active.
            metadata: Arbitrary key-value metadata.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            external_id=external_id,
            status=status,
            metadata=metadata,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", "/advertisers", json=body)
        return Advertiser.model_validate(response.json())

    async def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        external_id: str | None = None,
        status: AdvertiserStatus | str | None = None,
        metadata: Dict[str, object] | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Advertiser:
        """Update an advertiser. Only provided fields are changed.

        Args:
            entity_id: Advertiser ID.
            name: New display name, or None to leave unchanged.
            external_id: New external ID, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            metadata: New metadata, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            name=name,
            external_id=external_id,
            status=status,
            metadata=metadata,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("PATCH", f"/advertisers/{entity_id}", json=body)
        return Advertiser.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete an advertiser.

        Args:
            entity_id: Advertiser ID.
        """
        await self._client._request("DELETE", f"/advertisers/{entity_id}")


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
    external_id: str | None,
    status: AdvertiserStatus | str | None,
    metadata: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name}
    if external_id is not None:
        body["external_id"] = external_id
    if status is not None:
        body["status"] = str(status)
    if metadata is not None:
        body["metadata"] = metadata
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _update_body(
    *,
    name: str | None,
    external_id: str | None,
    status: AdvertiserStatus | str | None,
    metadata: dict[str, object] | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if external_id is not None:
        body["external_id"] = external_id
    if status is not None:
        body["status"] = str(status)
    if metadata is not None:
        body["metadata"] = metadata
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
