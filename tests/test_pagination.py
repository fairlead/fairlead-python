from __future__ import annotations

import httpx
import respx
from conftest import list_response, org_json

from mataki import AsyncMataki, Mataki, Organization


class TestSyncPagination:
    def test_single_page_attributes(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations").mock(
            return_value=httpx.Response(200, json=list_response([org_json()], offset=0, limit=25, total_results=1))
        )

        page = client.organizations.list()

        assert len(page.data) == 1
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25
        assert page.pagination.total_results == 1
        assert page.meta == {}

    def test_auto_pagination_stops_on_partial_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        """When a page has fewer items than the limit, pagination stops."""
        mock_api.get("/organizations").mock(
            return_value=httpx.Response(200, json=list_response([org_json(name="A"), org_json(name="B")], limit=5))
        )

        items = list(client.organizations.list(limit=5))

        assert len(items) == 2
        assert items[0].name == "A"
        assert items[1].name == "B"

    def test_auto_pagination_fetches_multiple_pages(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        """Auto-pagination fetches subsequent pages until a partial page is received."""
        route = mock_api.get("/organizations")
        route.side_effect = [
            httpx.Response(
                200, json=list_response([org_json(name="A"), org_json(name="B")], offset=0, limit=2, total_results=3)
            ),
            httpx.Response(200, json=list_response([org_json(name="C")], offset=2, limit=2, total_results=3)),
        ]

        items = list(client.organizations.list(limit=2))

        assert len(items) == 3
        assert [item.name for item in items] == ["A", "B", "C"]

    def test_auto_pagination_stops_on_total_results(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        """When offset + limit >= total_results, pagination stops."""
        route = mock_api.get("/organizations")
        route.side_effect = [
            httpx.Response(
                200, json=list_response([org_json(name="A"), org_json(name="B")], offset=0, limit=2, total_results=2)
            ),
        ]

        items = list(client.organizations.list(limit=2))

        assert len(items) == 2
        # Only one HTTP call should have been made (no second page fetch)
        assert len(route.calls) == 1

    def test_auto_pagination_empty_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations").mock(return_value=httpx.Response(200, json=list_response([], limit=25)))

        items = list(client.organizations.list())

        assert items == []

    def test_items_are_typed(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations").mock(
            return_value=httpx.Response(200, json=list_response([org_json()], limit=25))
        )

        for item in client.organizations.list():
            assert isinstance(item, Organization)


class TestAsyncPagination:
    async def test_async_auto_pagination(self, mock_api: respx.MockRouter, async_client: AsyncMataki) -> None:
        route = mock_api.get("/organizations")
        route.side_effect = [
            httpx.Response(
                200, json=list_response([org_json(name="X"), org_json(name="Y")], offset=0, limit=2, total_results=3)
            ),
            httpx.Response(200, json=list_response([org_json(name="Z")], offset=2, limit=2, total_results=3)),
        ]

        items = []
        async for item in await async_client.organizations.list(limit=2):
            items.append(item)

        assert len(items) == 3
        assert [item.name for item in items] == ["X", "Y", "Z"]

    async def test_async_empty_page(self, mock_api: respx.MockRouter, async_client: AsyncMataki) -> None:
        mock_api.get("/organizations").mock(return_value=httpx.Response(200, json=list_response([], limit=25)))

        items = []
        async for item in await async_client.organizations.list():
            items.append(item)

        assert items == []
