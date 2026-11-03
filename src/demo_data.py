"""Clearly illustrative records for the first UI iteration.

These numbers are synthetic and must never be presented as live quotes or forecasts.
Replace with validated source adapters before commercial decision-making.
"""
from datetime import date, timedelta
import numpy as np
import pandas as pd


def sample_market_prices(product: str) -> pd.DataFrame:
    rng = np.random.default_rng(17)
    markets = ["Ahmedabad", "Rajkot", "Indore", "Delhi", "Mumbai", "Jaipur"]
    base = {"Rice": 2800, "Turmeric": 9200, "Cotton": 6800}.get(product, 500)
    rows = []
    for day in range(60):
        d = date.today() - timedelta(days=59-day)
        for i, market in enumerate(markets):
            price = base * (1 + 0.025 * np.sin(day / 8 + i) + rng.normal(0, 0.012))
            rows.append({
                "date": d, "market": market, "product": product,
                "modal_price_inr_per_quintal": round(price, 0),
                "arrivals_tonnes": round(float(rng.uniform(20, 240)), 1),
                "data_status": "ILLUSTRATIVE — NOT LIVE DATA",
            })
    return pd.DataFrame(rows)


def sample_trade_data(product: str) -> pd.DataFrame:
    destinations = ["UAE", "USA", "Bangladesh", "Netherlands", "Saudi Arabia"]
    volumes = [82, 64, 55, 49, 42]
    return pd.DataFrame({
        "destination": destinations,
        "relative_trade_index": volumes,
        "product": product,
        "data_status": "ILLUSTRATIVE — NOT LIVE DATA",
    })


def sample_opportunities() -> pd.DataFrame:
    return pd.DataFrame([
        {"product":"Rice","type":"Domestic sourcing spread","market_pair":"Indore → Ahmedabad","score":78,"confidence":"Low (sample)","thesis":"Illustrative price dispersion to validate with live grade-matched mandi prices."},
        {"product":"Turmeric","type":"Export market screening","market_pair":"India → UAE","score":72,"confidence":"Low (sample)","thesis":"Illustrative destination screening; confirm import growth, quality specs and buyer demand."},
        {"product":"Cotton","type":"Industrial demand screening","market_pair":"Gujarat → Bangladesh","score":66,"confidence":"Low (sample)","thesis":"Illustrative trade hypothesis; validate HS-level import demand, yarn/fibre specs and freight."},
    ])
