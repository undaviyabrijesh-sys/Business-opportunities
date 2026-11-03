"""IMD client using documented API endpoints. No API key is hard-coded."""
from __future__ import annotations
import os
from typing import Any
import requests


class IMDClient:
    def __init__(self, base_url: str | None = None, session: requests.Session | None = None):
        self.base_url = (base_url or os.getenv("IMD_BASE_URL", "https://api.imd.gov.in/api/v1")).rstrip("/")
        self.session = session or requests.Session()
        self.timeout = float(os.getenv("HTTP_TIMEOUT_SECONDS", "20"))
        self.session.headers.setdefault("User-Agent", "BusinessOpportunitiesResearch/0.1")

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        response = self.session.get(f"{self.base_url}/{endpoint.lstrip('/')}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def city_forecast(self, station_id: str) -> Any:
        return self._get("cityforecast", {"id": station_id})

    def city_forecast_location(self, station_id: str) -> Any:
        return self._get("cityforecastloc", {"id": station_id})

    def current_weather(self, station_id: str | None = None) -> Any:
        return self._get("current_wx", {"id": station_id} if station_id else None)

    def district_warnings(self, district_id: str | None = None) -> Any:
        return self._get("districtwarning", {"id": district_id} if district_id else None)

    def district_nowcast(self, district_id: str | None = None) -> Any:
        return self._get("districtnowcast", {"id": district_id} if district_id else None)

    def agromet_advisory(self, district_id: str | None = None) -> Any:
        return self._get("agrometadvisory", {"id": district_id} if district_id else None)
