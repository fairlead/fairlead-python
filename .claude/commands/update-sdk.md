Update the SDK to match the current `openapi.json` in the repo root.

## Instructions

Read `openapi.json` and compare it against the existing SDK implementation. Then apply all necessary changes to bring the SDK in sync with the spec.

### Step 1: Analyze the diff

Read `openapi.json` and catalog every path, operation, schema, and enum. Compare against the current SDK:

- `src/mataki/types/` — Pydantic models for each schema
- `src/mataki/resources/` — Resource classes for each path group
- `src/mataki/_client.py` — Resource properties on Mataki and AsyncMataki
- `src/mataki/__init__.py` — Public re-exports and `__all__`
- `src/mataki/_errors.py` — Error types
- `src/mataki/_config.py` — Default API version

Produce a list of what changed: new resources, removed resources, new fields, removed fields, new endpoints, removed endpoints, changed types, new enums, etc.

### Step 2: Update types

For each schema in `components.schemas`:

- If the schema is **new**, create a new file in `types/` with Pydantic models.
- If the schema **changed**, update the existing model (add/remove/rename fields, change types).
- If the schema was **removed**, delete the file and all references.
- Update `types/__init__.py` to re-export all public types.

Follow existing patterns: `BaseModel` subclasses, `X | Y` union syntax, `StrEnum` for enums. See `types/organization.py` and `types/api_key.py` for reference.

### Step 3: Update resources

For each path group (e.g. `/organizations`, `/api-keys`):

- If the path group is **new**, create a new resource file following the pattern in `resources/organizations.py`: sync class, async class, shared private helpers.
- If endpoints were **added or removed**, add or remove the corresponding methods.
- If request/response shapes changed, update method signatures and body builders.
- Use `typing.List` and `typing.Dict` in resource class method signatures (not lowercase) to avoid the `list` method builtin shadowing issue.
- Do NOT use `from __future__ import annotations` in resource files.

### Step 4: Update the client

In `_client.py`:

- Add/remove resource property type annotations on `Mataki` and `AsyncMataki`.
- Add/remove resource instantiation in `__init__`.
- Import new resource classes.

### Step 5: Update `__init__.py`

- Re-export all new public types and remove deleted ones.
- Keep `__all__` sorted within each section (Clients, Version, Errors, Types).

### Step 6: Update `_config.py`

If the OpenAPI spec's `info.version` or any versioning metadata indicates a new API version date, update `DEFAULT_VERSION`.

### Step 7: Update tests

- Add `<resource>_json()` factories to `tests/conftest.py` for new resources.
- Create `tests/test_<resource>.py` for new resources, following the patterns in `test_organizations.py`: sync CRUD tests + async tests.
- Update existing test factories and tests if schemas changed.
- Remove tests for deleted resources.

### Step 8: Run quality checks

Run all checks and fix any issues:

```
uv run ruff check --fix .
uv run ruff format .
uv run mypy src tests
uv run pytest
```

### Step 9: Update CLAUDE.md

If the project structure section in `CLAUDE.md` is out of date (new files, removed files, new patterns), update it.

### Step 10: Update README.md

Update `README.md` to reflect any changes:

- Add usage examples for new resources.
- Remove examples for deleted resources.
- Update code snippets if method signatures or type names changed.
- If new configuration options were added, document them.
- Keep the existing structure and tone — concise, example-driven, matching Anthropic/Stripe SDK README conventions.

## Rules

- Read CLAUDE.md before starting — it documents all architecture decisions and gotchas.
- Do not change the SDK's design patterns (sync/async duplication, private helpers, pagination approach). Only change what the spec requires.
- Preserve all existing conventions: docstrings on public methods, `__all__` exports, keyword-only args for create/update methods, `entity_id` parameter naming.
- All checks must pass before declaring done.
