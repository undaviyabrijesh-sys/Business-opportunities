"""UN Comtrade monthly/annual merchandise-trade client."""
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
              period: str, flow_code: str = "M", aggregate: str = "6") -> dict:
        """Query one reporter/partner/HS code/period.

        flow_code M=imports, X=exports. Use HS code appropriate to the
        requested classification and period; validate reporter/partner codes.
        """
        params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "cmdCode": cmd_code,
            "period": period,
            "flowCode": flow_code,
            "aggregateBy": aggregate,
            "breakdownMode": "classic",
            "motCode": "0",
            "partner2Code": "0",
            "maxRecords": "500",
        }
        if self.api_key:
            params["subscription-key"] = self.api_key
            url = f"{self.BASE_URL}/data/v1/get/C/A/HS"
        else:
            # Preview endpoint has stricter limits; use for lightweight exploratory requests only.
            url = f"{self.BASE_URL}/public/v1/preview/C/A/HS"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
