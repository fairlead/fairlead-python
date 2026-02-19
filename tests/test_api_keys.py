from __future__ import annotations

import json

import httpx
import respx
from conftest import api_key_json, list_response

from mataki import ApiKey, AsyncMataki, CreateApiKeyResponse, Mataki


class TestApiKeysList:
    def test_list_returns_page(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/api-keys").mock(return_value=httpx.Response(200, json=list_response([api_key_json()])))

        page = client.api_keys.list()

        assert len(page.data) == 1
        assert isinstance(page.data[0], ApiKey)
        assert page.data[0].name == "Test Key"
        assert page.data[0].role == "member"
        assert page.data[0].environment == "test"

    def test_list_passes_query_params(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.get("/api-keys").mock(return_value=httpx.Response(200, json=list_response([])))

        client.api_keys.list(query="role = admin", sort="name:asc", offset=5, limit=10)

        request = route.calls[0].request
        assert request.url.params["query"] == "role = admin"
        assert request.url.params["sort"] == "name:asc"
        assert request.url.params["offset"] == "5"
        assert request.url.params["limit"] == "10"


class TestApiKeysCreate:
    def test_create_returns_response_with_raw_key(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        response_data = {
            "api_key": api_key_json(),
            "raw_key": "mk_test_abc123def456ghi789",
        }
        mock_api.post("/api-keys").mock(return_value=httpx.Response(201, json=response_data))

        result = client.api_keys.create(name="Test Key")

        assert isinstance(result, CreateApiKeyResponse)
        assert isinstance(result.api_key, ApiKey)
        assert result.raw_key == "mk_test_abc123def456ghi789"

    def test_create_sends_minimal_body(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/api-keys").mock(
            return_value=httpx.Response(201, json={"api_key": api_key_json(), "raw_key": "mk_test_x"})
        )

        client.api_keys.create(name="My Key")

        body = json.loads(route.calls[0].request.content)
        assert body == {"name": "My Key"}

    def test_create_sends_all_fields(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.post("/api-keys").mock(
            return_value=httpx.Response(201, json={"api_key": api_key_json(), "raw_key": "mk_test_x"})
        )

        client.api_keys.create(
            name="Admin Key",
            role="admin",
            scopes=["organizations:read"],
            expires_at="2026-12-31T23:59:59Z",
            environment="live",
            tags=["production"],
            labels={"team": "platform"},
        )

        body = json.loads(route.calls[0].request.content)
        assert body["name"] == "Admin Key"
        assert body["role"] == "admin"
        assert body["scopes"] == ["organizations:read"]
        assert body["expires_at"] == "2026-12-31T23:59:59Z"
        assert body["environment"] == "live"
        assert body["tags"] == ["production"]
        assert body["labels"] == {"team": "platform"}


class TestApiKeysDelete:
    def test_delete_returns_none(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        route = mock_api.delete("/api-keys/key_7mN3pR9xK2wLvY8cJH4fQ").mock(return_value=httpx.Response(204))

        client.api_keys.delete("key_7mN3pR9xK2wLvY8cJH4fQ")

        assert route.called


class TestAsyncApiKeys:
    async def test_list(self, mock_api: respx.MockRouter, async_client: AsyncMataki) -> None:
        mock_api.get("/api-keys").mock(return_value=httpx.Response(200, json=list_response([api_key_json()])))

        page = await async_client.api_keys.list()

        assert len(page.data) == 1
        assert page.data[0].name == "Test Key"

    async def test_create(self, mock_api: respx.MockRouter, async_client: AsyncMataki) -> None:
        mock_api.post("/api-keys").mock(
            return_value=httpx.Response(201, json={"api_key": api_key_json(), "raw_key": "mk_test_x"})
        )

        result = await async_client.api_keys.create(name="Async Key")

        assert isinstance(result, CreateApiKeyResponse)

    async def test_delete(self, mock_api: respx.MockRouter, async_client: AsyncMataki) -> None:
        route = mock_api.delete("/api-keys/key_7mN3pR9xK2wLvY8cJH4fQ").mock(return_value=httpx.Response(204))

        await async_client.api_keys.delete("key_7mN3pR9xK2wLvY8cJH4fQ")

        assert route.called
