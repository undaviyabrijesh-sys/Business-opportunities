"""Item normalization and starter catalogue search."""
from __future__ import annotations
import json
from pathlib import Path
from difflib import get_close_matches

PRODUCTS_PATH = Path(__file__).parent.parent / "config" / "products.json"


def suggest_products(query: str, limit: int = 5) -> list[dict]:
    records = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    names = {record["name"].casefold(): record for record in records}
    q = query.casefold().strip()
    exact = [record for name, record in names.items() if q == name or q in name]
    if exact:
        return exact[:limit]
    matches = get_close_matches(q, list(names), n=limit, cutoff=0.35)
    return [names[name] for name in matches]


def item_dossier_plan(query: str) -> dict:
    return {
        "query": query,
        "suggestions": suggest_products(query),
        "hs_code_status": "confirm_mapping_before_trade_analysis",
        "sections": ["India supply", "India imports/exports", "global demand", "price benchmarks",
                     "weather", "news", "buyers/sellers", "tenders", "compliance", "unit economics"],
    }
