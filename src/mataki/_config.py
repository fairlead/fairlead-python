from dataclasses import dataclass

DEFAULT_BASE_URL = "https://api.mataki.dev"
DEFAULT_TIMEOUT = 60.0
DEFAULT_VERSION = "2026-02-16"
DEFAULT_MAX_RETRIES = 2


@dataclass(frozen=True)
class ClientConfig:
    """Internal configuration for the Mataki API client."""

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT
    version: str = DEFAULT_VERSION
    max_retries: int = DEFAULT_MAX_RETRIES
