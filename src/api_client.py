import logging
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or os.getenv("BASE_URL", "https://dummyjson.com")) + os.getenv("API_VERSION", "")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", 10))
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        if token:
            self.set_auth_token(token)

    def set_auth_token(self, token):
        self.session.headers["Authorization"] = f"Bearer {token}"

    def clear_auth(self):
        self.session.headers.pop("Authorization", None)

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        start = time.perf_counter()
        logger.info("-> %s %s", method, url)
        response = self.session.request(
            method, url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("<- %s %s  [%.0fms]", response.status_code, response.reason, elapsed_ms)
        response.elapsed_ms = elapsed_ms
        return response
