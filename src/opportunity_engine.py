"""Evidence-aware opportunity screening and first-pass unit economics.

This module calculates from user-supplied commercial assumptions. It does not
fetch live prices or certify demand, buyer interest, regulatory fit or capex.
"""
from __future__ import annotations

from typing import Optional

CAPITAL_BANDS = {
    "Below ₹5 lakh": (0.0, 500_000.0),
    "₹5–25 lakh": (500_000.0, 2_500_000.0),
    "₹25–50 lakh": (2_500_000.0, 5_000_000.0),
    "₹50 lakh–₹2 crore": (5_000_000.0, 20_000_000.0),
    "Above ₹2 crore": (20_000_000.0, float("inf")),
}


def capital_band_limits(label: str) -> tuple[float, float]:
    """Return the numeric screening range for a sidebar capital profile."""
    if label not in CAPITAL_BANDS:
        raise ValueError(f"Unknown capital band: {label}")
    return CAPITAL_BANDS[label]


def calculate_unit_economics(
    purchase_cost: float,
    freight_handling: float,
    other_variable_cost: float,
    selling_price: float,
    monthly_quantity: float,
    monthly_fixed_cost: float = 0.0,
    setup_capex: float = 0.0,
    working_capital_days: float = 30.0,
) -> dict:
    """Calculate first-pass contribution and working-capital requirement."""
    inputs = {
        "purchase_cost": purchase_cost,
        "freight_handling": freight_handling,
        "other_variable_cost": other_variable_cost,
        "selling_price": selling_price,
        "monthly_quantity": monthly_quantity,
        "monthly_fixed_cost": monthly_fixed_cost,
        "setup_capex": setup_capex,
        "working_capital_days": working_capital_days,
    }
    if any(float(value) < 0 for value in inputs.values()):
        raise ValueError("Commercial inputs cannot be negative.")
    landed_cost = purchase_cost + freight_handling + other_variable_cost
    contribution = selling_price - landed_cost
    margin_pct = (contribution / selling_price * 100) if selling_price else None
    monthly_gross_contribution = contribution * monthly_quantity
    monthly_net_contribution = monthly_gross_contribution - monthly_fixed_cost
    working_capital = landed_cost * monthly_quantity * working_capital_days / 30.0
    total_funding = setup_capex + working_capital
    payback_months = (
        setup_capex / monthly_net_contribution
        if setup_capex > 0 and monthly_net_contribution > 0 else None
    )
    return {
        "landed_cost_per_unit": round(landed_cost, 2),
        "contribution_per_unit": round(contribution, 2),
        "contribution_margin_pct": round(margin_pct, 2) if margin_pct is not None else None,
        "monthly_gross_contribution": round(monthly_gross_contribution, 2),
        "monthly_net_contribution": round(monthly_net_contribution, 2),
        "working_capital_estimate": round(working_capital, 2),
        "setup_capex": round(setup_capex, 2),
        "estimated_funding_need": round(total_funding, 2),
        "simple_payback_months": round(payback_months, 1) if payback_months is not None else None,
        "status": "positive_contribution" if contribution > 0 else "negative_or_zero_contribution",
        "assumption_note": "Working capital uses landed cost × monthly volume × days/30; it excludes receivables, payables, tax, buffers and financing costs.",
    }


def assess_capital_fit(funding_need: float, capital_band: str) -> dict:
    """Compare estimated funding need with the user's selected capital band."""
    low, high = capital_band_limits(capital_band)
    if funding_need <= 0:
        status = "not_estimated"
    elif funding_need <= high:
        # The selected amount is available capacity, not a minimum project size.
        status = "within_selected_band"
    else:
        status = "above_selected_band"
    return {"status": status, "band_min": low, "band_max": high, "funding_need": round(funding_need, 2)}


def assess_opportunity(signals: dict[str, Optional[float]], capital_fit: dict) -> dict:
    """Score only assessed evidence dimensions; do not treat missing as zero risk."""
    from src.scoring import OpportunitySignals, score_opportunity

    allowed = {"demand_momentum", "supply_gap", "price_economics", "buyer_access", "supply_stability", "risk"}
    unknown = set(signals) - allowed
    if unknown:
        raise ValueError(f"Unknown evidence dimensions: {', '.join(sorted(unknown))}")
    for name, value in signals.items():
        if value is not None and not 0 <= float(value) <= 100:
            raise ValueError(f"{name} must be between 0 and 100.")
    result = score_opportunity(OpportunitySignals(**signals))
    result["capital_fit"] = capital_fit["status"]
    result["decision_gate"] = (
        "screen_for_diligence"
        if result["coverage"] >= 0.6 and capital_fit["status"] == "within_selected_band"
        else "collect_more_evidence_or_rework_capital"
    )
    return result
