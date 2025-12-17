
"""Lightweight client for the BrowserStack Demo public APIs."""

from __future__ import annotations

from typing import Optional

import requests

from utils.logger import get_logger


logger = get_logger(__name__)


class StoreClient:
    """HTTP helper that wraps the BrowserStack demo catalog and sign-in APIs."""

    def __init__(self, base_url: str, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip('/')
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, timeout=15, **kwargs)
        logger.info("%s %s -> %s", method, url, response.status_code)
        return response

    def list_products(self) -> requests.Response:
        """GET /products."""
        return self._request("GET", "/products")

    def sign_in(self, username: str, password: str) -> requests.Response:
        """POST /signin with username/password payload."""
        payload = {"userName": username, "password": password}
        return self._request("POST", "/signin", json=payload)
