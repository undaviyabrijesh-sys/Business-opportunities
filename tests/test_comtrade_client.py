import pytest

from src.connectors.comtrade import ComtradeClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append((url, dict(params), timeout))
        return FakeResponse({"data": [{"period": params["period"]}], "messages": []})


def test_public_preview_splits_multi_year_periods(monkeypatch):
    monkeypatch.delenv("COMTRADE_API_KEY", raising=False)
    session = FakeSession()
    client = ComtradeClient(session=session)
    result = client.query(
        reporter_code="699", partner_code="0", cmd_code="091030",
        period="2023,2024,2025", flow_code="X",
    )
    assert [call[1]["period"] for call in session.calls] == ["2023", "2024", "2025"]
    assert all("/public/v1/preview/" in call[0] for call in session.calls)
    assert [row["period"] for row in result["data"]] == ["2023", "2024", "2025"]


def test_authenticated_query_keeps_period_list_in_single_call(monkeypatch):
    monkeypatch.setenv("COMTRADE_API_KEY", "test-key")
    session = FakeSession()
    client = ComtradeClient(session=session)
    client.query(
        reporter_code="699", partner_code="0", cmd_code="091030",
        period="2023,2024", flow_code="M",
    )
    assert len(session.calls) == 1
    assert "/data/v1/get/" in session.calls[0][0]
    assert session.calls[0][1]["subscription-key"] == "test-key"
