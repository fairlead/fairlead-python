from __future__ import annotations

import httpx
import pytest
import respx
from conftest import error_response, list_response, placement_json

from mataki import Mataki, NotFoundError, Placement


class TestPlacementsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/placements").mock(
            return_value=httpx.Response(200, json=list_response([placement_json(), placement_json(name="Other")]))
        )

        page = client.placements.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Placement)
        assert page.data[0].name == "Test Placement"
        assert page.data[1].name == "Other"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/placements").mock(return_value=httpx.Response(200, json=list_response([])))

        client.placements.list(query="ad_format = native", sort="name:asc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "ad_format = native"
        assert request.url.params["sort"] == "name:asc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestPlacementsGet:
    def test_get_returns_placement(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=placement_json())
        )

        plc = client.placements.get("plc_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(plc, Placement)
        assert plc.id == "plc_4K7fR9pLm2nQwXvY8cJH3"
        assert plc.name == "Test Placement"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/placements/plc_nonexistent00000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.placements.get("plc_nonexistent00000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestPlacementsCreate:
    def test_create_returns_placement(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/placements").mock(return_value=httpx.Response(201, json=placement_json(name="Homepage")))

        plc = client.placements.create(name="Homepage", slug="homepage", ad_format="sponsored_listing")

        assert isinstance(plc, Placement)
        assert plc.name == "Homepage"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/placements").mock(return_value=httpx.Response(201, json=placement_json()))

        client.placements.create(
            name="Homepage",
            slug="homepage",
            ad_format="sponsored_listing",
            max_ads=5,
            tags=["prod"],
            labels={"env": "live"},
        )

        import json

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "Homepage"
        assert body["slug"] == "homepage"
        assert body["ad_format"] == "sponsored_listing"
        assert body["max_ads"] == 5
        assert body["tags"] == ["prod"]
        assert body["labels"] == {"env": "live"}

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/placements").mock(return_value=httpx.Response(201, json=placement_json()))

        client.placements.create(name="Homepage", slug="homepage", ad_format="sponsored_listing")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "Homepage", "slug": "homepage", "ad_format": "sponsored_listing"}


class TestPlacementsUpdate:
    def test_update_returns_placement(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=placement_json(name="Updated"))
        )

        plc = client.placements.update("plc_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert plc.name == "Updated"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=placement_json())
        )

        client.placements.update("plc_4K7fR9pLm2nQwXvY8cJH3", name="New Name")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "New Name"}
        assert "tags" not in body
        assert "labels" not in body


class TestPlacementsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.placements.delete("plc_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncPlacements:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/placements").mock(return_value=httpx.Response(200, json=list_response([placement_json()])))

        page = await async_client.placements.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test Placement"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=placement_json())
        )

        plc = await async_client.placements.get("plc_4K7fR9pLm2nQwXvY8cJH3")

        assert plc.name == "Test Placement"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/placements").mock(return_value=httpx.Response(201, json=placement_json(name="New")))

        plc = await async_client.placements.create(name="New", slug="new", ad_format="native")

        assert plc.name == "New"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=placement_json(name="Updated"))
        )

        plc = await async_client.placements.update("plc_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert plc.name == "Updated"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/placements/plc_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.placements.delete("plc_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
