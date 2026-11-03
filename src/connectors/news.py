"""RSS discovery for official announcements and item-related news."""
from __future__ import annotations
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
import re
import feedparser
import requests

PIB_RSS = "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=1"


def fetch_rss(url: str, timeout: int = 20) -> list[dict]:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "BusinessOpportunitiesResearch/0.1"})
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    rows = []
    for entry in feed.entries:
        published = entry.get("published") or entry.get("updated")
        try:
            published = parsedate_to_datetime(published).isoformat() if published else None
        except (ValueError, TypeError):
            pass
        summary = re.sub(r"<[^>]+>", " ", entry.get("summary", "") or "").strip()
        rows.append({"title": entry.get("title", ""), "summary": summary,
                     "url": entry.get("link", ""), "published_at": published,
                     "source": feed.feed.get("title", url)})
    return rows


def search_product_news(item: str) -> list[dict]:
    query = quote_plus(f'"{item}" (market OR demand OR export OR import OR price OR supply)')
    return fetch_rss(f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en")


def search_official_news(item: str) -> list[dict]:
    terms = [term for term in item.split() if len(term) > 2]
    rows = fetch_rss(PIB_RSS)
    lowered = " ".join(terms).casefold()
    return [row for row in rows if lowered in (row["title"] + " " + row["summary"]).casefold()]



def search_market_research(item: str) -> list[dict]:
    """Search publicly indexed CBI/ITC/Global Trade Helpdesk research for an item.

    Results are returned as discovery links from Google News RSS. This is not
    a direct CBI/ITC API and does not imply every result is an official study.
    """
    clean_item = " ".join(str(item).split())
    if not clean_item:
        return []
    terms = (
        f'"{clean_item}" (market OR demand OR import OR export OR regulation OR buyer) '
        '(site:cbi.eu/market-information OR site:intracen.org OR site:globaltradehelpdesk.org)'
    )
    query = quote_plus(terms)
    return fetch_rss(
        f"https://news.google.com/rss/search?q={query}&hl=en&gl=GB&ceid=GB:en"
    )
