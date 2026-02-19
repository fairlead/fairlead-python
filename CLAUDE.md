# Mataki Python SDK

Official Python client for the Mataki API.

## Package

- **Name**: `mataki` (PyPI: `mataki`)
- **Min Python**: 3.11+ (StrEnum requires 3.11; use `X | Y` unions, not `Optional`)
- **Build**: `pyproject.toml` with hatchling
- **Dependencies**: `httpx` (async + sync), `pydantic` for models
- **Dev deps**: `pytest`, `pytest-asyncio`, `ruff`, `mypy`, `respx` (httpx mocking)

## Project Structure

```text
src/mataki/
  __init__.py          # Re-export Mataki, AsyncMataki, all types and errors
  _client.py           # Sync + async client classes (_BaseClient, Mataki, AsyncMataki)
  _config.py           # ClientConfig (base_url, api_key, timeout, version)
  _errors.py           # MatakiError, APIError, AuthenticationError, NotFoundError, etc.
  _pagination.py       # SyncPage[T], AsyncPage[T] with auto-pagination iterators
  _version.py          # __version__
  types/               # Pydantic models from OpenAPI schemas
    __init__.py
    organization.py
    api_key.py
    shared.py          # Audit, Annotations, OffsetPaginationMeta
  resources/           # Resource-specific API methods
    __init__.py
    organizations.py   # OrganizationsResource, AsyncOrganizationsResource
    api_keys.py        # ApiKeysResource, AsyncApiKeysResource
tests/
  conftest.py          # Fixtures (client, async_client, mock_api) + response factories
  test_organizations.py
  test_api_keys.py
  test_errors.py
  test_pagination.py
```

## Commands

```bash
uv run pytest                # Run tests
uv run ruff check --fix .    # Lint
uv run ruff format .         # Format
uv run mypy src tests        # Type check
make pre-commit              # Run all checks
```

## API Conventions (from OpenAPI spec)

- **Base URL**: `https://api.mataki.dev`
- **Auth**: Bearer token — either a Clerk JWT or a Mataki API key (`mk_live_...` / `mk_test_...`)
- **Versioning**: `Mataki-Version` header, pinned to current API version (`YYYY-MM-DD`) per SDK release
- **List responses**: `{"data": [...], "pagination": {"offset": N, "limit": N, "total_results": N|null}, "meta": {}}`
- **Error envelope**: `{"error": {"type": "...", "message": "...", "code": N, "details": [...], "request_id": "..."}}`
- **ID format**: Prefixed IDs — `org_` for organizations, `key_` for API keys

## SDK Design Patterns

### Client initialization
```python
from mataki import Mataki

client = Mataki(api_key="mk_live_...")

# Async
from mataki import AsyncMataki

client = AsyncMataki(api_key="mk_live_...")

# Context manager (recommended)
with Mataki(api_key="mk_live_...") as client:
    org = client.organizations.get("org_...")

async with AsyncMataki(api_key="mk_live_...") as client:
    org = await client.organizations.get("org_...")
```

### Resource access (Stripe/Anthropic style)
```python
# List
orgs = client.organizations.list(query="name ~* %acme%", sort="name:asc", limit=10)

# Get
org = client.organizations.get("org_4K7fR9pLm2nQwXvY8cJH3")

# Create
org = client.organizations.create(name="Acme Corp", tags=["production"])

# Update
org = client.organizations.update("org_4K7fR9pLm2nQwXvY8cJH3", name="Acme Inc")

# Delete
client.organizations.delete("org_4K7fR9pLm2nQwXvY8cJH3")
```

### Error handling
```python
from mataki import APIError, AuthenticationError, NotFoundError

try:
    org = client.organizations.get("org_nonexistent")
except NotFoundError as e:
    print(e.message)       # Human-readable
    print(e.status_code)   # 404
    print(e.request_id)    # For support
except APIError as e:
    print(e.error_type)    # "not_found_error", "invalid_request_error", etc.
```

### Pagination
```python
# Auto-pagination iterator
for org in client.organizations.list():
    print(org.name)

# Async auto-pagination
async for org in await async_client.organizations.list():
    print(org.name)

# Manual single-page access
page = client.organizations.list(limit=10, offset=0)
print(page.data)          # list[Organization]
print(page.pagination)    # OffsetPaginationMeta
```

### Error hierarchy
```
MatakiError (base)
├── APIError (any HTTP error from the API)
│   ├── BadRequestError (400)
│   ├── AuthenticationError (401)
│   ├── PermissionDeniedError (403)
│   ├── NotFoundError (404)
│   ├── RateLimitError (429)
│   └── InternalServerError (500)
└── ConnectionError (network-level, including timeouts)
```

## Architecture Notes

### `list` method and builtin shadowing

