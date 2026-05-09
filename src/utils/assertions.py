"""
Custom assertion helpers.

Wrapping assertions in named functions does two things:
1. Failure messages are human-readable without extra pytest output config
2. Assertions can be reused across test files without copy-pasting
"""

import os
import jsonschema
import requests


MAX_RESPONSE_TIME_MS = int(os.getenv("MAX_RESPONSE_TIME_MS", 2000))


# ── Status code assertions ────────────────────────────────────────────────

def assert_status(response: requests.Response, expected: int) -> None:
    """Assert HTTP status code with a descriptive failure message."""
    actual = response.status_code
    assert actual == expected, (
        f"Expected status {expected}, got {actual}.\n"
        f"URL: {response.url}\n"
        f"Body: {response.text[:500]}"
    )


def assert_ok(response: requests.Response) -> None:
    assert_status(response, 200)


def assert_created(response: requests.Response) -> None:
    assert_status(response, 201)


def assert_no_content(response: requests.Response) -> None:
    assert_status(response, 204)


def assert_not_found(response: requests.Response) -> None:
    assert_status(response, 404)


def assert_bad_request(response: requests.Response) -> None:
    assert_status(response, 400)


def assert_unauthorized(response: requests.Response) -> None:
    assert_status(response, 401)


# ── Schema validation ─────────────────────────────────────────────────────

def assert_schema(data: dict, schema: dict) -> None:
    """Validate response body against a JSON Schema definition."""
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(
            f"Schema validation failed:\n"
            f"  Path:    {' → '.join(str(p) for p in e.absolute_path)}\n"
            f"  Message: {e.message}"
        ) from e


# ── Performance assertions ────────────────────────────────────────────────

def assert_response_time(response: requests.Response, max_ms: int = MAX_RESPONSE_TIME_MS) -> None:
    """Assert that the response arrived within the allowed time budget."""
    elapsed = getattr(response, "elapsed_ms", response.elapsed.total_seconds() * 1000)
    assert elapsed <= max_ms, (
        f"Response too slow: {elapsed:.0f}ms > {max_ms}ms threshold\n"
        f"URL: {response.url}"
    )


# ── Content assertions ────────────────────────────────────────────────────

def assert_json_key(data: dict, key: str, expected_value=None) -> None:
    assert key in data, f"Key '{key}' not found in response. Keys present: {list(data.keys())}"
    if expected_value is not None:
        assert data[key] == expected_value, (
            f"Key '{key}': expected {expected_value!r}, got {data[key]!r}"
        )


def assert_list_not_empty(data: list, field: str = "data") -> None:
    assert isinstance(data, list) and len(data) > 0, (
        f"Expected a non-empty list for '{field}', got: {data!r}"
    )


def assert_pagination(body: dict) -> None:
    """Assert that the response contains standard pagination fields."""
    for field in ("page", "per_page", "total", "total_pages"):
        assert field in body, f"Pagination field '{field}' missing from response"
    assert body["total_pages"] >= 1
    assert body["per_page"] >= 1
