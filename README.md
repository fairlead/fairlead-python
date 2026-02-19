# Mataki Python Library

[![PyPI version](https://img.shields.io/pypi/v/mataki.svg)](https://pypi.org/project/mataki/)
[![CI](https://github.com/mataki-dev/mataki-python/actions/workflows/ci.yml/badge.svg)](https://github.com/mataki-dev/mataki-python/actions/workflows/ci.yml)

The Mataki Python library provides convenient access to the [Mataki API](https://docs.mataki.dev) from Python 3.11+. It includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Installation

```sh
pip install mataki
```

## Usage

```python
from mataki import Mataki

client = Mataki(api_key="mk_live_...")

# List organizations
for org in client.organizations.list():
    print(org.name)

# Get a single organization
org = client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")

# Create an organization
org = client.organizations.create(name="Acme Corp", tags=["production"])

# Update an organization
org = client.organizations.update("org_4K7fR9pLm2nQwXvY8cJH3", name="Acme Inc")

# Delete an organization
client.organizations.delete("org_4K7fR9pLm2nQwXvY8cJH3")
```

We recommend using a context manager to ensure connections are cleaned up:

```python
with Mataki(api_key="mk_live_...") as client:
    org = client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")
```

## Async usage

Import `AsyncMataki` instead of `Mataki` and use `await` with each API call:

```python
import asyncio
from mataki import AsyncMataki


async def main():
    async with AsyncMataki(api_key="mk_live_...") as client:
        org = await client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")
        print(org.name)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is identical.

## Pagination

List methods return a page that supports automatic pagination:

```python
# Auto-paginate through all results
for org in client.organizations.list():
    print(org.name)

# Async auto-pagination
async for org in await async_client.organizations.list():
    print(org.name)
```

You can also access a single page directly:

```python
page = client.organizations.list(limit=10, offset=0)

print(page.data)        # list[Organization]
print(page.pagination)  # OffsetPaginationMeta (offset, limit, total_results)
```

## Handling errors

When the API returns a non-success status code, a subclass of `APIError` is raised:

```python
from mataki import Mataki, NotFoundError, AuthenticationError, APIError

client = Mataki(api_key="mk_live_...")

try:
    client.organizations.get("org_nonexistent00000000")
except NotFoundError as e:
    print(e.message)       # Human-readable error message
    print(e.status_code)   # 404
    print(e.request_id)    # For support — e.g. "req_abc123"
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(e.status_code)
    print(e.error_type)
```

When the library cannot reach the API (network issues, timeouts), a `ConnectionError` is raised.

### Error types

| Status Code | Error Type             |
| ----------- | ---------------------- |
| 400         | `BadRequestError`      |
| 401         | `AuthenticationError`  |
| 403         | `PermissionDeniedError`|
| 404         | `NotFoundError`        |
| 429         | `RateLimitError`       |
| 500         | `InternalServerError`  |
| N/A         | `ConnectionError`      |

All errors inherit from `MatakiError`.

## API keys

Create and manage API keys programmatically:

```python
from mataki import Mataki

client = Mataki(api_key="mk_live_...")

# Create — the raw key is returned only once
result = client.api_keys.create(
    name="CI Pipeline",
    role="member",
    environment="live",
)
print(result.raw_key)    # mk_live_... (save this immediately)
print(result.api_key)    # ApiKey object (metadata)

# List
for key in client.api_keys.list():
    print(f"{key.name} ({key.role})")

# Delete
client.api_keys.delete("key_7mN3pR9xK2wLvY8cJH4fQ")
```

## Configuration

### Timeouts

The default timeout is 60 seconds. You can override it:

```python
client = Mataki(api_key="mk_live_...", timeout=30.0)
```

On timeout, a `ConnectionError` is raised.

### Base URL

```python
client = Mataki(
    api_key="mk_live_...",
    base_url="https://api.staging.mataki.dev",
)
```

### API versioning

Each SDK release is pinned to a specific [API version](https://docs.mataki.dev/versioning). You can override it, but be aware that the types may not match:

```python
client = Mataki(api_key="mk_live_...", version="2026-02-16")
```

## Types

All responses are [Pydantic](https://docs.pydantic.dev) models with full type annotations. This gives you autocomplete, type checking, and serialization out of the box:

```python
org = client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")

org.id          # str
org.name        # str
org.tags        # list[str]
org.labels      # dict[str, str]
org.annotations # OrganizationAnnotations
```

### Determining the installed version

```python
import mataki
print(mataki.__version__)
```

## Versioning

This package follows [SemVer](https://semver.org/spec/v2.0.0.html). Backwards-incompatible changes are released as major versions.

## Requirements

Python 3.11+.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the [MIT License](LICENSE).
