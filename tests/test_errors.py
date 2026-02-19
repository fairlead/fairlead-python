from __future__ import annotations

import httpx
import pytest
import respx
from conftest import error_response

from mataki import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    Mataki,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from mataki._errors import ConnectionError as MatakiConnectionError


class TestErrorMapping:
    def test_400_raises_bad_request(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                400,
                json=error_response(type="invalid_request_error", message="Invalid request", code=400),
            )
        )

        with pytest.raises(BadRequestError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 400
        assert exc_info.value.error_type == "invalid_request_error"
        assert exc_info.value.message == "Invalid request"

    def test_401_raises_authentication_error(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                401,
                json=error_response(type="authentication_error", message="Invalid API key", code=401),
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 401

    def test_403_raises_permission_denied(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                403,
                json=error_response(type="authentication_error", message="Forbidden", code=403),
            )
        )

        with pytest.raises(PermissionDeniedError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 403

    def test_404_raises_not_found(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(404, json=error_response())
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 404
        assert exc_info.value.request_id == "req_123"

    def test_429_raises_rate_limit(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                429,
                json=error_response(type="invalid_request_error", message="Rate limited", code=429),
            )
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 429

    def test_500_raises_internal_server_error(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                500,
                json=error_response(type="api_error", message="Internal error", code=500),
            )
        )

        with pytest.raises(InternalServerError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 500

    def test_unknown_status_raises_api_error(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                502,
                json=error_response(type="api_error", message="Bad gateway", code=502),
            )
        )

        with pytest.raises(APIError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 502
        # Should be generic APIError, not a specific subclass
        assert type(exc_info.value) is APIError


class TestErrorAttributes:
    def test_error_has_all_attributes(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(
                400,
                json=error_response(
                    type="invalid_request_error",
                    message="Validation failed",
                    code=400,
                    request_id="req_abc",
                    details=[{"field": "name", "code": "required", "message": "Name is required"}],
                ),
            )
        )

        with pytest.raises(BadRequestError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        err = exc_info.value
        assert err.message == "Validation failed"
        assert err.status_code == 400
        assert err.error_type == "invalid_request_error"
        assert err.request_id == "req_abc"
        assert err.details is not None
        assert len(err.details) == 1
        assert err.details[0].field == "name"
        assert err.details[0].code == "required"
        assert err.details[0].message == "Name is required"

    def test_non_json_error_response(self, mock_api: respx.MockRouter, client: Mataki) -> None:
        mock_api.get("/organizations/org_test0000000000000000").mock(
            return_value=httpx.Response(502, text="<html>Bad Gateway</html>")
        )

        with pytest.raises(APIError) as exc_info:
            client.organizations.get("org_test0000000000000000")

        assert exc_info.value.status_code == 502
        assert "<html>" in exc_info.value.message


class TestConnectionErrors:
    def test_connect_error(self, client: Mataki) -> None:
        with respx.mock(base_url="https://api.mataki.dev") as mock:
            mock.get("/organizations/org_test0000000000000000").mock(
                side_effect=httpx.ConnectError("Connection refused"),
            )

            with pytest.raises(MatakiConnectionError) as exc_info:
                client.organizations.get("org_test0000000000000000")

            assert "Connection refused" in exc_info.value.message

    def test_timeout_error(self, client: Mataki) -> None:
        with respx.mock(base_url="https://api.mataki.dev") as mock:
            mock.get("/organizations/org_test0000000000000000").mock(side_effect=httpx.ReadTimeout("Read timed out"))

            with pytest.raises(MatakiConnectionError) as exc_info:
                client.organizations.get("org_test0000000000000000")

            assert "timed out" in exc_info.value.message
