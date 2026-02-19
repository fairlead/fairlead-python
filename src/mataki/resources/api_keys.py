from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List

from mataki._pagination import AsyncPage, SyncPage, _parse_async_page, _parse_sync_page
from mataki.types.api_key import ApiKey, CreateApiKeyResponse, Environment, Role

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki


class ApiKeysResource:
    """Synchronous API keys API."""

    def __init__(self, client: "Mataki") -> None:
        self._client = client

    def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> SyncPage[ApiKey]:
        """List API keys with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``role = admin``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of API keys. Iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = self._client._request("GET", "/api-keys", params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path="/api-keys",
            params=params,
            model=ApiKey,
        )

    def create(
        self,
        *,
        name: str,
        role: Role | str | None = None,
        scopes: List[str] | None = None,
        expires_at: datetime | str | None = None,
        environment: Environment | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> CreateApiKeyResponse:
        """Create a new API key. The raw key is returned once and cannot be retrieved again.

        Args:
            name: Display name (1-255 characters).
            role: Key role (admin, member, viewer). Defaults to member.
            scopes: Explicit scopes. Empty list inherits from role.
            expires_at: Expiration datetime, or None for no expiry.
            environment: Key environment (live, test). Defaults to live.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            role=role,
            scopes=scopes,
            expires_at=expires_at,
            environment=environment,
            tags=tags,
            labels=labels,
        )
        response = self._client._request("POST", "/api-keys", json=body)
        return CreateApiKeyResponse.model_validate(response.json())

    def delete(self, entity_id: str) -> None:
        """Delete an API key.

        Args:
            entity_id: API key ID (e.g. ``key_7mN3pR9xK2wLvY8cJH4fQ``).
        """
        self._client._request("DELETE", f"/api-keys/{entity_id}")


class AsyncApiKeysResource:
    """Asynchronous API keys API."""

    def __init__(self, client: "AsyncMataki") -> None:
        self._client = client

    async def list(
        self,
        *,
        query: str | None = None,
        sort: str | None = None,
        offset: int = 0,
        limit: int = 25,
    ) -> AsyncPage[ApiKey]:
        """List API keys with optional filtering, sorting, and pagination.

        Args:
            query: Filter expression (e.g. ``role = admin``).
            sort: Sort clause (e.g. ``name:asc``).
            offset: Number of items to skip.
            limit: Maximum items to return (1-100).

        Returns:
            A page of API keys. Async-iterate directly to auto-paginate.
        """
        params = _list_params(query=query, sort=sort, offset=offset, limit=limit)
        response = await self._client._request("GET", "/api-keys", params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path="/api-keys",
            params=params,
            model=ApiKey,
        )

    async def create(
        self,
        *,
        name: str,
        role: Role | str | None = None,
        scopes: List[str] | None = None,
        expires_at: datetime | str | None = None,
        environment: Environment | str | None = None,
        tags: List[str] | None = None,
        labels: Dict[str, str] | None = None,
    ) -> CreateApiKeyResponse:
        """Create a new API key. The raw key is returned once and cannot be retrieved again.

        Args:
            name: Display name (1-255 characters).
            role: Key role (admin, member, viewer). Defaults to member.
            scopes: Explicit scopes. Empty list inherits from role.
            expires_at: Expiration datetime, or None for no expiry.
            environment: Key environment (live, test). Defaults to live.
            tags: Freeform tags for categorization.
            labels: Key-value labels for filtering.
        """
        body = _create_body(
            name=name,
            role=role,
            scopes=scopes,
            expires_at=expires_at,
            environment=environment,
            tags=tags,
            labels=labels,
        )
        response = await self._client._request("POST", "/api-keys", json=body)
        return CreateApiKeyResponse.model_validate(response.json())

    async def delete(self, entity_id: str) -> None:
        """Delete an API key.

        Args:
            entity_id: API key ID (e.g. ``key_7mN3pR9xK2wLvY8cJH4fQ``).
        """
        await self._client._request("DELETE", f"/api-keys/{entity_id}")


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
    role: Role | str | None,
    scopes: list[str] | None,
    expires_at: datetime | str | None,
    environment: Environment | str | None,
    tags: list[str] | None,
    labels: dict[str, str] | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name}
    if role is not None:
        body["role"] = str(role)
    if scopes is not None:
        body["scopes"] = scopes
    if expires_at is not None:
        body["expires_at"] = expires_at if isinstance(expires_at, str) else expires_at.isoformat()
    if environment is not None:
        body["environment"] = str(environment)
    if tags is not None:
        body["tags"] = tags
    if labels is not None:
        body["labels"] = labels
    return body
