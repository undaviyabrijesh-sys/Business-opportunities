"""Item normalization and cross-sector catalogue search.

HS codes in the starter catalogue are candidate headings/codes only. Product
form, composition, grade, processing and destination rules can change the
correct classification; users must confirm before trade analysis.
"""
from __future__ import annotations

import json
import re
from difflib import get_close_matches
from pathlib import Path
from typing import Any

PRODUCTS_PATH = Path(__file__).parent.parent / "config" / "products.json"


def normalize_text(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def load_products() -> list[dict[str, Any]]:
    return json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))


def _search_terms(record: dict[str, Any]) -> list[str]:
    return [record["name"], record.get("product_id", ""), record.get("category", ""), *record.get("aliases", [])]


def suggest_products(query: str, limit: int = 8) -> list[dict]:
    """Find products by exact/partial alias, category or fuzzy text match."""
    q = normalize_text(query)
    if not q:
        return []
    records = load_products()
    ranked: list[tuple[int, dict]] = []
    for record in records:
        terms = [(term, normalize_text(term)) for term in _search_terms(record) if term]
        score = 0
        reason = ""
        if any(q == norm for _, norm in terms):
            score, reason = 100, "exact_match"
        elif any(q in norm for _, norm in terms):
            score, reason = 90, "partial_match"
        elif any(norm in q for _, norm in terms if len(norm) >= 4):
            score, reason = 82, "query_contains_product_term"
        else:
            candidates = [norm for _, norm in terms]
            best = max((__import__("difflib").SequenceMatcher(None, q, term).ratio() for term in candidates), default=0)
            if best >= 0.55:
                score, reason = round(best * 75), "fuzzy_match"
        if score:
            item = dict(record)
            item["status"] = item.get("hs_status", "mapping_not_reviewed")
            item["match_score"] = score
            item["match_reason"] = reason
            ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["name"]))
    return [item for _, item in ranked[:max(1, limit)]]


def item_dossier_plan(query: str) -> dict:
    suggestions = suggest_products(query)
    return {
        "query": query,
        "suggestions": suggestions,
        "hs_code_status": "confirm_mapping_before_trade_analysis",
        "sections": [
            "India supply", "India imports/exports", "global demand",
            "price benchmarks", "weather", "news", "buyers/sellers",
            "tenders", "compliance", "unit economics",
        ],
        "catalogue_match_status": "matched" if suggestions else "new_item",
    }
