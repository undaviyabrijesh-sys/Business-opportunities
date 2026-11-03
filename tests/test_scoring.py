from src.scoring import OpportunitySignals, score_opportunity


def test_full_score_is_bounded_and_explained():
    result = score_opportunity(OpportunitySignals(80, 70, 90, 60, 75, 30))
    assert 0 <= result["score"] <= 100
    assert result["coverage"] == 1.0
    assert result["risk_penalty"] == 3.0
    assert result["status"] == "research_priority"


def test_missing_signals_reduce_coverage():
    result = score_opportunity(OpportunitySignals(demand_momentum=80))
    assert result["coverage"] < 1
    assert result["status"] == "insufficient_evidence"


def test_missing_risk_is_not_treated_as_zero_risk():
    result = score_opportunity(OpportunitySignals(80, 80, 80, 80, 80, None))
    assert result["risk_penalty"] is None
    assert result["coverage"] < 1
