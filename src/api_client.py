"""
Base API client — single point of control for all HTTP communication.

Every test goes through this client, which means:
- Auth headers are set once, not in every test file
- Timeouts are consistent
- Response logging is centralised
- Swapping the base URL for staging/prod is a one-liner
"""

import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class APIClient:
    """Thin wrapper around requests.Session with logging and shared config."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or os.getenv("BASE_URL", "https://reqres.in")) + os.getenv("API_VERSION", "/api")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", 10))
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-client": "qa-automation-framework",
        })
        if token:
            self.set_auth_token(token)

    # ── Auth ────────────────────────────────────────────────────────────

    def set_auth_token(self, token: str) -> None:
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_auth(self) -> None:
        self.session.headers.pop("Authorization", None)

    # ── HTTP verbs ───────────────────────────────────────────────────────

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    # ── Core ─────────────────────────────────────────────────────────────

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        start = time.perf_counter()

        logger.info("→ %s %s", method, url)
        if kwargs.get("json"):
            logger.debug("  body: %s", kwargs["json"])

        response = self.session.request(
            method,
            url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "← %s %s  [%.0fms]",
            response.status_code,
            response.reason,
            elapsed_ms,
        )

        # Attach elapsed time so tests can assert on it without re-timing
        response.elapsed_ms = elapsed_ms  # type: ignore[attr-defined]
        return response
