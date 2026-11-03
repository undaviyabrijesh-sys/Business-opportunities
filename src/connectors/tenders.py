"""Tender discovery links and keyword scoring.

CPPP's public advanced search includes CAPTCHA. This module therefore provides
a compliant hand-off to the official search page and a local relevance filter
for records imported by a supported export/feed. It does not bypass CAPTCHA.
"""
from __future__ import annotations

from datetime import date


CPPP_HOME = "https://eprocure.gov.in/eprocure/app"
CPPP_ADVANCED_SEARCH = "https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page"
GEM_BIDS = "https://bidplus.gem.gov.in/all-bids"


def keyword_relevance(title: str, description: str, item: str) -> int:
    text = f"{title} {description}".casefold()
    terms = [t.casefold() for t in item.split() if len(t) > 2]
    if not terms:
        return 0
    matched = sum(1 for term in terms if term in text)
    return round(100 * matched / len(set(terms)))


def tender_status(closing_date: date | None, today: date | None = None) -> str:
    if closing_date is None:
        return "date_unverified"
    today = today or date.today()
    return "open" if closing_date >= today else "closed_or_expired"
