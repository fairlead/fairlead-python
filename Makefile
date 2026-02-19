.PHONY: fetch-openapi test ruff-check ruff-format mypy pre-commit install-pre-commit

fetch-openapi:
	bash scripts/fetch-openapi.sh

test:
	uv run pytest

ruff-check:
	uv run ruff check --fix .

ruff-format:
	uv run ruff format .

mypy:
	uv run mypy src tests

pre-commit: ruff-format ruff-check mypy test

install-pre-commit:
	uv tool install pre-commit --with pre-commit-uv && uv run pre-commit install
