"""Client for OGD Platform India resource APIs."""
from __future__ import annotations
import os
import requests


class OGDClient:
    BASE_URL = "https://api.data.gov.in/resource"

    def __init__(self, api_key: str | None = None, session: requests.Session | None = None):
        self.api_key = api_key or os.getenv("OGD_API_KEY")
        self.session = session or requests.Session()
        self.timeout = float(os.getenv("HTTP_TIMEOUT_SECONDS", "20"))

    def records(self, resource_id: str, *, limit: int = 100, offset: int = 0,
                filters: dict[str, str] | None = None) -> dict:
        if not self.api_key:
            raise RuntimeError("Set OGD_API_KEY from your data.gov.in account before using OGD resource API.")
        params = {"api-key": self.api_key, "format": "json", "limit": limit, "offset": offset}
        for field, value in (filters or {}).items():
            params[f"filters[{field}]"] = value
        response = self.session.get(f"{self.BASE_URL}/{resource_id}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
