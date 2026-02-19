from __future__ import annotations

import json

import httpx
import pytest
import respx
from conftest import campaign_json, error_response, line_item_json, list_response

from mataki import Campaign, LineItem, Mataki, NotFoundError


class TestCampaignsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/campaigns").mock(
            return_value=httpx.Response(200, json=list_response([campaign_json(), campaign_json(name="Other")]))
        )

        page = client.campaigns.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Campaign)
        assert page.data[0].name == "Test Campaign"
        assert page.data[1].name == "Other"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/campaigns").mock(return_value=httpx.Response(200, json=list_response([])))

        client.campaigns.list(query="advertiser_id = adv_123", sort="name:asc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "advertiser_id = adv_123"
        assert request.url.params["sort"] == "name:asc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestCampaignsGet:
    def test_get_returns_campaign(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=campaign_json())
        )

        cmp = client.campaigns.get("cmp_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(cmp, Campaign)
        assert cmp.id == "cmp_4K7fR9pLm2nQwXvY8cJH3"
        assert cmp.name == "Test Campaign"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/campaigns/cmp_nonexistent00000000").mock(return_value=httpx.Response(404, json=error_response()))

        with pytest.raises(NotFoundError) as exc_info:
            client.campaigns.get("cmp_nonexistent00000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestCampaignsCreate:
    def test_create_returns_campaign(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/campaigns").mock(return_value=httpx.Response(201, json=campaign_json(name="New Campaign")))

        cmp = client.campaigns.create(advertiser_id="adv_4K7fR9pLm2nQwXvY8cJH3", name="New Campaign")

        assert isinstance(cmp, Campaign)
        assert cmp.name == "New Campaign"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns").mock(return_value=httpx.Response(201, json=campaign_json()))

        client.campaigns.create(
            advertiser_id="adv_4K7fR9pLm2nQwXvY8cJH3",
            name="Test",
            budget_total_cents=100000,
            tags=["prod"],
            labels={"env": "live"},
        )

        body = json.loads(route.calls[0].request.content)
        assert body["advertiser_id"] == "adv_4K7fR9pLm2nQwXvY8cJH3"
        assert body["name"] == "Test"
        assert body["budget_total_cents"] == 100000
        assert body["tags"] == ["prod"]
        assert body["labels"] == {"env": "live"}

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns").mock(return_value=httpx.Response(201, json=campaign_json()))

        client.campaigns.create(advertiser_id="adv_4K7fR9pLm2nQwXvY8cJH3", name="Test")

        body = json.loads(route.calls[0].request.content)
        assert body == {"advertiser_id": "adv_4K7fR9pLm2nQwXvY8cJH3", "name": "Test"}


class TestCampaignsCreateLineItem:
    def test_create_line_item_returns_line_item(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        li = client.campaigns.create_line_item(
            "cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        assert isinstance(li, LineItem)
        assert li.id == "li_4K7fR9pLm2nQwXvY8cJH3"
        assert li.bid_strategy == "cpc"

    def test_create_line_item_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        client.campaigns.create_line_item(
            "cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=200,
            bidder_type="sponsored_listing",
            status="active",
            targeting={"geo": ["US"]},
            priority=5,
            tags=["test"],
            labels={"team": "growth"},
        )

        body = json.loads(route.calls[0].request.content)
        assert body["bid_strategy"] == "cpc"
        assert body["bid_amount_cents"] == 200
        assert body["bidder_type"] == "sponsored_listing"
        assert body["status"] == "active"
        assert body["targeting"] == {"geo": ["US"]}
        assert body["priority"] == 5
        assert body["tags"] == ["test"]
        assert body["labels"] == {"team": "growth"}
        # campaign_id should NOT be in the body (it's in the URL path)
        assert "campaign_id" not in body

    def test_create_line_item_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        client.campaigns.create_line_item(
            "cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        body = json.loads(route.calls[0].request.content)
        assert body == {"bid_strategy": "cpc", "bid_amount_cents": 150}


class TestCampaignsUpdate:
    def test_update_returns_campaign(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=campaign_json(name="Updated"))
        )

        cmp = client.campaigns.update("cmp_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert cmp.name == "Updated"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=campaign_json())
        )

        client.campaigns.update("cmp_4K7fR9pLm2nQwXvY8cJH3", name="New Name")

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "New Name"}
        assert "tags" not in body
        assert "labels" not in body


class TestCampaignsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.campaigns.delete("cmp_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncCampaigns:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/campaigns").mock(return_value=httpx.Response(200, json=list_response([campaign_json()])))

        page = await async_client.campaigns.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test Campaign"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=campaign_json())
        )

        cmp = await async_client.campaigns.get("cmp_4K7fR9pLm2nQwXvY8cJH3")

        assert cmp.name == "Test Campaign"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/campaigns").mock(return_value=httpx.Response(201, json=campaign_json(name="New")))

        cmp = await async_client.campaigns.create(advertiser_id="adv_4K7fR9pLm2nQwXvY8cJH3", name="New")

        assert cmp.name == "New"

    async def test_create_line_item(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3/line-items").mock(
            return_value=httpx.Response(201, json=line_item_json())
        )

        li = await async_client.campaigns.create_line_item(
            "cmp_4K7fR9pLm2nQwXvY8cJH3",
            bid_strategy="cpc",
            bid_amount_cents=150,
        )

        assert isinstance(li, LineItem)
        assert li.bid_strategy == "cpc"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=campaign_json(name="Updated"))
        )

        cmp = await async_client.campaigns.update("cmp_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert cmp.name == "Updated"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/campaigns/cmp_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.campaigns.delete("cmp_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
