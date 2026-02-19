from __future__ import annotations

import json

import httpx
import pytest
import respx
from conftest import ad_json, error_response, list_response

from mataki import Ad, Mataki, NotFoundError


class TestAdsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/ads").mock(
            return_value=httpx.Response(200, json=list_response([ad_json(), ad_json(ad_type="native")]))
        )

        page = client.ads.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Ad)
        assert page.data[0].ad_type == "listing_ref"
        assert page.data[1].ad_type == "native"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/ads").mock(return_value=httpx.Response(200, json=list_response([])))

        client.ads.list(query="line_item_id = li_123", sort="ad_type:asc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "line_item_id = li_123"
        assert request.url.params["sort"] == "ad_type:asc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestAdsGet:
    def test_get_returns_ad(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=ad_json()))

        ad = client.ads.get("ad_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(ad, Ad)
        assert ad.id == "ad_4K7fR9pLm2nQwXvY8cJH3"
        assert ad.ad_type == "listing_ref"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/ads/ad_nonexistent000000000").mock(return_value=httpx.Response(404, json=error_response()))

        with pytest.raises(NotFoundError) as exc_info:
            client.ads.get("ad_nonexistent000000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestAdsCreate:
    def test_create_returns_ad(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(return_value=httpx.Response(201, json=ad_json()))

        ad = client.ads.create(line_item_id="li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        assert isinstance(ad, Ad)
        assert ad.ad_type == "listing_ref"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(
            return_value=httpx.Response(201, json=ad_json())
        )

        client.ads.create(
            line_item_id="li_4K7fR9pLm2nQwXvY8cJH3",
            ad_type="listing_ref",
            external_item_id="ext_123",
            quality_score="0.95",
            tags=["test"],
        )

        body = json.loads(route.calls[0].request.content)
        assert body["ad_type"] == "listing_ref"
        assert body["external_item_id"] == "ext_123"
        assert body["quality_score"] == "0.95"
        assert body["tags"] == ["test"]
        # line_item_id should NOT be in the body (it's in the URL path)
        assert "line_item_id" not in body

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(
            return_value=httpx.Response(201, json=ad_json())
        )

        client.ads.create(line_item_id="li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        body = json.loads(route.calls[0].request.content)
        assert body == {"ad_type": "listing_ref"}


class TestAdsUpdate:
    def test_update_returns_ad(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=ad_json(status="paused"))
        )

        ad = client.ads.update("ad_4K7fR9pLm2nQwXvY8cJH3", status="paused")

        assert ad.status == "paused"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=ad_json()))

        client.ads.update("ad_4K7fR9pLm2nQwXvY8cJH3", status="paused")

        body = json.loads(route.calls[0].request.content)
        assert body == {"status": "paused"}
        assert "tags" not in body
        assert "labels" not in body


class TestAdsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.ads.delete("ad_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncAds:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/ads").mock(return_value=httpx.Response(200, json=list_response([ad_json()])))

        page = await async_client.ads.list()

        assert len(page.data) == 1
        assert page.data[0].ad_type == "listing_ref"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=ad_json()))

        ad = await async_client.ads.get("ad_4K7fR9pLm2nQwXvY8cJH3")

        assert ad.ad_type == "listing_ref"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(return_value=httpx.Response(201, json=ad_json()))

        ad = await async_client.ads.create(line_item_id="li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        assert ad.ad_type == "listing_ref"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=ad_json(status="paused"))
        )

        ad = await async_client.ads.update("ad_4K7fR9pLm2nQwXvY8cJH3", status="paused")

        assert ad.status == "paused"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/ads/ad_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.ads.delete("ad_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
