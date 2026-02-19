from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.organization import Organization

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class OrganizationsResource:
    """Synchronous organizations API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[Organization]:
        """List organizations with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``name ~* %acme%``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of organizations. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/organizations", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/organizations",
            params=params,
            model=Organization,
        )

    def get(self, entity_id: str) -> Organization:
        """Get an organization by ID.

        Args:
            entity_id: Organization ID (e.g. ``org_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = self._client._request("GET", f"/organizations/{entity_id}")
        return Organization.model_validate(response.json())

    def create(
        self,
        *,
        name: str,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Organization:
        """Create a new organization.

        Args:
            name: Display name (1-255 characters).
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(name=name, tags=tags, labels=labels)
        response = self._client._request("POST", "/organizations", json=body)
        return Organization.model_validate(response.json())

    def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Organization:
        """Update an organization. Only provided fields are changed.

        Args:
            entity_id: Organization ID.
            name: New display name, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(name=name, tags=tags, labels=labels)
        response = self._client._request("PATCH", f"/organizations/{entity_id}", json=body)
        return Organization.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete an organization.

        Args:
            entity_id: Organization ID.
        """
        self._client._request("DELETE", f"/organizations/{entity_id}")


class AsyncOrganizationsResource:
    """Asynchronous organizations API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[Organization]:
        """List organizations with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``name ~* %acme%``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of organizations. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/organizations", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/organizations",
            params=params,
            model=Organization,
        )

    async def get(self, entity_id: str) -> Organization:
        """Get an organization by ID.

        Args:
            entity_id: Organization ID (e.g. ``org_4K7fR9pLm2nQwXvY8cJH3``).
        """
        response = await self._client._request("GET", f"/organizations/{entity_id}")
        return Organization.model_validate(response.json())

    async def create(
        self,
        *,
        name: str,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Organization:
        """Create a new organization.

        Args:
            name: Display name (1-255 characters).
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(name=name, tags=tags, labels=labels)
        response = await self._client._request("POST", "/organizations", json=body)
        return Organization.model_validate(response.json())

    async def update(
        self,
        entity_id: str,
        *,
        name: str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> Organization:
        """Update an organization. Only provided fields are changed.

        Args:
            entity_id: Organization ID.
            name: New display name, or None to leave unchanged.
            tags: New tags, or None to leave unchanged.
            labels: New labels, or None to leave unchanged.
        """
        body = _update_body(name=name, tags=tags, labels=labels)
        response = await self._client._request("PATCH", f"/organizations/{entity_id}", json=body)
        return Organization.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete an organization.

        Args:
            entity_id: Organization ID.
        """
        await self._client._request("DELETE", f"/organizations/{entity_id}")


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
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name}
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body


def _update_body(
    *,
    name: str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
