"""UN Comtrade client for HS trade exploration."""
from __future__ import annotations
import os
import requests


class ComtradeClient:
    BASE_URL = "https://comtradeapi.un.org"

    def __init__(self, api_key: str | None = None, session: requests.Session | None = None):
        self.api_key = api_key or os.getenv("COMTRADE_API_KEY")
        self.session = session or requests.Session()
        self.timeout = float(os.getenv("HTTP_TIMEOUT_SECONDS", "25"))

    def query(self, *, reporter_code: str, partner_code: str, cmd_code: str,
              period: str, flow_code: str = "M") -> dict:
        base_params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "cmdCode": cmd_code,
            "flowCode": flow_code,
            "motCode": "0",
            "partner2Code": "0",
            "maxRecords": "500",
            "breakdownMode": "classic",
        }
        if self.api_key:
            url = f"{self.BASE_URL}/data/v1/get/C/A/HS"
            base_params["subscription-key"] = self.api_key
            requested_periods = [period]
        else:
            # UN Comtrade public preview accepts only one annual period per call.
            url = f"{self.BASE_URL}/public/v1/preview/C/A/HS"
            requested_periods = [p.strip() for p in str(period).split(",") if p.strip()]

        combined = []
        messages = []
        for requested_period in requested_periods:
            params = {**base_params, "period": requested_period}
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
            combined.extend(payload.get("data") or [])
            if payload.get("messages"):
                messages.extend(payload["messages"] if isinstance(payload["messages"], list) else [payload["messages"]])
        return {"data": combined, "messages": messages, "count": len(combined)}