Resource classes have a method named `list` which shadows Python's builtin `list`
type. This causes mypy `valid-type` errors when later methods in the same class use
`list[str]` in annotations. **Use `typing.List` and `typing.Dict` in resource class
method signatures** — this is the same workaround used by the Anthropic and Stripe
Python SDKs. The private helper functions (outside the class) can use lowercase
`list`/`dict` since there is no shadowing there. Ruff UP006/UP035 are suppressed
via per-file-ignores in `pyproject.toml` for `src/mataki/resources/*.py`.

Do NOT use `from __future__ import annotations` in resource files — it makes the
problem worse by deferring all annotation evaluation, causing mypy to resolve `list`
to the class method in all cases.

### `ConnectionError` builtin shadowing

`_errors.py` defines `ConnectionError` which shadows Python's builtin. This requires
`# noqa: A001` on the class definition. In `_client.py`, import it aliased:
`from mataki._errors import ConnectionError as MatakiConnectionError`.

### `from __future__ import annotations` policy

- **DO use** in `_client.py`, `_errors.py`, `_pagination.py`, and test files —
  needed for `TYPE_CHECKING`-guarded forward references and cleaner annotations
- **Do NOT use** in resource files (`resources/*.py`) — it breaks the `list`
  builtin shadowing workaround (see above)

### `TYPE_CHECKING` guards for client types

Resource files and `_pagination.py` reference `Mataki` / `AsyncMataki` in type
annotations but don't need them at runtime. These imports are guarded behind
`if TYPE_CHECKING:` to keep the dependency one-directional (`_client.py` →
resources, never the reverse). In `_pagination.py` and `_client.py`,
`from __future__ import annotations` defers annotation evaluation so the guarded
names resolve. Resource files omit the future import (see `list` shadowing above)
— the guarded types still work in `__init__` signatures without it.

### Sync/async duplication

Each resource has a sync class and an async class with identical method signatures.
Private helper functions (`_list_params`, `_create_body`, etc.) are shared at module
level to eliminate logic duplication. Method bodies are 2-3 lines each.

### Client `__init__` forwarding

`Mataki.__init__` and `AsyncMataki.__init__` use `**kwargs: Any` to forward all
parameters to `_BaseClient.__init__`, avoiding duplicating the parameter list
(api_key, base_url, timeout, version, max_retries) in three places.

### Pagination internals

`SyncPage[T]` and `AsyncPage[T]` are plain generic classes (not Pydantic models)
because they carry non-serializable state (`_client`, `_path`, `_params`, `_model`)
needed for auto-pagination. `_pagination.py` uses `from __future__ import annotations`
for forward-reference resolution of `TYPE_CHECKING`-guarded client types.

Auto-pagination stops when either: (a) a page has fewer items than the limit, or
(b) `offset + limit >= total_results` (when total_results is provided).

### Test imports

Test files import conftest helpers as `from conftest import ...` (not
`from tests.conftest import ...`) because `tests/` is not a package on `sys.path`.
pytest makes conftest importable within the test directory automatically.

### Test factories

`conftest.py` provides factory functions for building mock responses:

- `org_json(**overrides)` / `api_key_json(**overrides)` — single entity dicts
- `list_response(data, offset, limit, total_results)` — paginated list envelope
- `error_response(type, message, code, request_id)` — error envelope

All accept `**overrides` for field customization. Use `respx.mock(base_url=...)`.

## Adding a New Resource

1. Add Pydantic models in `types/<resource>.py`, re-export from `types/__init__.py`
2. Create `resources/<resource>.py` with sync + async classes and private helpers.
   Use `typing.List`/`typing.Dict` in class method signatures (not lowercase)
3. Register on both client classes in `_client.py` (type annotation + `__init__`)
4. Re-export new types from `__init__.py` and add to `__all__`
5. Add `<resource>_json()` factory to `tests/conftest.py`
6. Write tests in `tests/test_<resource>.py`

## Style

- Python 3.11+ — use `X | Y` unions, `StrEnum`, not `Optional`
- All public methods return typed Pydantic models
- Both sync (`Mataki`) and async (`AsyncMataki`) clients with context manager support
- httpx for HTTP — supports connection pooling, retries, timeouts
- respx for test mocking (not requests-mock)
- Follow Anthropic SDK patterns for naming and structure
- Docstrings on all public methods with parameter descriptions
- `__all__` exports in every `__init__.py`
- Line length: 120
- ruff for linting/formatting, mypy strict mode for type checking

## API Version Pinning

The SDK pins `DEFAULT_VERSION` in `_config.py` to a specific API version date (e.g.
`"2026-02-16"`). This is sent as the `Mataki-Version` header on every request, ensuring
deterministic API behavior for SDK users regardless of server-side changes.

**Never use `"latest"` as the default.** Each SDK release must target a known API
version. When the API introduces a new version, update `DEFAULT_VERSION` to the new
date and adjust types/resources to match.

## Reference

- OpenAPI spec: `openapi.json` in repo root
- The spec is the source of truth for all types, endpoints, and error shapes
