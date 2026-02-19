from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar

# NOTE: `from __future__ import annotations` is needed here to avoid
# circular import issues with the TYPE_CHECKING-guarded client types.
from pydantic import BaseModel

from mataki.types.shared import OffsetPaginationMeta

if TYPE_CHECKING:
    from mataki._client import AsyncMataki, Mataki

T = TypeVar("T", bound=BaseModel)


class SyncPage(Generic[T]):
    """A single page of results that supports auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Offset pagination metadata.
        meta: Additional response metadata.
    """

    data: list[T]
    pagination: OffsetPaginationMeta
    meta: dict[str, Any]

    def __init__(
        self,
        *,
        data: list[T],
        pagination: OffsetPaginationMeta,
        meta: dict[str, Any],
        client: Mataki,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self.meta = meta
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    def __iter__(self) -> Iterator[T]:
        """Iterate through all items across all pages (auto-pagination)."""
        page: SyncPage[T] = self
        while True:
            yield from page.data
            if page._is_last_page():
                break
            page = page._fetch_next_page()

    def _is_last_page(self) -> bool:
        if len(self.data) < self.pagination.limit:
            return True
        if self.pagination.total_results is not None:
            return self.pagination.offset + self.pagination.limit >= self.pagination.total_results
        return False

    def _fetch_next_page(self) -> SyncPage[T]:
        next_offset = self.pagination.offset + self.pagination.limit
        params = {**self._params, "offset": next_offset}
        response = self._client._request("GET", self._path, params=params)
        return _parse_sync_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


class AsyncPage(Generic[T]):
    """A single page of results that supports async auto-pagination via iteration.

    Attributes:
        data: The items on this page.
        pagination: Offset pagination metadata.
        meta: Additional response metadata.
    """

    data: list[T]
    pagination: OffsetPaginationMeta
    meta: dict[str, Any]

    def __init__(
        self,
        *,
        data: list[T],
        pagination: OffsetPaginationMeta,
        meta: dict[str, Any],
        client: AsyncMataki,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.pagination = pagination
        self.meta = meta
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    async def __aiter__(self) -> AsyncIterator[T]:
        """Iterate through all items across all pages (async auto-pagination)."""
        page: AsyncPage[T] = self
        while True:
            for item in page.data:
                yield item
            if page._is_last_page():
                break
            page = await page._fetch_next_page()

    def _is_last_page(self) -> bool:
        if len(self.data) < self.pagination.limit:
            return True
        if self.pagination.total_results is not None:
            return self.pagination.offset + self.pagination.limit >= self.pagination.total_results
        return False

    async def _fetch_next_page(self) -> AsyncPage[T]:
        next_offset = self.pagination.offset + self.pagination.limit
        params = {**self._params, "offset": next_offset}
        response = await self._client._request("GET", self._path, params=params)
        return _parse_async_page(
            data=response.json(),
            client=self._client,
            path=self._path,
            params=params,
            model=self._model,
        )


def _parse_sync_page(
    *,
    data: dict[str, Any],
    client: Mataki,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> SyncPage[T]:
    """Parse a list response JSON into a SyncPage."""
    items = [model.model_validate(item) for item in data["data"]]
    pagination = OffsetPaginationMeta.model_validate(data["pagination"])
    return SyncPage(
        data=items,
        pagination=pagination,
        meta=data.get("meta", {}),
        client=client,
        path=path,
        params=params,
        model=model,
    )


def _parse_async_page(
    *,
    data: dict[str, Any],
    client: AsyncMataki,
    path: str,
    params: dict[str, Any],
    model: type[T],
) -> AsyncPage[T]:
    """Parse a list response JSON into an AsyncPage."""
    items = [model.model_validate(item) for item in data["data"]]
    pagination = OffsetPaginationMeta.model_validate(data["pagination"])
    return AsyncPage(
        data=items,
        pagination=pagination,
        meta=data.get("meta", {}),
        client=client,
        path=path,
        params=params,
        model=model,
    )
