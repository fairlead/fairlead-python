from __future__ import annotations

from typing import Any

import httpx

from mataki._config import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    DEFAULT_VERSION,
    ClientConfig,
)
from mataki._errors import ConnectionError as MatakiConnectionError
from mataki._errors import _make_api_error
from mataki._version import __version__
from mataki.resources.ads import AdsResource, AsyncAdsResource
from mataki.resources.advertisers import AdvertisersResource, AsyncAdvertisersResource
from mataki.resources.api_keys import ApiKeysResource, AsyncApiKeysResource
from mataki.resources.campaigns import AsyncCampaignsResource, CampaignsResource
from mataki.resources.line_items import AsyncLineItemsResource, LineItemsResource
from mataki.resources.organizations import AsyncOrganizationsResource, OrganizationsResource
from mataki.resources.placements import AsyncPlacementsResource, PlacementsResource


class _BaseClient:
    """Shared logic for sync and async Mataki clients."""

    _config: ClientConfig

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        version: str = DEFAULT_VERSION,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._config = ClientConfig(
            api_key=api_key,
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            version=version,
            max_retries=max_retries,
        )

    @property
    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._config.api_key}",
            "Mataki-Version": self._config.version,
            "User-Agent": f"mataki-python/{__version__}",
            "Accept": "application/json",
        }

    @staticmethod
    def _process_response(response: httpx.Response) -> httpx.Response:
        """Check response status and raise the appropriate error on failure."""
        if response.is_success:
            return response
        raise _make_api_error(response)


class Mataki(_BaseClient):
    """Synchronous Mataki API client.

    Usage::

        from mataki import Mataki

        client = Mataki(api_key="mk_live_...")
        orgs = client.organizations.list()

        # As a context manager
        with Mataki(api_key="mk_live_...") as client:
            org = client.organizations.get("org_...")
    """

    organizations: OrganizationsResource
    api_keys: ApiKeysResource
    advertisers: AdvertisersResource
    campaigns: CampaignsResource
    line_items: LineItemsResource
    ads: AdsResource
    placements: PlacementsResource

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.Client(
            base_url=self._config.base_url,
            headers=self._default_headers,
            timeout=self._config.timeout,
        )
        self.organizations = OrganizationsResource(self)
        self.api_keys = ApiKeysResource(self)
        self.advertisers = AdvertisersResource(self)
        self.campaigns = CampaignsResource(self)
        self.line_items = LineItemsResource(self)
        self.ads = AdsResource(self)
        self.placements = PlacementsResource(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Send a synchronous HTTP request and process the response."""
        try:
            response = self._http.request(method, path, params=params, json=json)
        except httpx.ConnectError as exc:
            raise MatakiConnectionError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise MatakiConnectionError(f"Request timed out: {exc}") from exc
        return self._process_response(response)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> Mataki:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncMataki(_BaseClient):
    """Asynchronous Mataki API client.

    Usage::

        from mataki import AsyncMataki

        client = AsyncMataki(api_key="mk_live_...")
        orgs = await client.organizations.list()

        # As an async context manager
        async with AsyncMataki(api_key="mk_live_...") as client:
            org = await client.organizations.get("org_...")
    """

    organizations: AsyncOrganizationsResource
    api_keys: AsyncApiKeysResource
    advertisers: AsyncAdvertisersResource
    campaigns: AsyncCampaignsResource
    line_items: AsyncLineItemsResource
    ads: AsyncAdsResource
    placements: AsyncPlacementsResource

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            headers=self._default_headers,
            timeout=self._config.timeout,
        )
        self.organizations = AsyncOrganizationsResource(self)
        self.api_keys = AsyncApiKeysResource(self)
        self.advertisers = AsyncAdvertisersResource(self)
        self.campaigns = AsyncCampaignsResource(self)
        self.line_items = AsyncLineItemsResource(self)
        self.ads = AsyncAdsResource(self)
        self.placements = AsyncPlacementsResource(self)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Send an asynchronous HTTP request and process the response."""
        try:
            response = await self._http.request(method, path, params=params, json=json)
        except httpx.ConnectError as exc:
            raise MatakiConnectionError(str(exc)) from exc
        except httpx.TimeoutException as exc:
            raise MatakiConnectionError(f"Request timed out: {exc}") from exc
        return self._process_response(response)

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncMataki:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
