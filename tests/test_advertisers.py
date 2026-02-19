from __future__ import annotations

import httpx
import pytest
import respx
from conftest import advertiser_json, error_response, list_response

from mataki import Advertiser, Mataki, NotFoundError


class TestAdvertisersList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/advertisers").mock(
            return_value=httpx.Response(200, json=list_response([advertiser_json(), advertiser_json(name="Other")]))
        )

        page = client.advertisers.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Advertiser)
        assert page.data[0].name == "Test Advertiser"
        assert page.data[1].name == "Other"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/advertisers").mock(return_value=httpx.Response(200, json=list_response([])))

        client.advertisers.list(query="name ~* %acme%", sort="name:asc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "name ~* %acme%"
        assert request.url.params["sort"] == "name:asc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestAdvertisersGet:
    def test_get_returns_advertiser(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=advertiser_json())
        )

        adv = client.advertisers.get("adv_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(adv, Advertiser)
        assert adv.id == "adv_4K7fR9pLm2nQwXvY8cJH3"
        assert adv.name == "Test Advertiser"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/advertisers/adv_nonexistent00000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.advertisers.get("adv_nonexistent00000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestAdvertisersCreate:
    def test_create_returns_advertiser(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/advertisers").mock(return_value=httpx.Response(201, json=advertiser_json(name="Acme Corp")))

        adv = client.advertisers.create(name="Acme Corp")

        assert isinstance(adv, Advertiser)
        assert adv.name == "Acme Corp"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/advertisers").mock(return_value=httpx.Response(201, json=advertiser_json()))

        client.advertisers.create(name="Acme", tags=["prod"], labels={"env": "live"})

        import json

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "Acme"
        assert body["tags"] == ["prod"]
        assert body["labels"] == {"env": "live"}

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/advertisers").mock(return_value=httpx.Response(201, json=advertiser_json()))

        client.advertisers.create(name="Acme")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "Acme"}


class TestAdvertisersUpdate:
    def test_update_returns_advertiser(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=advertiser_json(name="Updated"))
        )

        adv = client.advertisers.update("adv_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert adv.name == "Updated"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=advertiser_json())
        )

        client.advertisers.update("adv_4K7fR9pLm2nQwXvY8cJH3", name="New Name")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "New Name"}
        assert "tags" not in body
        assert "labels" not in body


class TestAdvertisersDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.advertisers.delete("adv_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncAdvertisers:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/advertisers").mock(return_value=httpx.Response(200, json=list_response([advertiser_json()])))

        page = await async_client.advertisers.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test Advertiser"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=advertiser_json())
        )

        adv = await async_client.advertisers.get("adv_4K7fR9pLm2nQwXvY8cJH3")

        assert adv.name == "Test Advertiser"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/advertisers").mock(return_value=httpx.Response(201, json=advertiser_json(name="New")))

        adv = await async_client.advertisers.create(name="New")

        assert adv.name == "New"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=advertiser_json(name="Updated"))
        )

        adv = await async_client.advertisers.update("adv_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert adv.name == "Updated"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/advertisers/adv_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.advertisers.delete("adv_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
