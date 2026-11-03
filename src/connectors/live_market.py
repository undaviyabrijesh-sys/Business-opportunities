"""Live market-data adapters with normalized records and provenance.

AGMARKNET access uses the published data.gov.in resource API. UN Comtrade
returns reporter/partner/HS trade records. These adapters do not synthesize
missing observations or silently repair ambiguous HS classifications.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.connectors.ogd import OGDClient
from src.connectors.comtrade import ComtradeClient

AGMARKNET_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
AGMARKNET_SOURCE = "data.gov.in / AGMARKNET"
COMTRADE_SOURCE = "UN Comtrade"


def _pick(record: dict[str, Any], *names: str) -> Any:
    lookup = {str(key).casefold().replace(" ", "").replace("_", ""): value for key, value in record.items()}
    for name in names:
        key = name.casefold().replace(" ", "").replace("_", "")
        if key in lookup:
            return lookup[key]
    return None


def normalize_agmarknet(payload: dict[str, Any], item: str, retrieved_at: str | None = None) -> list[dict]:
    """Filter and normalize AGMARKNET records for the requested commodity."""
    retrieved = retrieved_at or datetime.now(timezone.utc).isoformat()
    records = payload.get("records") or []
    query = " ".join(item.casefold().split())
    rows = []
    for raw in records:
        commodity = _pick(raw, "commodity", "Commodity")
        if not commodity or query not in " ".join(str(commodity).casefold().split()):
            continue
        rows.append({
            "date": _pick(raw, "arrival_date", "Arrival_Date", "Arrival Date"),
            "state": _pick(raw, "state", "State"),
            "district": _pick(raw, "district", "District"),
            "market": _pick(raw, "market", "Market"),
            "commodity": commodity,
            "variety": _pick(raw, "variety", "Variety"),
            "grade": _pick(raw, "grade", "Grade"),
            "min_price": _pick(raw, "min_price", "Min Price"),
            "max_price": _pick(raw, "max_price", "Max Price"),
            "modal_price": _pick(raw, "modal_price", "Modal Price"),
            "price_unit": "INR per quintal (source convention; verify dataset metadata)",
            "source": AGMARKNET_SOURCE,
            "source_record_id": _pick(raw, "id", "record_id"),
            "retrieved_at": retrieved,
            "data_status": "LIVE_SOURCE_RECORD",
        })
    return rows


def fetch_agmarknet_prices(item: str, api_key: str, limit: int = 1000) -> dict:
    """Fetch recent mandi observations; callers should display no-match as such."""
    if not api_key:
        raise RuntimeError("OGD_API_KEY is required. Add it to Streamlit secrets or the app environment.")
    payload = OGDClient(api_key=api_key).records(
        AGMARKNET_RESOURCE_ID,
        limit=max(1, min(int(limit), 100)),
        offset=0,
        filters={"commodity": item},
    )
    rows = normalize_agmarknet(payload, item)
    return {
        "records": rows,
        "source": AGMARKNET_SOURCE,
        "resource_id": AGMARKNET_RESOURCE_ID,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "total_records_returned": len(payload.get("records") or []),
        "matched_records": len(rows),
        "source_status": "live_records" if rows else "live_query_no_item_match",
    }


def normalize_comtrade(payload: dict[str, Any], retrieved_at: str | None = None) -> list[dict]:
    """Normalize UN Comtrade response while preserving units and source dimensions."""
    retrieved = retrieved_at or datetime.now(timezone.utc).isoformat()
    rows = []
    for raw in payload.get("data") or []:
        rows.append({
            "period": _pick(raw, "period"),
            "reporter": _pick(raw, "reporterDesc", "reporterCode"),
            "partner": _pick(raw, "partnerDesc", "partnerCode"),
            "flow": _pick(raw, "flowDesc", "flowCode"),
            "hs_code": _pick(raw, "cmdCode"),
            "product": _pick(raw, "cmdDesc"),
            "trade_value_usd": _pick(raw, "primaryValue", "TradeValue"),
            "net_weight_kg": _pick(raw, "netWgt", "NetWgt"),
            "quantity": _pick(raw, "qty", "quantity"),
            "quantity_unit": _pick(raw, "qtyUnitAbbr", "qtyUnit"),
            "source": COMTRADE_SOURCE,
            "retrieved_at": retrieved,
            "data_status": "LIVE_SOURCE_RECORD",
        })
    return rows


def fetch_india_trade(hs_code: str, periods: str, flow_code: str = "X", api_key: str | None = None) -> dict:
    """Fetch India-reported world trade for a verified/confirmed HS code."""
    if not hs_code or not hs_code.isdigit():
        raise ValueError("A numeric HS code is required.")
    if flow_code not in {"X", "M"}:
        raise ValueError("flow_code must be X (exports) or M (imports).")
    payload = ComtradeClient(api_key=api_key).query(
        reporter_code="699",
        partner_code="0",
        cmd_code=hs_code,
        period=periods,
        flow_code=flow_code,
    )
    rows = normalize_comtrade(payload)
    return {
        "records": rows,
        "source": COMTRADE_SOURCE,
        "reporter": "India",
        "partner": "World",
        "flow": "Exports" if flow_code == "X" else "Imports",
        "hs_code": hs_code,
        "periods": periods,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "matched_records": len(rows),
        "source_status": "live_records" if rows else "live_query_no_records",
        "api_message": payload.get("messages"),
    }


def fetch_global_import_markets(hs_code: str, periods: str, api_key: str | None = None) -> dict:
    """Fetch product imports reported by all countries from UN Comtrade.

    The public preview is limited to 500 records per annual period. The
    caller must confirm the candidate HS code before requesting this data.
    """
    if not hs_code or not hs_code.isdigit():
        raise ValueError("A numeric HS code is required.")
    payload = ComtradeClient(api_key=api_key).query(
        reporter_code="ALL",
        partner_code="0",
        cmd_code=hs_code,
        period=periods,
        flow_code="M",
    )
    rows = normalize_comtrade(payload)
    return {
        "records": rows,
        "source": COMTRADE_SOURCE,
        "reporter": "All reporting countries",
        "partner": "World",
        "flow": "Imports",
        "hs_code": hs_code,
        "periods": periods,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "matched_records": len(rows),
        "source_status": "live_records" if rows else "live_query_no_records",
        "api_message": payload.get("messages"),
        "preview_limit": 500 if not api_key else None,
    }
