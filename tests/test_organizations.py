from __future__ import annotations

import httpx
import pytest
import respx
from conftest import error_response, list_response, org_json

from mataki import Mataki, NotFoundError, Organization


class TestOrganizationsList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations").mock(
            return_value=httpx.Response(200, json=list_response([org_json(), org_json(name="Other")]))
        )

        page = client.organizations.list()

        assert len(page.data) == 2
        assert isinstance(page.data[0], Organization)
        assert page.data[0].name == "Test Org"
        assert page.data[1].name == "Other"
        assert page.pagination.offset == 0
        assert page.pagination.limit == 25

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/organizations").mock(return_value=httpx.Response(200, json=list_response([])))

        client.organizations.list(query="name ~* %acme%", sort="name:asc", offset=10, limit=5)

        request = route.calls[0].request
        assert request.url.params["query"] == "name ~* %acme%"
        assert request.url.params["sort"] == "name:asc"
        assert request.url.params["offset"] == "10"
        assert request.url.params["limit"] == "5"


class TestOrganizationsGet:
    def test_get_returns_organization(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=org_json()))

        org = client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")

        assert isinstance(org, Organization)
        assert org.id == "org_4K7fR9pLm2nQwXvY8cJH3"
        assert org.name == "Test Org"

    def test_get_not_found_raises(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_nonexistent00000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.organizations.get("org_nonexistent00000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found"
        assert exc_info.value.request_id == "req_123"


class TestOrganizationsCreate:
    def test_create_returns_organization(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.post("/organizations").mock(return_value=httpx.Response(201, json=org_json(name="Acme Corp")))

        org = client.organizations.create(name="Acme Corp")

        assert isinstance(org, Organization)
        assert org.name == "Acme Corp"

    def test_create_sends_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/organizations").mock(return_value=httpx.Response(201, json=org_json()))

        client.organizations.create(name="Acme", tags=["prod"], labels={"env": "live"})

        import json

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "Acme"
        assert body["tags"] == ["prod"]
        assert body["labels"] == {"env": "live"}

    def test_create_omits_none_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/organizations").mock(return_value=httpx.Response(201, json=org_json()))

        client.organizations.create(name="Acme")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "Acme"}


class TestOrganizationsUpdate:
    def test_update_returns_organization(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.patch("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=org_json(name="Updated"))
        )

        org = client.organizations.update("org_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert org.name == "Updated"

    def test_update_sends_partial_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.patch("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=org_json())
        )

        client.organizations.update("org_4K7fR9pLm2nQwXvY8cJH3", name="New Name")

        import json

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "New Name"}
        assert "tags" not in body
        assert "labels" not in body


class TestOrganizationsDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        client.organizations.delete("org_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called


class TestAsyncOrganizations:
    async def test_list(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/organizations").mock(return_value=httpx.Response(200, json=list_response([org_json()])))

        page = await async_client.organizations.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test Org"

    async def test_get(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.get("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(200, json=org_json()))

        org = await async_client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")

        assert org.name == "Test Org"

    async def test_create(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.post("/organizations").mock(return_value=httpx.Response(201, json=org_json(name="New")))

        org = await async_client.organizations.create(name="New")

        assert org.name == "New"

    async def test_update(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        mock_api.patch("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(
            return_value=httpx.Response(200, json=org_json(name="Updated"))
        )

        org = await async_client.organizations.update("org_4K7fR9pLm2nQwXvY8cJH3", name="Updated")

        assert org.name == "Updated"

    async def test_delete(self, mock_api: respx.MockRouter, async_client: object) -> None:
        from mataki import AsyncMataki

        assert isinstance(async_client, AsyncMataki)
        route = mock_api.delete("/organizations/org_4K7fR9pLm2nQwXvY8cJH3").mock(return_value=httpx.Response(204))

        await async_client.organizations.delete("org_4K7fR9pLm2nQwXvY8cJH3")

        assert route.called
