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
        return FakeResponse({"data": [{"reporterDesc": "United States", "period": params["period"]}], "messages": []})


def test_global_import_market_query_uses_all_reporters_and_import_flow(monkeypatch):
    monkeypatch.delenv("COMTRADE_API_KEY", raising=False)
    session = FakeSession()
    client = ComtradeClient(session=session)
    result = client.query(
        reporter_code="ALL", partner_code="0", cmd_code="391239",
        period="2023,2024", flow_code="M",
    )
    assert [call[1]["reporterCode"] for call in session.calls] == ["ALL", "ALL"]
    assert all(call[1]["flowCode"] == "M" for call in session.calls)
    assert all(call[1]["partnerCode"] == "0" for call in session.calls)
    assert len(result["data"]) == 2
