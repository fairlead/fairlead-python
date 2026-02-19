from __future__ import annotations

import json

import httpx
import pytest
import respx
from conftest import ad_json, error_response, line_item_json, list_response

from mataki import Ad, LineItem, Mataki, NotFoundError


class TestLineItemsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/line-items").mock(
            return_value=httpx.Response(200, json=list_response([line_item_json(), line_item_json(bid_strategy="cpm")]))
        )

        page = client.line_items.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], LineItem)
        assert page.data[0].bid_strategy == "cpc"
        assert page.data[1].bid_strategy == "cpm"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/line-items").mock(return_value=httpx.Response(200, json=list_response([])))

        client.line_items.list(query="campaign_id = cmp_123", sort="priority:desc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "campaign_id = cmp_123"
        assert request.url.params["sort"] == "priority:desc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestLineItemsGet:
    def test_get_returns_line_item(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=line_item_json())
        )

        li = client.line_items.get("li_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(li, LineItem)
        assert li.id == "li_4K7fR9pLm2nQwXvY8cJH3"
        assert li.bid_strategy == "cpc"
        assert li.bid_amount_cents == 150

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/line-items/li_nonexistent000000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.line_items.get("li_nonexistent000000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestLineItemsCreate:
    def test_create_returns_line_item(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        li = client.line_items.create(
            campaign_id="cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        assert isinstance(li, LineItem)
        assert li.bid_strategy == "cpc"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        client.line_items.create(
            campaign_id="cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
            priority=5,
            tags=["test"],
        )

        body = json.loads(route.calls[0].request.content)
        assert body["bid_strategy"] == "cpc"
        assert body["bid_amount_cents"] == 150
        assert body["priority"] == 5
        assert body["tags"] == ["test"]
        # campaign_id should NOT be in the body (it's in the URL path)
        assert "campaign_id" not in body

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        client.line_items.create(
            campaign_id="cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        body = json.loads(route.calls[0].request.content)
        assert body == {"bid_strategy": "cpc", "bid_amount_cents": 150}


class TestLineItemsCreateAd:
    def test_create_ad_returns_ad(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(return_value=httpx.Response(201, json=ad_json()))

        ad = client.line_items.create_ad("li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        assert isinstance(ad, Ad)
        assert ad.id == "ad_4K7fR9pLm2nQwXvY8cJH3"
        assert ad.ad_type == "listing_ref"

    def test_create_ad_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(
            return_value=httpx.Response(201, json=ad_json())
        )

        client.line_items.create_ad(
            "li_4K7fR9pLm2nQwXvY8cJH3",
            ad_type="listing_ref",
            external_item_id="ext_123",
            quality_score="0.95",
            status="active",
            tags=["test"],
            labels={"env": "live"},
        )

        body = json.loads(route.calls[0].request.content)
        assert body["ad_type"] == "listing_ref"
        assert body["external_item_id"] == "ext_123"
        assert body["quality_score"] == "0.95"
        assert body["status"] == "active"
        assert body["tags"] == ["test"]
        assert body["labels"] == {"env": "live"}
        # line_item_id should NOT be in the body (it's in the URL path)
        assert "line_item_id" not in body

    def test_create_ad_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(
            return_value=httpx.Response(201, json=ad_json())
        )

        client.line_items.create_ad("li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        body = json.loads(route.calls[0].request.content)
        assert body == {"ad_type": "listing_ref"}


class TestLineItemsUpdate:
    def test_update_returns_line_item(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=line_item_json(bid_amount_cents=200))
        )

        li = client.line_items.update("li_4K7fR9pLm2nQwXvY8cJH3", bid_amount_cents=200)

        assert li.bid_amount_cents == 200

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=line_item_json())
        )

        client.line_items.update("li_4K7fR9pLm2nQwXvY8cJH3", bid_amount_cents=200)

        body = json.loads(route.calls[0].request.content)
        assert body == {"bid_amount_cents": 200}
        assert "tags" not in body
        assert "labels" not in body


class TestLineItemsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.line_items.delete("li_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncLineItems:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/line-items").mock(return_value=httpx.Response(200, json=list_response([line_item_json()])))

        page = await async_client.line_items.list()

        assert len(page.data) == 1
        assert page.data[0].bid_strategy == "cpc"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=line_item_json())
        )

        li = await async_client.line_items.get("li_4K7fR9pLm2nQwXvY8cJH3")

        assert li.bid_strategy == "cpc"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        li = await async_client.line_items.create(
            campaign_id="cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        assert li.bid_strategy == "cpc"

    async def test_create_ad(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/line-items/li_4K7fR9pLm2nQwXvY8cJH3/ads").mock(return_value=httpx.Response(201, json=ad_json()))

        ad = await async_client.line_items.create_ad("li_4K7fR9pLm2nQwXvY8cJH3", ad_type="listing_ref")

        assert isinstance(ad, Ad)
        assert ad.ad_type == "listing_ref"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=line_item_json(bid_amount_cents=200))
        )

        li = await async_client.line_items.update("li_4K7fR9pLm2nQwXvY8cJH3", bid_amount_cents=200)

        assert li.bid_amount_cents == 200

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/line-items/li_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.line_items.delete("li_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
