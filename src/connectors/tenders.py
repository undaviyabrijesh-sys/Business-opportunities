"""Tender portal hand-offs and keyword relevance helpers.

CPPP advanced search uses CAPTCHA. This connector does not bypass it.
"""
from datetime import date

CPPP_HOME = "https://eprocure.gov.in/eprocure/app"
CPPP_ADVANCED_SEARCH = "https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page"
GEM_BIDS = "https://bidplus.gem.gov.in/all-bids"


def keyword_relevance(title: str, description: str, item: str) -> int:
    text = f"{title} {description}".casefold()
    terms = {term.casefold() for term in item.split() if len(term) > 2}
    return round(100 * sum(term in text for term in terms) / len(terms)) if terms else 0


def tender_status(closing_date: date | None, today: date | None = None) -> str:
    if closing_date is None:
        return "date_unverified"
    return "open" if closing_date >= (today or date.today()) else "closed_or_expired"
