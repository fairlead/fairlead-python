from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.ad import Ad, AdStatus, AdType

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class AdsResource:
    """Synchronous ads API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[Ad]:
        """List ads with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``line_item_id = li_...``).
            sort: Sort clause (e.g. ``ad_type:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of ads. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/ads", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/ads",
            params=params,
            model=Ad,
        )

    def get(self, entity_id: str) -> Ad:
        """Get an ad by ID.

        Args:
            entity_id: Ad ID (e.g. ``ad_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/ads/{entity_id}")
        return Ad.model_validate(response.json())

    def create(
        self,
        *,
        line_item_id: str,
        ad_type: AdType | str,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Create a new ad.

        Args:
            line_item_id: Parent line item ID.
            ad_type: Ad format type (listing_ref, native, display).
            external_item_id: External item reference, or None.
            quality_score: Quality score (default "1.00").
            metadata: Arbitrary key-value metadata.
            status: Ad status (active, paused). Defaults to active.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", f"/line-items/{line_item_id}/ads", json=body)
        return Ad.model_validate(response.json())

    def update(
        self,
        entity_id: str,
        *,
        ad_type: AdType | str | None = None,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Update an ad. Only provided fields are changed.

        Args:
            entity_id: Ad ID.
            ad_type: New ad type, or None to leave unchanged.
            external_item_id: New external item ID, or None to leave unchanged.
            quality_score: New quality score, or None to leave unchanged.
            metadata: New metadata, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("PATCH", f"/ads/{entity_id}", json=body)
        return Ad.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete an ad.

        Args:
            entity_id: Ad ID.
        """
        self._client._request("DELETE", f"/ads/{entity_id}")


class AsyncAdsResource:
    """Asynchronous ads API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[Ad]:
        """List ads with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``line_item_id = li_...``).
            sort: Sort clause (e.g. ``ad_type:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of ads. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/ads", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/ads",
            params=params,
            model=Ad,
        )

    async def get(self, entity_id: str) -> Ad:
        """Get an ad by ID.

        Args:
            entity_id: Ad ID (e.g. ``ad_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/ads/{entity_id}")
        return Ad.model_validate(response.json())

    async def create(
        self,
        *,
        line_item_id: str,
        ad_type: AdType | str,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Create a new ad.

        Args:
            line_item_id: Parent line item ID.
            ad_type: Ad format type (listing_ref, native, display).
            external_item_id: External item reference, or None.
            quality_score: Quality score (default "1.00").
            metadata: Arbitrary key-value metadata.
            status: Ad status (active, paused). Defaults to active.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", f"/line-items/{line_item_id}/ads", json=body)
        return Ad.model_validate(response.json())

    async def update(
        self,
        entity_id: str,
        *,
        ad_type: AdType | str | None = None,
        external_item_id: str | None = None,
        quality_score: float | str | None = None,
        metadata: Dict[str, object] | None = None,
        status: AdStatus | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Ad:
        """Update an ad. Only provided fields are changed.

        Args:
            entity_id: Ad ID.
            ad_type: New ad type, or None to leave unchanged.
            external_item_id: New external item ID, or None to leave unchanged.
            quality_score: New quality score, or None to leave unchanged.
            metadata: New metadata, or None to leave unchanged.
            status: New status, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(
            ad_type=ad_type,
            external_item_id=external_item_id,
            quality_score=quality_score,
            metadata=metadata,
            status=status,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("PATCH", f"/ads/{entity_id}", json=body)
        return Ad.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete an ad.

        Args:
            entity_id: Ad ID.
        """
        await self._client._request("DELETE", f"/ads/{entity_id}")


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
    ad_type: AdType | str,
    external_item_id: str | None,
    quality_score: float | str | None,
    metadata: dict[str, object] | None,
    status: AdStatus | str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "ad_type": str(ad_type),
    }
    if external_item_id is not None:
        body["external_item_id"] = external_item_id
    if quality_score is not None:
        body["quality_score"] = quality_score
    if metadata is not None:
        body["metadata"] = metadata
    if status is not None:
        body["status"] = str(status)
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _update_body(
    *,
    ad_type: AdType | str | None,
    external_item_id: str | None,
    quality_score: float | str | None,
    metadata: dict[str, object] | None,
    status: AdStatus | str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if ad_type is not None:
        body["ad_type"] = str(ad_type)
    if external_item_id is not None:
        body["external_item_id"] = external_item_id
    if quality_score is not None:
        body["quality_score"] = quality_score
    if metadata is not None:
        body["metadata"] = metadata
    if status is not None:
        body["status"] = str(status)
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
