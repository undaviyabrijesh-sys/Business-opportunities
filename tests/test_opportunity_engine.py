import pytest

from src.opportunity_engine import (
    assess_capital_fit,
    assess_opportunity,
    calculate_unit_economics,
)


def test_unit_economics_calculates_contribution_and_funding():
    result = calculate_unit_economics(
        purchase_cost=100, freight_handling=10, other_variable_cost=5,
        selling_price=150, monthly_quantity=1000, monthly_fixed_cost=5000,
        setup_capex=200000, working_capital_days=30,
    )
    assert result["landed_cost_per_unit"] == 115
    assert result["contribution_per_unit"] == 35
    assert result["monthly_net_contribution"] == 30000
    assert result["working_capital_estimate"] == 115000
    assert result["estimated_funding_need"] == 315000
    assert result["simple_payback_months"] == pytest.approx(6.7, abs=0.1)


def test_capital_fit_uses_selected_user_band():
    assert assess_capital_fit(10_000_000, "₹50 lakh–₹2 crore")["status"] == "within_selected_band"
    assert assess_capital_fit(25_000_000, "₹50 lakh–₹2 crore")["status"] == "above_selected_band"


def test_missing_evidence_does_not_create_a_research_priority():
    result = assess_opportunity(
        {"demand_momentum": 80, "buyer_access": None},
        {"status": "within_selected_band"},
    )
    assert result["status"] == "insufficient_evidence"
    assert result["decision_gate"] == "collect_more_evidence_or_rework_capital"


def test_complete_evidence_and_capital_fit_can_pass_to_diligence():
    result = assess_opportunity(
        {
            "demand_momentum": 80, "supply_gap": 70, "price_economics": 75,
            "buyer_access": 65, "supply_stability": 70, "risk": 20,
        },
        {"status": "within_selected_band"},
    )
    assert result["coverage"] == 1.0
    assert result["decision_gate"] == "screen_for_diligence"


def test_negative_commercial_inputs_are_rejected():
    with pytest.raises(ValueError):
        calculate_unit_economics(100, -1, 0, 150, 100)


def test_evidence_scores_must_be_in_range():
    with pytest.raises(ValueError):
        assess_opportunity({"demand_momentum": 120}, {"status": "within_selected_band"})
