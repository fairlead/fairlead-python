from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """A single validation or field-level error detail from the API."""

    field: str | None = None
    code: str
    message: str


class MatakiError(Exception):
    """Base exception for all Mataki SDK errors."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(MatakiError):
    """An error response from the Mataki API."""

    status_code: int
    error_type: str | None
    request_id: str | None
    details: list[ErrorDetail] | None

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_type: str | None = None,
        request_id: str | None = None,
        details: list[ErrorDetail] | None = None,
    ) -> None:
        self.status_code = status_code
        self.error_type = error_type
        self.request_id = request_id
        self.details = details
        super().__init__(message)


class BadRequestError(APIError):
    """400 Bad Request."""


class AuthenticationError(APIError):
    """401 Unauthorized."""


class PermissionDeniedError(APIError):
    """403 Forbidden."""


class NotFoundError(APIError):
    """404 Not Found."""


class RateLimitError(APIError):
    """429 Too Many Requests."""


class InternalServerError(APIError):
    """500 Internal Server Error."""


class ConnectionError(MatakiError):  # noqa: A001
    """Network-level error (timeout, DNS, connection refused)."""


_STATUS_CODE_MAP: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    429: RateLimitError,
    500: InternalServerError,
}


def _make_api_error(response: httpx.Response) -> APIError:
    """Parse an error response and return the appropriate APIError subclass."""
    status_code = response.status_code
    error_cls = _STATUS_CODE_MAP.get(status_code, APIError)

    try:
        body: dict[str, Any] = response.json()
        error_data = body.get("error", {})
    except Exception:
        return error_cls(
            message=response.text or f"HTTP {status_code}",
            status_code=status_code,
        )

    message = error_data.get("message", response.text or f"HTTP {status_code}")
    error_type = error_data.get("type")
    request_id = error_data.get("request_id")

    details: list[ErrorDetail] | None = None
    raw_details = error_data.get("details")
    if raw_details is not None:
        details = [ErrorDetail.model_validate(d) for d in raw_details]

    return error_cls(
        message=message,
        status_code=status_code,
        error_type=error_type,
        request_id=request_id,
        details=details,
    )
