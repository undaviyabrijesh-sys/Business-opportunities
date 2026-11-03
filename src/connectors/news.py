"""RSS-based news ingestion for official sources and product keyword search."""
from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
import re

import feedparser
import requests

PIB_RSS = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1"


def _date(entry) -> str | None:
    raw = entry.get("published") or entry.get("updated")
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return raw


def fetch_rss(url: str, timeout: int = 20) -> list[dict]:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "BusinessOpportunitiesResearch/0.1"})
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    rows = []
    for item in feed.entries:
        rows.append({
            "title": item.get("title", ""),
            "summary": re.sub(r"<[^>]+>", " ", item.get("summary", "") or "").strip(),
            "url": item.get("link", ""),
            "published_at": _date(item),
            "source": feed.feed.get("title", url),
        })
    return rows


def search_product_news(item: str) -> list[dict]:
    """Search Google News RSS for a product; returns linked headlines, not verified demand."""
    from urllib.parse import quote_plus
    query = quote_plus(f'"{item}" (market OR demand OR export OR import OR price OR supply)')
    return fetch_rss(f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en")


def filter_keyword(rows: Iterable[dict], item: str) -> list[dict]:
    terms = [t.lower() for t in re.findall(r"[A-Za-z0-9]+", item) if len(t) > 2]
    return [r for r in rows if any(t in (r.get("title", "") + " " + r.get("summary", "")).lower() for t in terms)]
