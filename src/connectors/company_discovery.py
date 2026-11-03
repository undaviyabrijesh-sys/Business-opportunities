"""Public web discovery for potential product buyers and sellers."""
from __future__ import annotations
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urlparse, urljoin
from datetime import datetime, timezone
import re
import requests

SEARCH_URL = "https://html.duckduckgo.com/html/"
HEADERS = {"User-Agent": "BusinessOpportunityResearch/1.0"}
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s()./-]{7,}\d)(?!\w)")


class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.current, self.capture, self.buffer, self.depth = [], None, None, [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "div" and "result" in classes and self.current is None:
            self.current = {"title": "", "url": "", "snippet": ""}
            self.depth = 1
        elif self.current is not None and tag == "div":
            self.depth += 1
        elif self.current is not None and tag == "a" and "result__a" in classes:
            self.capture = "title"
            self.current["url"] = unwrap_url(attrs.get("href", ""))
            self.buffer = []
        elif self.current is not None and "result__snippet" in classes:
            self.capture, self.buffer = "snippet", []

    def handle_data(self, data):
        if self.current is not None and self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if self.current is None:
            return
        if self.capture == "title" and tag == "a":
            self.current["title"] = " ".join("".join(self.buffer).split())
            self.capture = None
        elif self.capture == "snippet" and tag in {"a", "div"}:
            self.current["snippet"] = " ".join("".join(self.buffer).split())
            self.capture = None
        if tag == "div":
            self.depth -= 1
            if self.depth <= 0:
                if self.current.get("url"):
                    self.rows.append(self.current)
                self.current = None
                self.capture = None
                self.depth = 0


def unwrap_url(raw):
    raw = urljoin("https://duckduckgo.com/", raw or "")
    parsed = urlparse(raw)
    is_ddg = parsed.netloc == "duckduckgo.com" or parsed.netloc.endswith(".duckduckgo.com")
    if is_ddg and parsed.path.startswith("/l/"):
        target = unquote(parse_qs(parsed.query).get("uddg", [""])[0])
        return target if urlparse(target).scheme in {"http", "https"} else ""
    return raw if parsed.scheme in {"http", "https"} else ""


def _search(query, session, limit):
    response = session.get(SEARCH_URL, params={"q": query, "kl": "in-en"},
                           headers=HEADERS, timeout=15)
    response.raise_for_status()
    parser = ResultParser()
    parser.feed(response.text)
    seen, rows = set(), []
    for row in parser.rows:
        if row["url"] and row["url"] not in seen and row["title"]:
            seen.add(row["url"])
            row["domain"] = urlparse(row["url"]).netloc.lower().removeprefix("www.")
            rows.append(row)
        if len(rows) >= limit:
            break
    return rows


def _contacts(url, session):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return [], [], ""
    pages = [url, f"{parsed.scheme}://{parsed.netloc}/contact",
             f"{parsed.scheme}://{parsed.netloc}/contact-us"]
    emails, phones, contact_page = set(), set(), ""
    for page_url in pages:
        try:
            response = session.get(page_url, headers=HEADERS, timeout=12)
            if response.status_code >= 400 or urlparse(response.url).netloc.lower() != parsed.netloc.lower():
                continue
            body = response.text[:800000]
            emails.update(EMAIL_RE.findall(body))
            phones.update(PHONE_RE.findall(body))
            if "contact" in response.url.lower() and not contact_page:
                contact_page = response.url
        except requests.RequestException:
            continue
    return sorted(emails)[:5], sorted({" ".join(x.split()) for x in phones if len(re.sub(r"\D", "", x)) >= 8})[:5], contact_page


def search_company_leads(product, market="India + Global", max_per_side=8,
                         session=None, enrich_contacts=True):
    """Return separate buyer and seller prospect lists with source links."""
    product = " ".join(str(product).split())
    if not product:
        return {"query": "", "buyers": [], "sellers": [], "errors": []}
    session = session or requests.Session()
    region = "India" if market == "India only" else "India and international"
    queries = {
        "buyers": [f'"{product}" importer buyer company {region}',
                   f'site:volza.com "{product}" importers buyers'],
        "sellers": [f'"{product}" manufacturer supplier exporter {region}',
                    f'site:indiamart.com OR site:tradeindia.com "{product}" supplier manufacturer'],
    }
    result = {"query": product, "market": market, "buyers": [], "sellers": [],
              "errors": [], "searched_at": datetime.now(timezone.utc).isoformat(),
              "search_provider": "DuckDuckGo public web search"}
    for kind, terms in queries.items():
        rows, seen = [], set()
        for term in terms:
            try:
                for row in _search(term, session, max_per_side):
                    if row["url"] not in seen:
                        seen.add(row["url"])
                        rows.append(row)
            except requests.RequestException as exc:
                result["errors"].append(f"{kind.title()} search: {exc}")
        for index, row in enumerate(rows[:max_per_side]):
            row.update({"emails": [], "phones": [], "contact_url": "",
                        "contact_status": "Not checked",
                        "verification": "Unverified prospect. Confirm current activity and product fit directly.",
                        "source": "DuckDuckGo public web search"})
            if enrich_contacts and index < 3:
                emails, phones, contact_url = _contacts(row["url"], session)
                row.update({"emails": emails, "phones": phones, "contact_url": contact_url,
                            "contact_status": "Public details found" if emails or phones else
                            "Contact page found" if contact_url else "No public contact details extracted"})
        result[kind] = rows[:max_per_side]
    return result
