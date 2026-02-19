#!/usr/bin/env bash
# Fetch the OpenAPI spec from mataki-openapi (the single source of truth).
#
# Local dev: copies from sibling directory ../mataki-openapi/
# CI:        downloads from GitHub at a pinned tag
set -euo pipefail

REPO="mataki-dev/mataki-openapi"
TAG="${OPENAPI_TAG:-latest}"
OUTPUT="openapi.json"
LOCAL_PATH="../mataki-openapi/openapi.json"

if [ "$TAG" = "latest" ] && [ -f "$LOCAL_PATH" ]; then
  echo "Copying from local mataki-openapi..."
  cp "$LOCAL_PATH" "$OUTPUT"
elif command -v gh &>/dev/null; then
  echo "Downloading from GitHub ($REPO @ $TAG)..."
  if [ "$TAG" = "latest" ]; then
    gh release download --repo "$REPO" --pattern openapi.json --output "$OUTPUT" --clobber
  else
    gh release download "$TAG" --repo "$REPO" --pattern openapi.json --output "$OUTPUT" --clobber
  fi
else
  echo "Error: gh CLI not found and no local mataki-openapi directory available."
  exit 1
fi

echo "Wrote $OUTPUT ($(wc -c < "$OUTPUT" | tr -d ' ') bytes)"
