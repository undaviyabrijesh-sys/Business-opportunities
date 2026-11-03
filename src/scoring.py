"""Transparent opportunity scoring; component scores are 0-100."""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class OpportunitySignals:
    demand_momentum: Optional[float] = None
    supply_gap: Optional[float] = None
    price_economics: Optional[float] = None
    buyer_access: Optional[float] = None
    supply_stability: Optional[float] = None
    risk: Optional[float] = None


WEIGHTS = {
    "demand_momentum": 0.25,
    "supply_gap": 0.20,
    "price_economics": 0.20,
    "buyer_access": 0.15,
    "supply_stability": 0.10,
}


def score_opportunity(signals: OpportunitySignals) -> dict:
    """Return a weighted score, coverage and explanation.

    Missing dimensions are excluded from the weighted average and reduce coverage.
    Risk is deducted only when explicitly assessed; missing risk never means zero risk.
    """
    values = asdict(signals)
    available = {
        key: max(0.0, min(100.0, float(value)))
        for key, value in values.items()
        if value is not None
    }
    positive = {k: v for k, v in available.items() if k in WEIGHTS}
    covered_weight = sum(WEIGHTS[k] for k in positive)
    weighted = (
        sum(positive[k] * WEIGHTS[k] for k in positive) / covered_weight
        if covered_weight else 0.0
    )
    risk_penalty = (
        (available["risk"] / 100.0) * 10.0 if "risk" in available else None
    )
    final_score = max(0.0, weighted - (risk_penalty or 0.0))
    coverage = covered_weight / sum(WEIGHTS.values())
    if "risk" not in available:
        coverage *= 0.9
    return {
        "score": round(final_score, 1),
        "coverage": round(coverage, 3),
        "risk_penalty": round(risk_penalty, 1) if risk_penalty is not None else None,
        "components": values,
        "status": "research_priority" if coverage >= 0.6 else "insufficient_evidence",
        "method": "baseline-v0.1",
    }
